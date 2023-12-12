import OthelloLogic
import Evaluate
import copy
import InactiveEvaluate
import time
import SetupC
from multiprocessing import Pool
from typing import List

evalCnt = 0


def eval_move(args):
    board, move, limit = args
    cModule = SetupC.generate_c_module()
    nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, 1, 8)
    eval = cModule.minLevelWrapper(nextBoard, limit - 1, -1)
    return eval, move


def getAction(board, moves) -> List[int]:
    print("=====================================")
    print(f"len : {len(moves)} moves: {moves}")

    # 処理時間計測開始
    start_time = time.time()

    # 探索の深さを決定
    stoneNum = count_stone(board)
    print(f"stoneNum: {stoneNum}")
    limit = 0
    if stoneNum >= 48:
        limit = 7
    else:
        limit = 5 if len(moves) >= 12 else 6  # 6
    limit = 8

    print(f"limit: {limit}")

    maxEvalMove = float("-inf"), None

    pool = Pool()
    args = [(board, move, limit) for move in moves]
    results = pool.map(eval_move, args)
    pool.close()
    pool.join()

    for eval, move in results:
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


def test2(board, limit):
    "pythonとCの評価値を比較する"
    moves = OthelloLogic.getMoves(board, 1, 8)
    move = moves[0]

    pyEval = minLevel(board, move, limit - 1, -1, float("-inf"), float("inf"))
    print(f"python eval: {pyEval}")

    nextBoard = OthelloLogic.execute(copy.deepcopy(board), move, 1, 8)
    cModule = SetupC.generate_c_module()
    cEval = cModule.minLevelWrapper(nextBoard, limit - 1, -1)
    print(f"C eval: {cEval}")
    # pyeval と cevalの値が小数点第二位まで一致しているか確認する
    if round(pyEval, 2) == round(cEval, 2):
        print("OK")
    else:
        print("一致していない!!!!!!!!!!")


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


def debug_print(move, limit, player, nextBoard, nextMoves):
    print(f"-------- move: {move} limit: {limit} player: {player} --------")
    OthelloLogic.printBoardWithCell(nextBoard, player, nextMoves, 8)
    print(f"nextMoves: {nextMoves}\n")
