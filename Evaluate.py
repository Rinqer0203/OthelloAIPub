import OthelloLogic
import TestBoardProvider

# Boardに対する評価関数 evaluate(self, board, player)を実装したクラス定義


class __EvaluateBase:
    def __init__(self):
        self.baseBoardPoint = [
            [30, -12, 0, -1, -1, 0, -12, 30],
            [-12, -15, -3, -3, -3, -3, -15, -12],
            [0, -3, 0, -1, -1, 0, -3, 0],
            [-1, -3, -1, -1, -1, -1, -3, -1],
            [-1, -3, -1, -1, -1, -1, -3, -1],
            [0, -3, 0, -1, -1, 0, -3, 0],
            [-12, -15, -3, -3, -3, -3, -15, -12],
            [30, -12, 0, -1, -1, 0, -12, 30],
        ]
        self.leftUpAround = [
            [0, 1],
            [1, 0],
            [1, 1],
        ]
        self.rightUpAround = [
            [0, 6],
            [1, 6],
            [1, 7],
        ]
        self.leftDownAround = [
            [6, 0],
            [6, 1],
            [7, 1],
        ]
        self.rightDownAround = [
            [6, 6],
            [6, 7],
            [7, 6],
        ]

    def is_special_corner_around(self, x, y, board, player):
        if [x, y] in self.leftUpAround and board[0][0] == player:
            return True
        if [x, y] in self.rightUpAround and board[0][7] == player:
            return True
        if [x, y] in self.leftDownAround and board[7][0] == player:
            return True
        if [x, y] in self.rightDownAround and board[7][7] == player:
            return True
        return False

    def evaluate(self, board, player) -> float:
        playerScore = enemyScore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == player:
                    score = (
                        0
                        if self.is_special_corner_around(x, y, board, player)
                        else self.baseBoardPoint[x][y]
                    )
                    playerScore += score
                elif board[x][y] == -player:
                    score = (
                        0
                        if self.is_special_corner_around(x, y, board, -player)
                        else self.baseBoardPoint[x][y]
                    )
                    enemyScore += score
        return playerScore - enemyScore


class __EvaluateStoneCount:
    def evaluate(self, board, player) -> float:
        playerStones = sum(board[x][y] == player for x in range(8) for y in range(8))
        enemyStones = sum(board[x][y] == -player for x in range(8) for y in range(8))
        # evalを正規化
        if playerStones + enemyStones == 0:
            return 0
        return (playerStones - enemyStones) / (playerStones + enemyStones)


# -----------------ここまでBoard評価関数の定義-----------------


# 初期化処理
# 評価関数を追加したらここに追加する
__evalute_board_funcs = [
    __EvaluateBase(),
    __EvaluateStoneCount(),
]


# 評価関数を回してBoard評価値の合計を返す
def evaluate_board(board, player) -> float:
    evaluate_point = 0
    for func in __evalute_board_funcs:
        evaluate_point += func.evaluate(board, player)
    return evaluate_point * player


# テスト用
if __name__ == "__main__":
    board = TestBoardProvider.generate_evaluate_board1()
    eval = evaluate_board(board, 1)
    print(f"board eval: {eval}")
