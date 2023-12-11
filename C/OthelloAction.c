#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <float.h>
#include <math.h>
#include "OthelloLogic.h"

static int result[2];

float minLevel(int board[][BOARD_SIZE], int limit, int player, float alpha, float beta);
float maxLevel(int board[][BOARD_SIZE], int limit, int player, float alpha, float beta);
float evaluateBoard(int board[][BOARD_SIZE], int player);
bool isSpecialCornerAround(int x, int y, int board[BOARD_SIZE][BOARD_SIZE], int player);
float evaluateStoneCount(int board[BOARD_SIZE][BOARD_SIZE], int player);
float evaluateBase(int board[BOARD_SIZE][BOARD_SIZE], int player);
void copyBoard(int src[][BOARD_SIZE], int dest[][BOARD_SIZE]);

void convertIntMovesToVec2(int src[][2], Vec2 dest[], int movesLength)
{
    for (int i = 0; i < movesLength; i++)
    {
        dest[i].x = src[i][0];
        dest[i].y = src[i][1];
    }
}

int *Action(int board[][BOARD_SIZE], int moves[][2], int movesLength)
{
    printf("%d\n", movesLength);
    PrintBoard(board);

    // 配列を初期化
    result[0] = 4;
    result[1] = 5;
    return result;
}

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

int evalCnt = 0;

float evaluate(int board[][BOARD_SIZE], int player, int limit)
{
    evalCnt = 0;
    Vec2 moves[MAX_MOVES];
    int moveLen = getMoves(board, moves, player);

    if (moveLen == 0)
        return evaluateBoard(board, player);

    float alpha = -FLT_MAX;
    float beta = FLT_MAX;
    float maxValue = -FLT_MAX;

    for (int i = 0; i < moveLen; i++)
    {
        Vec2 move = moves[i];
        int nextBoard[BOARD_SIZE][BOARD_SIZE];
        copyBoard(board, nextBoard);
        execute(nextBoard, move, player);
        // printf("move %d %d : nextBoard\n", move.x, move.y);
        // PrintBoard(nextBoard);

        float value = minLevel(nextBoard, limit - 1, -player, alpha, beta);
        maxValue = fmax(maxValue, value);

        // alpha = fmax(alpha, value);
        // if (beta <= alpha)
        //     break; // アルファベータ枝刈り
    }

    printf("evalCnt: %d\n", evalCnt);
    return maxValue;
}

//--------------------------------------------------

float evaluateBoard(int board[][BOARD_SIZE], int player)
{
    evalCnt++;
    float stoneCount = evaluateStoneCount(board, player);
    float base = evaluateBase(board, player);
    return (stoneCount + base) * player;
}

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
        return evaluateBoard(board, player);

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
        return evaluateBoard(board, player);

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

int baseBoardPoint[BOARD_SIZE][BOARD_SIZE] = {
    {30, -12, 0, -1, -1, 0, -12, 30},
    {-12, -15, -3, -3, -3, -3, -15, -12},
    {0, -3, 0, -1, -1, 0, -3, 0},
    {-1, -3, -1, -1, -1, -1, -3, -1},
    {-1, -3, -1, -1, -1, -1, -3, -1},
    {0, -3, 0, -1, -1, 0, -3, 0},
    {-12, -15, -3, -3, -3, -3, -15, -12},
    {30, -12, 0, -1, -1, 0, -12, 30}};

Vec2 leftUpAround[3] = {{0, 1}, {1, 0}, {1, 1}};
Vec2 rightUpAround[3] = {{0, 6}, {1, 6}, {1, 7}};
Vec2 leftDownAround[3] = {{6, 0}, {6, 1}, {7, 1}};
Vec2 rightDownAround[3] = {{6, 6}, {6, 7}, {7, 6}};

bool isSpecialCornerAround(int x, int y, int board[BOARD_SIZE][BOARD_SIZE], int player)
{
    for (int i = 0; i < 3; i++)
    {
        if ((x == leftUpAround[i].x && y == leftUpAround[i].y && board[0][0] == player) ||
            (x == rightUpAround[i].x && y == rightUpAround[i].y && board[0][7] == player) ||
            (x == leftDownAround[i].x && y == leftDownAround[i].y && board[7][0] == player) ||
            (x == rightDownAround[i].x && y == rightDownAround[i].y && board[7][7] == player))
        {
            return true;
        }
    }

    return false;
}

float evaluateStoneCount(int board[BOARD_SIZE][BOARD_SIZE], int player)
{
    int playerStones = 0, enemyStones = 0;

    for (int x = 0; x < BOARD_SIZE; x++)
    {
        for (int y = 0; y < BOARD_SIZE; y++)
        {
            if (board[x][y] == player)
            {
                playerStones++;
            }
            else if (board[x][y] == -player)
            {
                enemyStones++;
            }
        }
    }
    if (playerStones + enemyStones == 0)
        return 0.0f;
    return (float)(playerStones - enemyStones) / (playerStones + enemyStones) * 5;
}

float evaluateBase(int board[BOARD_SIZE][BOARD_SIZE], int player)
{
    int playerScore = 0, enemyScore = 0;

    for (int x = 0; x < BOARD_SIZE; x++)
    {
        for (int y = 0; y < BOARD_SIZE; y++)
        {
            if (board[x][y] == player)
            {
                int score = isSpecialCornerAround(x, y, board, player) ? 0 : baseBoardPoint[x][y];
                playerScore += score;
            }
            else if (board[x][y] == -player)
            {
                int score = isSpecialCornerAround(x, y, board, -player) ? 0 : baseBoardPoint[x][y];
                enemyScore += score;
            }
        }
    }
    return (float)(playerScore - enemyScore);
}
