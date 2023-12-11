# ボードの状態を提供するクラス (テスト用)


def generate_initial_board():
    """
    初期状態のボードを返す
    """
    return [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, 1, 0, 0, 0],
        [0, 0, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]


def generate_board1():
    """
    パターン１のボードを返す
    """
    return [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, -1, -1, 0, 0],
        [0, -1, 1, -1, -1, -1, 0, 0],
        [0, 0, 0, 1, -1, -1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]


def generate_board2():
    """
    パターン2のボードを返す
    """
    return [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, 1, 0, 0, 0],
        [0, 0, -1, -1, -1, -1, 0, 0],
        [0, -1, 1, -1, -1, -1, 0, 0],
        [0, 0, -1, 1, -1, -1, 0, 0],
        [0, 0, -1, -1, 1, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]


def generate_board3():
    return [
        [0, -1, -1, -1, 0, 0, 0, 0],
        [0, 0, -1, -1, -1, -1, -1, 0],
        [0, -1, 1, -1, -1, -1, -1, 0],
        [-1, -1, 1, -1, -1, -1, -1, 0],
        [0, -1, 1, -1, -1, -1, -1, 0],
        [0, -1, 1, -1, -1, 0, 0, 0],
        [-1, 1, 1, -1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0],
    ]


def generate_board4():
    """
    初期状態のボードを返す
    """
    return [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, 1, 1, 0, 0],
        [0, 0, 0, 1, -1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]


def generate_inactive_board1():
    """
    最弱モードのテストで使用するボード1
    すべての石をひっくり返される手しかない
    """
    return [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, -1, 1, -1, 0, 0],
        [0, 0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]


def generate_inactive_board2():
    """
    最弱モードのテストで使用するボード2
    """
    return [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, 0, -1, -1, 1, 0],
        [0, 0, 0, 0, -1, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]


def generate_evaluate_board1():
    """
    パターン１のボードを返す
    """
    return [
        [1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, 1, 0, 0, 0],
        [0, 0, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
