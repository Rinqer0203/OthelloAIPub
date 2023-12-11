import OthelloLogic
import Evaluate
import copy
import InactiveEvaluate
import time
import SetupC
from multiprocessing import Pool
from typing import List


def evaluate_wrapper(board, player, limit):
    cModule = SetupC.generate_c_module()
    return cModule.evaluate(board, player, limit)


def getAction(board, moves) -> List[int]:
    print("=====================================")
    print(f"len : {len(moves)} moves: {moves}")

    if check_active_mode(board) is False and False:
        # 30ターン経過していない場合は最弱モード
        return inactive_action(board, moves, 1)

    # 処理時間計測開始
    start_time = time.time()

    # 探索の深さを決定
    stoneNum = count_stone(board)
    print(f"stoneNum: {stoneNum}")
    limit = 6

    print(f"limit: {limit}")

    cModule = SetupC.generate_c_module()
    maxEvalMove = float("-inf"), None
    for move in moves:
        nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, 1, 8)
        OthelloLogic.printBoard(nextBoard)
        eval = cModule.evaluate(nextBoard, -1, limit)
        if eval > maxEvalMove[0]:
            maxEvalMove = eval, move

    end_time = time.time()
    print(f"決定した手: {maxEvalMove[1]} 評価値: {maxEvalMove[0]}")
    print(f"処理時間: {end_time - start_time}s")
    return maxEvalMove[1]

    """
    #並列化しない場合
    maxEvalMove = float("-inf"), None
    for move in moves:
        eval = minLevel(board, move, limit, -1, alpha, beta)
        if eval > maxEvalMove[0]:
            maxEvalMove = eval, move
    """


evalCnt = 0


def test(board, player, limit):
    # アルファとベータの初期値
    alpha = float("-inf")
    beta = float("inf")

    moves = OthelloLogic.getMoves(board, player, 8)
    maxEvalMove = float("-inf"), None
    for move in moves:
        eval = minLevel(board, move, limit - 1, -player, alpha, beta)
        # print(f"move: {move} eval: {eval}")
        if eval > maxEvalMove[0]:
            maxEvalMove = eval, move

    print(f"evalCnt: {evalCnt}")
    return maxEvalMove[0]


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


def minLevel(board, move, limit, player, alpha, beta):
    nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, -player, 8)
    nextMoves = OthelloLogic.getMoves(nextBoard, player, 8)

    if len(nextMoves) == 0 or limit == 0:
        # evalCntをインクリメントする
        global evalCnt
        evalCnt += 1
        return Evaluate.evaluate_board(nextBoard, player)

    for nextMove in nextMoves:
        eval = maxLevel(nextBoard, nextMove, limit - 1, -player, alpha, beta)
        beta = min(beta, eval)
        if beta <= alpha:
            break  # アルファカットオフ
    return beta


def maxLevel(board, move, limit, player, alpha, beta):
    nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, -player, 8)
    nextMoves = OthelloLogic.getMoves(nextBoard, player, 8)

    if len(nextMoves) == 0 or limit == 0:
        # evalCntをインクリメントする
        global evalCnt
        evalCnt += 1
        return Evaluate.evaluate_board(nextBoard, player)

    for nextMove in nextMoves:
        eval = minLevel(nextBoard, nextMove, limit - 1, -player, alpha, beta)
        alpha = max(alpha, eval)
        if alpha >= beta:
            break  # ベータカットオフ
    return alpha


def check_active_mode(board):
    """
    30ターン経過したらTrueになる
    """
    return count_stone(board) >= 34


def count_stone(board):
    """
    石の数をカウントして返す
    """
    stoneCnt = 0
    # 石の数をカウント
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] != 0:
                stoneCnt += 1
    return stoneCnt


def debug_print(move, limit, player, nextBoard, nextMoves):
    print(f"-------- move: {move} limit: {limit} player: {player} --------")
    OthelloLogic.printBoardWithCell(nextBoard, player, nextMoves, 8)
    print(f"nextMoves: {nextMoves}\n")
