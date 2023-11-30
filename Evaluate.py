import OthelloLogic
import TestBoardProvider

# 評価関数 evaluate(self, board, player)を実装したクラス定義


class __TestEvaluate:
    def evaluate(self, board, player) -> float:
        # boardに対する評価値を返す
        return 3


class __TestEvaluate2:
    def evaluate(self, board, player) -> float:
        # boardに対する評価値を返す
        return 7


# -----------------ここまで評価関数の定義-----------------


# 初期化処理
# 評価関数を追加したらここに追加する
__evalute_funcs = [__TestEvaluate(), __TestEvaluate2()]


# 評価関数を回して評価値を返す
def evaluate_board(board, player) -> float:
    evaluate_point = 0
    for func in __evalute_funcs:
        evaluate_point += func.evaluate(board, player)
    return evaluate_point


print(evaluate_board(TestBoardProvider.get_initial_board(), 1))
# 　testのみだと10が出力される
