import OthelloLogic
import copy
import InactiveEvaluate


class __InactiveEvaluateBaseBoard:
    def __init__(self):
        # 中心に近いほどポイントが高くなるように設定
        self.baseBoardPoint = [
            [0, 1, 2, 2, 2, 2, 1, 0],
            [1, 1, 3, 3, 3, 3, 3, 1],
            [2, 3, 4, 4, 4, 4, 3, 2],
            [2, 3, 4, 5, 5, 4, 3, 2],
            [2, 3, 4, 5, 5, 4, 3, 2],
            [2, 3, 4, 4, 4, 4, 3, 2],
            [1, 1, 3, 3, 3, 3, 1, 1],
            [0, 1, 2, 2, 2, 2, 1, 0],
        ]

    def evaluate(self, board, move, player):
        return self.baseBoardPoint[move[0]][move[1]]


class __InactiveEvaluateDangerous:
    def __init__(self):
        # 　角周りは避けるように設定
        self.baseBoardPoint = [
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
        ]

    def isDangerousMove(self, move) -> bool:
        return self.baseBoardPoint[move[0]][move[1]] == 1


__evaluate_base_board = __InactiveEvaluateBaseBoard()


__dangerous_evaluate_move_func = __InactiveEvaluateDangerous()


def inactive_evaluate_move(board, move, player) -> float:
    return __evaluate_base_board.evaluate(board, move, player)


def is_dangerous_move(move) -> bool:
    return __dangerous_evaluate_move_func.isDangerousMove(move)


def sort_moves_inactive(board, moves, player):
    """
    最弱モードで優先的に打つ手をソートする
    角周りの危険なゾーンは最後尾
    ひっくり返せる数の少ない順 (2個以下ならひっくり返せる数よりも評価関数を優先する)
    評価関数の高い順 (中心に近いほどポイントが高くなるように設定)
    """
    return sorted(
        moves,
        key=lambda move: (
            1 if InactiveEvaluate.is_dangerous_move(move) else 0,
            OthelloLogic.countFlippable(board, move, player, 8),
            -InactiveEvaluate.inactive_evaluate_move(board, move, player),
        ),
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


def debug_check_sort(board, moves):
    print(f"moves: {moves}")

    sortedMoves = sort_moves_inactive(board, moves, 1)

    for move in sortedMoves:
        flippable = OthelloLogic.countFlippable(board, move, 1, 8)
        eval = InactiveEvaluate.inactive_evaluate_move(board, move, 1)
        isDangerous = InactiveEvaluate.is_dangerous_move(move)
        print(
            f"move: {move} flippable: {flippable} eval: {eval} isDangerous: {isDangerous}"
        )
