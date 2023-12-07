import OthelloLogic
import Evaluate
import copy
import InactiveEvaluate
import time
from multiprocessing import Pool
from typing import List


def getAction(board, moves) -> List[int]:
    print("=====================================")
    print(f"len : {len(moves)} moves: {moves}")

    if check_active_mode(board) is False:
        # 30ターン経過していない場合は最弱モード
        return inactive_action(board, moves, 1)

    # 処理時間計測開始
    start_time = time.time()

    # アルファとベータの初期値
    alpha = float("-inf")
    beta = float("inf")

    stoneNum = count_stone(board)
    print(f"stoneNum: {stoneNum}")
    limit = 0
    if stoneNum >= 48:
        limit = 8
    else:
        limit = 5 if len(moves) >= 12 else 6  # 6

    print(f"limit: {limit}")

    # プールを作成
    with Pool() as pool:
        evals = pool.starmap(
            minLevel, [(board, move, limit, -1, alpha, beta) for move in moves]
        )

    maxEvalMove = float("-inf"), None
    for move, eval in zip(moves, evals):
        if eval > maxEvalMove[0]:
            maxEvalMove = eval, move

    end_time = time.time()
    print(f"決定した手: {maxEvalMove[1]} 評価値: {maxEvalMove[0]}")
    print(f"処理時間: {end_time - start_time}s")
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


def minLevel(board, move, limit, player, alpha, beta):
    nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, -player, 8)
    nextMoves = OthelloLogic.getMoves(nextBoard, player, 8)

    if len(nextMoves) == 0 or limit == 0:
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
