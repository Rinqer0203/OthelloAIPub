import random
import OthelloLogic
import Evaluate
import copy
from typing import List

turnCnt = 0
isActiveMode = False


def getAction(board, moves) -> List[int]:
    # 自分のターンにフロントエンドから呼ばれるメソッド

    check_active_mode()

    # return select_max_eval_moves(board, moves, 1)
    return inactive_action(board, moves, 1)


def inactive_action(board, moves, player):
    """
    受け取ったmovesで裏返せる石の数が最小の手で相手に次のターンで相手にすべての石をひっくり返されない手を返す
    """
    sortedMoves = sort_moves_by_flippable(board, moves, player)  # ソート
    for move in sortedMoves:
        if check_my_stone_all_reverse(board, move) is True:  # ここでチェック関数を呼ぶ
            return move


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


def sort_moves_by_flippable(board, moves, player):
    """
    ひっくり返せる石が少ない順にソートする
    """
    return sorted(
        moves, key=lambda move: OthelloLogic.countFlippable(board, move, player, 8)
    )


def check_my_stone_all_reverse(board, move):
    """
    次のターンで相手にすべての石をひっくり返されないかチェックする
    """
    nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, 1, 8)
    nextEnemyMoves = OthelloLogic.getMoves(nextBoard, -1, 8)

    for enemyMove in nextEnemyMoves:
        nextNextBoard = OthelloLogic.execute(copy.deepcopy(nextBoard), enemyMove, -1, 8)
        nextNextMyMoves = OthelloLogic.getMoves(nextNextBoard, 1, 8)
        if len(nextNextMyMoves) == 0:
            return False
    return True


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
