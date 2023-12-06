import OthelloLogic
import random
import OthelloLogic
import Evaluate
import copy
import InactiveEvaluate
from typing import List

SIZE = 8
LIMIT = 5
turnCnt = 0
isActiveMode = False

evaluateCnt = 0


def getAction(board, moves) -> List[int]:
    check_active_mode()

    # return select_max_eval_moves(board, moves, 1)
    # return inactive_action(board, moves, 1)

    # 自分のターンにフロントエンドから呼ばれるメソッド
    check_active_mode()

    # return select_max_eval_moves(board, moves, 1)

    maxEvalMove = float("-inf"), None
    for move in moves:
        eval = minLevel(board, move, LIMIT, -1)
        print("=====================================")
        print(f"move : {move} eval: {eval}")
        print("=====================================")
        if eval > maxEvalMove[0]:
            maxEvalMove = eval, move
    print(f"決定した手: {maxEvalMove[1]} 評価値: {maxEvalMove[0]}")
    print(f"evaluateCnt: {evaluateCnt}")
    reset_evaluateCnt()
    return maxEvalMove[1]


def inactive_action(board, moves, player):
    """
    受け取ったmovesを戦略の優先度でソートしてに次のターンで相手にすべての石をひっくり返されない手を返す
    """
    sortedMoves = InactiveEvaluate.sort_moves_inactive(board, moves, player)
    InactiveEvaluate.debug_check_sort(board, sortedMoves)
    for move in sortedMoves:
        if InactiveEvaluate.check_my_stone_all_reverse(board, move):
            return move
    print("相手にすべての石をひっくり返される手しかないので最初の要素を返します")
    return sortedMoves[0]


def minLevel(board, move, limit, player) -> float:
    if limit == 0:
        increment_evaluateCnt()
        return Evaluate.evaluate_move(board, move, player) * player

    nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, -player, SIZE)
    nextMoves = OthelloLogic.getMoves(nextBoard, player, SIZE)

    if len(nextMoves) == 0:
        increment_evaluateCnt()
        return Evaluate.evaluate_move(board, move, player) * player

    # debug_print(move, limit, player, nextBoard, nextMoves)

    minEval = float("inf")
    for nextMove in nextMoves:
        minEval = min(maxLevel(nextBoard, nextMove, limit - 1, -player), minEval)

    return minEval


def maxLevel(board, move, limit, player) -> float:
    if limit == 0:
        increment_evaluateCnt()
        return Evaluate.evaluate_move(board, move, player) * player

    nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, -player, SIZE)
    nextMoves = OthelloLogic.getMoves(nextBoard, player, SIZE)

    if len(nextMoves) == 0:
        increment_evaluateCnt()
        return Evaluate.evaluate_move(board, move, player) * player

    # debug_print(move, limit, player, nextBoard, nextMoves)

    maxEval = float("-inf")
    for nextMove in nextMoves:
        maxEval = max(minLevel(nextBoard, nextMove, limit - 1, -player), maxEval)

    return maxEval


def increment_evaluateCnt():
    global evaluateCnt
    evaluateCnt += 1


def reset_evaluateCnt():
    global evaluateCnt
    evaluateCnt = 0


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

    print(f"turnCnt: {turnCnt} isActiveMode: {isActiveMode}")


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
