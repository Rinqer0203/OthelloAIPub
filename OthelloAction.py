import OthelloLogic
import random
import Evaluate
import copy
from typing import List

SIZE = 8
LIMIT = 2
turnCnt = 0
isActiveMode = False


def getAction(board, moves) -> List[int]:
    # 自分のターンにフロントエンドから呼ばれるメソッド
    check_active_mode()

    # return select_max_eval_moves(board, moves, 1)

    maxEvalMove = float("-inf"), None
    for move in moves:
        eval = minLevel(board, move, LIMIT, -1)
        # print(f"eval: {eval}")
        if eval > maxEvalMove[0]:
            maxEvalMove = eval, move
    return maxEvalMove[1]


def minLevel(board, move, limit, player) -> float:
    if limit == 0:
        return Evaluate.evaluate_move(board, move, player) * player

    nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, -player, SIZE)
    nextMoves = OthelloLogic.getMoves(nextBoard, player, SIZE)

    if len(nextMoves) == 0:
        return Evaluate.evaluate_move(board, move, player) * player

    debug_print(move, limit, player, nextBoard, nextMoves)

    minEval = float("inf")
    for nextMove in nextMoves:
        minEval = min(maxLevel(nextBoard, nextMove, limit - 1, -player), minEval)
    return minEval


def maxLevel(board, move, limit, player) -> float:
    if limit == 0:
        return Evaluate.evaluate_move(board, move, player) * player

    nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, -player, SIZE)
    nextMoves = OthelloLogic.getMoves(nextBoard, player, SIZE)

    if len(nextMoves) == 0:
        return Evaluate.evaluate_move(board, move, player) * player

    debug_print(move, limit, player, nextBoard, nextMoves)

    maxEval = float("-inf")
    for nextMove in nextMoves:
        maxEval = max(minLevel(nextBoard, nextMove, limit - 1, -player), maxEval)
    return maxEval


def debug_print(move, limit, player, nextBoard, nextMoves):
    print(f"-------- move: {move} limit: {limit} player: {player} --------")
    OthelloLogic.printBoardWithCell(nextBoard, player, nextMoves, SIZE)
    print(f"nextMoves: {nextMoves}\n")


def check_active_mode():
    """
    30ターン経過したらisActiveModeをTrueにする
    """
    global turnCnt
    global isActiveMode

    if turnCnt > 30:
        isActiveMode = True
    turnCnt += 2

    # print(f"turnCnt: {turnCnt} isActiveMode: {isActiveMode}")


def select_max_eval_moves(board, moves, player) -> List[int]:
    """
    渡されたMovesの中から評価値が最大のものを返却する。
    """
    maxEvalMove = float("-inf"), None

    for move in moves:
        eval = Evaluate.evaluate_move(board, move, player)
        if maxEvalMove[0] < eval:
            maxEvalMove = eval, move

    print(f"決定した手: {maxEvalMove[1]} 評価値: {maxEvalMove[0]}")
    return maxEvalMove[1]


def select_random_moves(moves) -> List[int]:
    """
    渡されたMovesの中からランダムで返り値として返却する。
    """
    index = random.randrange(len(moves))
    return moves[index]
