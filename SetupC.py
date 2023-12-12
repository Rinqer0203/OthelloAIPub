import TestBoardProvider
import OthelloLogic
import OthelloAction
import Evaluate
import subprocess
import ctypes
import time
from typing import List

FILE_NAMES = r"C\OthelloAction.c C\OthelloLogic.c C\ActiveEvaluate.c"
RESULT_FILE_NAME = "OthelloAction"
ENEMY_FILE_NAME = "EnemyOthelloAction"
COMPILE_COMMAND = rf"gcc {FILE_NAMES} -shared -O2 -o {RESULT_FILE_NAME}.dll"

MOVES_MAX_LENGTH = 60  # movesの最大長

isCompiled = False


class CModule:
    def __init__(self, dll):
        self.dll = dll
        self.MOVES_MAX_LENGTH = 60  # movesの最大長

        self.dll.getMovesC.restype = ctypes.POINTER(
            (ctypes.c_int * 2) * (MOVES_MAX_LENGTH + 1)
        )

        self.dll.minLevelWrapper.restype = ctypes.c_float
        self.dll.minLevelWrapper.argtypes = [
            ctypes.POINTER((ctypes.c_int * 8) * 8),  # ボード配列の型
            ctypes.c_int,  # limit
            ctypes.c_int,  # player
        ]

    def __convert_2d_array(self, c_type, data):
        """
        ctypes用の2次元配列の型を定義して変換
        """
        rows, cols = len(data), len(data[0])
        ArrayType = (c_type * cols) * rows
        array = ArrayType()
        for i, row in enumerate(data):
            array[i] = (c_type * cols)(*row)
        return array

    def get_moves(self, board, player):
        board_array = self.__convert_2d_array(ctypes.c_int, board)
        result_ptr = self.dll.getMovesC(board_array, player)

        # 結果をPythonのリストに変換
        moves = []
        for move in result_ptr.contents:
            if move[0] == -1 and move[1] == -1:
                break
            moves.append(list(move))

        return moves

    def minLevel(self, board, limit, player, alpha, beta):
        board_array = self.__convert_2d_array(ctypes.c_int, board)
        return self.dll.minLevel(board_array, limit, player, alpha, beta)

    def minLevelWrapper(self, board, limit, player):
        board_array = self.__convert_2d_array(ctypes.c_int, board)
        return self.dll.minLevelWrapper(board_array, limit, player)


def generate_c_module() -> CModule:
    """
    dllをロードしてインスタンス生成
    """
    return CModule(__load_dll(RESULT_FILE_NAME))


def generate_enemy_c_module() -> CModule:
    return CModule(__load_dll(ENEMY_FILE_NAME))


def compile_c():
    subprocess.run(COMPILE_COMMAND, check=True)


def __load_dll(fileName) -> ctypes.WinDLL:
    return ctypes.WinDLL(rf".\{fileName}.dll")


def benchmark():
    cModule = generate_c_module()
    board = TestBoardProvider.generate_initial_board()
    player = 1

    start_time = time.time()
    for _ in range(1000):
        moves = cModule.get_moves(board, player)
    end_time = time.time()
    print(f"cModule 処理時間: {end_time - start_time}s")

    start_time = time.time()
    for _ in range(1000):
        moves = OthelloLogic.getMoves(board, 1, 8)
    end_time = time.time()
    print(f"python 処理時間: {end_time - start_time}s")


def check_move():
    cModule = generate_c_module()
    board = TestBoardProvider.generate_board2()
    player = 1

    print(cModule.get_moves(board, player))
    print(OthelloLogic.getMoves(board, player, 8))


def check_evaluates():
    OthelloAction.test2(TestBoardProvider.generate_initial_board(), 4)
    OthelloAction.test2(TestBoardProvider.generate_board1(), 4)
    OthelloAction.test2(TestBoardProvider.generate_board2(), 4)
    OthelloAction.test2(TestBoardProvider.generate_board3(), 4)
    OthelloAction.test2(TestBoardProvider.generate_board4(), 4)
    OthelloAction.test2(TestBoardProvider.generate_inactive_board1(), 4)
    OthelloAction.test2(TestBoardProvider.generate_inactive_board2(), 4)
    OthelloAction.test2(TestBoardProvider.generate_evaluate_board1(), 4)


def benchmark_minimax(cModule, board, limit):
    start_time = time.time()
    eval = cModule.evaluate(board, -1, limit)
    end_time = time.time()
    print(f"C eval: {eval} 処理時間: {end_time - start_time}s")

    start_time = time.time()
    eval = OthelloAction.test(board, -1, limit)
    end_time = time.time()
    print(f"python eval: {eval} 処理時間: {end_time - start_time}s")


def benchmark_minimax2(cModule, board, limit):
    start_time = time.time()
    eval = cModule.minLevelWrapper(board, limit, -1)
    end_time = time.time()
    print(f"処理時間: {end_time - start_time}s")


def benchmark_minimax2_exe():
    cModule = generate_enemy_c_module()
    limit = 10

    benchmark_minimax2(cModule, TestBoardProvider.generate_initial_board(), limit)
    benchmark_minimax2(cModule, TestBoardProvider.generate_board1(), limit)
    benchmark_minimax2(cModule, TestBoardProvider.generate_board2(), limit)
    benchmark_minimax2(cModule, TestBoardProvider.generate_board3(), limit)
    benchmark_minimax2(cModule, TestBoardProvider.generate_board4(), limit)
    benchmark_minimax2(cModule, TestBoardProvider.generate_inactive_board1(), limit)
    benchmark_minimax2(cModule, TestBoardProvider.generate_inactive_board2(), limit)
    benchmark_minimax2(cModule, TestBoardProvider.generate_evaluate_board1(), limit)


if __name__ == "__main__":
    compile_c()

    benchmark_minimax2_exe()

    # benchmark()
    # check_move()
    # test_evaluates(cModule, player)
    # benchmark_minimax(cModule, board, 5)
