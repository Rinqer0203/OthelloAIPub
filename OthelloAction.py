import random
import Evaluate
from typing import List


def getAction(board, moves) -> List[int]:
    # 自分のターンにフロントエンドから呼ばれるメソッド
    return select_random_moves(moves)


def select_random_moves(moves) -> List[int]:
    # 渡されたMovesの中からランダムで返り値として返却する。
    index = random.randrange(len(moves))
    return moves[index]
