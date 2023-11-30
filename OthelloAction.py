import random
import Evaluate
from typing import List

turnCnt = 0
isActiveMode = False


def getAction(board, moves) -> List[int]:
    # 自分のターンにフロントエンドから呼ばれるメソッド
    check_active_mode()
    # 現在の状態をデバッグ出力
    # print(f"turnCnt: {turnCnt} isActiveMode: {isActiveMode}")
    return select_random_moves(moves)


def check_active_mode():
    global turnCnt
    global isActiveMode

    if turnCnt > 30:
        isActiveMode = True
    turnCnt += 2


def select_random_moves(moves) -> List[int]:
    # 渡されたMovesの中からランダムで返り値として返却する。
    index = random.randrange(len(moves))
    return moves[index]
