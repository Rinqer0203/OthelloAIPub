import random
import Evaluate
from typing import List

turnCnt = 0
isActiveMode = False


def getAction(board, moves) -> List[int]:
    # 自分のターンにフロントエンドから呼ばれるメソッド

    check_active_mode()
    # print(f"turnCnt: {turnCnt} isActiveMode: {isActiveMode}")

    return select_max_eval_moves(board, moves, 1)


def check_active_mode():
    global turnCnt
    global isActiveMode

    if turnCnt > 30:
        isActiveMode = True
    turnCnt += 2


def select_max_eval_moves(board, moves, player) -> List[int]:
    maxEvalMove = float("-inf"), None

    for move in moves:
        eval = Evaluate.evaluate_move(board, move, player)
        if maxEvalMove[0] < eval:
            maxEvalMove = eval, move

    print(f"決定した手: {maxEvalMove[1]} 評価値: {maxEvalMove[0]}")
    return maxEvalMove[1]


def select_random_moves(moves) -> List[int]:
    # 渡されたMovesの中からランダムで返り値として返却する。
    index = random.randrange(len(moves))
    return moves[index]
