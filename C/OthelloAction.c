#include <stdio.h>
#include <stdbool.h>
#include "OthelloLogic.h"

static int result[2];

void convertIntMovesToVec2(int src[][2], Vec2 dest[], int movesLength)
{
    for (int i = 0; i < movesLength; i++)
    {
        dest[i].x = src[i][0];
        dest[i].y = src[i][1];
    }
}

void assertMoves(int board[][BOARD_SIZE], int moves[][2], int movesLength)
{
    Vec2 moves2[MAX_MOVES];
    int moves2Length = getMoves(board, moves2);

    // movesとmoves2の長さが一致するか
    if (movesLength == moves2Length)
    {
        // 中身が一致するか
        for (int i = 0; i < movesLength; i++)
        {
            if (moves[i][0] != moves2[i].x || moves[i][1] != moves2[i].y)
            {
                printf("GetMovesの結果が一致しない\n");
            }
        }
    }
    else
    {
        printf("GetMovesの結果が一致しない\n");
    }
}

int *Action(int board[][BOARD_SIZE], int moves[][2], int movesLength)
{
    printf("%d\n", movesLength);
    PrintBoard(board);
    assertMoves(board, moves, movesLength);

    // 配列を初期化
    result[0] = 4;
    result[1] = 5;
    return result;
}

int (*getMovesC(int board[][BOARD_SIZE]))[2]
{
    static int staticMoves[MAX_MOVES + 1][2]; // +1 to include the end marker
    Vec2 moves[MAX_MOVES];
    int movesLength = getMoves(board, moves);

    for (int i = 0; i < movesLength; i++)
    {
        staticMoves[i][0] = moves[i].x;
        staticMoves[i][1] = moves[i].y;
    }

    // 終端マーカーとして{-1, -1}を追加
    staticMoves[movesLength][0] = -1;
    staticMoves[movesLength][1] = -1;

    return staticMoves;
}
