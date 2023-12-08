import TestBoardProvider
import OthelloLogic
import subprocess
import ctypes
import time
from typing import List

FILE_NAMES = r"C\OthelloAction.c C\OthelloLogic.c"
RESULT_FILE_NAME = "OthelloAction"
COMPILE_COMMAND = rf"gcc {FILE_NAMES} -shared -O2 -o {RESULT_FILE_NAME}.dll"

MOVES_MAX_LENGTH = 60  # movesの最大長


class CModule:
    def __init__(self, dll):
        self.dll = dll
        self.MOVES_MAX_LENGTH = 60  # movesの最大長

        self.dll.getMovesC.restype = ctypes.POINTER(
            (ctypes.c_int * 2) * (MOVES_MAX_LENGTH + 1)
        )
        self.dll.Action.restype = ctypes.POINTER(ctypes.c_int * 2)

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

    def get_action(self, board, moves) -> List[int]:
        board_array = self.__convert_2d_array(ctypes.c_int, board)
        moves_array = self.__convert_2d_array(
            ctypes.c_int, moves[: self.MOVES_MAX_LENGTH]
        )

        result_ptr = self.dll.Action(board_array, moves_array, len(moves))

        # 結果をPythonのリストに変換
        return list(result_ptr.contents)

    def get_moves(self, board):
        board_array = self.__convert_2d_array(ctypes.c_int, board)
        result_ptr = self.dll.getMovesC(board_array)

        # 結果をPythonのリストに変換
        moves = []
        for move in result_ptr.contents:
            if move[0] == -1 and move[1] == -1:
                break
            moves.append(list(move))

        return moves


def generate_c_module() -> ctypes.WinDLL:
    """
    dllをロードしてインスタンス生成
    """
    __compile_c()
    return CModule(__load_dll())


def __compile_c():
    subprocess.run(COMPILE_COMMAND, check=True)


def __load_dll() -> ctypes.WinDLL:
    return ctypes.WinDLL(rf".\{RESULT_FILE_NAME}.dll")


def benchmark():
    cModule = generate_c_module()
    board = TestBoardProvider.generate_initial_board()

    start_time = time.time()
    for _ in range(1000):
        moves = cModule.get_moves(board)
    end_time = time.time()
    print(f"cModule 処理時間: {end_time - start_time}s")

    start_time = time.time()
    for _ in range(1000):
        moves = OthelloLogic.getMoves(board, 1, 8)
    end_time = time.time()
    print(f"python 処理時間: {end_time - start_time}s")


if __name__ == "__main__":
    benchmark()
