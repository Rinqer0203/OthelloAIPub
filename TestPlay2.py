import OthelloAction
import OthelloLogic
import TestBoardProvider
import random

if __name__ == "__main__":
    board = TestBoardProvider.generate_initial_board()
    player = 1
    turnCnt = 1

    while True:
        print(f"--------turn {turnCnt}--------")
        turnCnt += 1

        moves = OthelloLogic.getMoves(board, player, 8)

        if len(moves) == 0:
            if len(OthelloLogic.getMoves(board, player * -1, 8)) == 0:
                print("終了")
                break
            else:
                print(f"player {player}のパス")
                player *= -1
                continue

        if player == 1:
            action = OthelloAction.getAction(
                board, OthelloLogic.getMoves(board, player, 8)
            )
        else:
            action = moves[random.randrange(len(moves))]
            print(f"ランダムで手を決定 : {action}")

        board = OthelloLogic.execute(board, action, player, 8)
        player *= -1
        OthelloLogic.printBoard(board)

    playerOneStoneCnt = playerMinusStoneCnt = 0

    for y in range(8):
        for x in range(8):
            if board[y][x] == 1:
                playerOneStoneCnt += 1
            elif board[y][x] == -1:
                playerMinusStoneCnt += 1
    if playerOneStoneCnt > playerMinusStoneCnt:
        print("player 1の勝ち")
    elif playerOneStoneCnt < playerMinusStoneCnt:
        print("player -1の勝ち")
    else:
        print("引き分け")
