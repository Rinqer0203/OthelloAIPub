import OthelloAction
import OthelloLogic
import EnemyOthelloAction
import TestBoardProvider
import copy
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
            action = OthelloAction.getAction(board, moves)
        else:
            # action = moves[random.randrange(len(moves))]
            action = EnemyOthelloAction.getAction(
                OthelloLogic.getReverseboard(copy.deepcopy(board)), moves
            )
            # print(f"ランダムで手を決定 : {action}")

        board = OthelloLogic.execute(board, action, player, 8)
        OthelloLogic.printBoardWithCell(board, player, [-1, -1], 8)
        player *= -1

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

    print(f"player 1の石の数: {playerOneStoneCnt}")
    print(f"player -1の石の数: {playerMinusStoneCnt}")
