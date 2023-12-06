import OthelloLogic
import TestBoardProvider

# Boardに対する評価関数 evaluate(self, board, player)を実装したクラス定義


class __TestEvaluate:
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

    def evaluate(self, board, player) -> float:
        playerScore = enemyScore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == 1:
                    playerScore += self.baseBoardPoint[x][y]
                elif board[x][y] == -1:
                    enemyScore += self.baseBoardPoint[x][y]

        if player == 1:
            return playerScore - enemyScore
        return enemyScore - playerScore


# -----------------ここまでBoard評価関数の定義-----------------


# Moveに対する評価関数 evaluate(self, board, move, player)を実装したクラス定義


class __EvaluateBaseBoard:
    def __init__(self):
        self.baseBoardPoint = [
            [30, -10, 2, 1, 1, 2, -10, 30],
            [-10, -20, -3, -3, -3, -3, -20, -10],
            [2, -3, 2, 0, 0, 2, -3, 2],
            [1, -3, 0, 0, 0, 0, -3, 1],
            [1, -3, 0, 0, 0, 0, -3, 1],
            [2, -3, 2, 0, 0, 2, -3, 2],
            [-10, -20, -3, -3, -3, -3, -20, -10],
            [30, -10, 2, 1, 1, 2, -10, 30],
        ]

    def evaluate(self, board, move, player):
        return self.baseBoardPoint[move[0]][move[1]]


# -----------------ここまでMove評価関数の定義-----------------


# 初期化処理
# 評価関数を追加したらここに追加する
__evalute_board_funcs = [__TestEvaluate()]

__evaluate_move_funcs = [__EvaluateBaseBoard()]


# 評価関数を回してBoard評価値の合計を返す
def evaluate_board(board, player) -> float:
    evaluate_point = 0
    for func in __evalute_board_funcs:
        evaluate_point += func.evaluate(board, player)
    return evaluate_point


# 評価関数を回してMove評価値の合計を返す
def evaluate_move(board, move, player) -> float:
    evaluate_point = 0
    for func in __evaluate_move_funcs:
        evaluate_point += func.evaluate(board, move, player)
    return evaluate_point


# テスト用
if __name__ == "__main__":
    board = TestBoardProvider.generate_initial_board()

    print("boardの評価値を返す関数のテスト")
    eval = evaluate_board(board, 1)
    print(eval)

    print("moveの評価値を返す関数のテスト")
    for x in range(8):
        for y in range(8):
            move = [x, y]
            eval = evaluate_move(board, move, 1)
            print(eval, end=" | ")
        print()
