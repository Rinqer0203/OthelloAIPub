import OthelloAction
import OthelloLogic
import TestBoardProvider


def __Test(board, testName):
    print(f"------ {testName} ------")
    OthelloLogic.printBoard(board)
    moves = OthelloLogic.getMoves(board, 1, 8)
    resultMove = OthelloAction.getAction(board, moves)
    print(f"resultMove: {resultMove}")
    OthelloLogic.execute(board, resultMove, 1, 8)
    OthelloLogic.printBoard(board)
    print("\n")


if __name__ == "__main__":
    __Test(TestBoardProvider.generate_initial_board(), "initial board test")
    # __Test(TestBoardProvider.generate_board1(), "board1 test")
    # __Test(TestBoardProvider.generate_board2(), "board1 test")
    # __Test(TestBoardProvider.generate_inactive_board1(), "inactive board1 test")
    # __Test(TestBoardProvider.generate_inactive_board2(), "generate_inactive_board2")
    # __Test(TestBoardProvider.generate_board3(), "generate_board3")
