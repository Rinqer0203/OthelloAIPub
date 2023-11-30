
def evaluate_board(board, player) -> float:
    evaluate_point = 0
    for func in evalute_funcs:
        evaluate_point += func.evaluate(board, player)
    return evaluate_point