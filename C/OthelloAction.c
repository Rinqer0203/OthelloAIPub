#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <float.h>
#include <math.h>
#include "OthelloLogic.h"
#include "ActiveEvaluate.h"

float minLevel(int board[][BOARD_SIZE], int limit, int player, float alpha, float beta);
float maxLevel(int board[][BOARD_SIZE], int limit, int player, float alpha, float beta);
void copyBoard(int src[][BOARD_SIZE], int dest[][BOARD_SIZE]);

int evalCnt = 0;

// pythonから呼び出されるgetMoves関数
int (*getMovesC(int board[][BOARD_SIZE], int player))[2]
{
    static int staticMoves[MAX_MOVES + 1][2]; // +1 to include the end marker
    Vec2 moves[MAX_MOVES];
    int movesLength = getMoves(board, moves, player);

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

// pythonから呼び出されるミニマックス法のminLevelラッパー関数
float minLevelWrapper(int board[][BOARD_SIZE], int limit, int player)
{
    evalCnt = 0;
    return minLevel(board, limit, player, -FLT_MAX, FLT_MAX);
}

//--------------------------------------------------

void copyBoard(int src[][BOARD_SIZE], int dest[][BOARD_SIZE])
{
    for (int y = 0; y < BOARD_SIZE; y++)
        memcpy(dest[y], src[y], sizeof(int) * BOARD_SIZE);
}

float minLevel(int board[][BOARD_SIZE], int limit, int player, float alpha, float beta)
{
    Vec2 moves[MAX_MOVES];
    int moveLen = getMoves(board, moves, player);

    if (limit == 0 || moveLen == 0)
        return evaluateBoard(board);

    float minValue = FLT_MAX;
    for (int i = 0; i < moveLen; i++)
    {
        Vec2 move = moves[i];
        int nextBoard[BOARD_SIZE][BOARD_SIZE];
        copyBoard(board, nextBoard);
        execute(nextBoard, move, player);

        float value = maxLevel(nextBoard, limit - 1, -player, alpha, beta);
        minValue = fmin(minValue, value);

        beta = fmin(beta, value);
        if (beta <= alpha)
            break; // アルファベータ枝刈り
    }

    return minValue;
}

float maxLevel(int board[][BOARD_SIZE], int limit, int player, float alpha, float beta)
{
    Vec2 moves[MAX_MOVES];
    int moveLen = getMoves(board, moves, player);

    if (limit == 0 || moveLen == 0)
        return evaluateBoard(board);

    float maxValue = -FLT_MAX;
    for (int i = 0; i < moveLen; i++)
    {
        Vec2 move = moves[i];
        int nextBoard[BOARD_SIZE][BOARD_SIZE];
        copyBoard(board, nextBoard);
        execute(nextBoard, move, player);

        float value = minLevel(nextBoard, limit - 1, -player, alpha, beta);
        maxValue = fmax(maxValue, value);

        alpha = fmax(alpha, value);
        if (beta <= alpha)
            break; // アルファベータ枝刈り
    }

    return maxValue;
}