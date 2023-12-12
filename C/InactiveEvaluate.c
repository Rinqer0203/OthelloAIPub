#include "OthelloLogic.h"
#include "InactiveEvaluate.h"
#include <stdio.h>
#include <stdbool.h>

// ------基本的な石の評価------

// baseBoardPointは中心に近いほど高い点数がつく
const int baseBoardPoint2[BOARD_SIZE][BOARD_SIZE] = {
    {10, -5, 2, 2, 2, 2, -5, 10},
    {-5, -5, 3, 3, 3, 3, -5, -5},
    {2, 3, 4, 4, 4, 4, 3, 2},
    {2, 3, 4, 5, 5, 4, 3, 2},
    {2, 3, 4, 5, 5, 4, 3, 2},
    {2, 3, 4, 4, 4, 4, 3, 2},
    {-5, -5, 3, 3, 3, 3, -5, -5},
    {10, -5, 2, 2, 2, 2, -5, 10},
};

bool isSpecialCornerAround2(int x, int y, int board[BOARD_SIZE][BOARD_SIZE], int player)
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

float evaluateBase2(int board[BOARD_SIZE][BOARD_SIZE])
{
    int playerScore = 0, enemyScore = 0;

    for (int x = 0; x < BOARD_SIZE; x++)
    {
        for (int y = 0; y < BOARD_SIZE; y++)
        {
            if (board[x][y] == 1)
            {
                int score = isSpecialCornerAround2(x, y, board, 1) ? 0 : baseBoardPoint2[x][y];
                playerScore += score;
            }
            else if (board[x][y] == -1)
            {
                int score = isSpecialCornerAround2(x, y, board, -1) ? 0 : baseBoardPoint2[x][y];
                enemyScore += score;
            }
        }
    }
    return (float)(playerScore - enemyScore);
}

// ------石の数の評価------

float evaluateStoneCount2(int board[BOARD_SIZE][BOARD_SIZE])
{
    int playerStones = 0, enemyStones = 0;

    for (int x = 0; x < BOARD_SIZE; x++)
    {
        for (int y = 0; y < BOARD_SIZE; y++)
        {
            if (board[x][y] == 1)
            {
                playerStones++;
            }
            else if (board[x][y] == -1)
            {
                enemyStones++;
            }
        }
    }
    if (playerStones + enemyStones == 0)
        return 0.0f;

    float normalizedDiff = (float)(playerStones - enemyStones) / (playerStones + enemyStones) * 5;
    return normalizedDiff;
}

// ------確定石の評価------

int countInDirection2(int board[BOARD_SIZE][BOARD_SIZE], int player, int startX, int startY, int deltaX, int deltaY)
{
    int count = 0;
    int x = startX;
    int y = startY;

    while (x >= 0 && x < BOARD_SIZE && y >= 0 && y < BOARD_SIZE && board[x][y] == player)
    {
        count++;
        x += deltaX;
        y += deltaY;
    }

    if (count > 0)
        return count - 1;
    return 0;
}

int countConfirmedStonesFromCorner2(int board[BOARD_SIZE][BOARD_SIZE], int player, int cornerX, int cornerY)
{
    int confirmed = 0;

    confirmed += board[cornerX][cornerY] == player ? 1 : 0;
    // 水平方向
    confirmed += countInDirection2(board, player, cornerX, cornerY, (cornerX == 0) ? 1 : -1, 0);
    // 垂直方向
    confirmed += countInDirection2(board, player, cornerX, cornerY, 0, (cornerY == 0) ? 1 : -1);
    // 対角線方向
    confirmed += countInDirection2(board, player, cornerX, cornerY, (cornerX == 0) ? 1 : -1, (cornerY == 0) ? 1 : -1);

    return confirmed;
}

int countConfirmedStones2(int board[BOARD_SIZE][BOARD_SIZE], int player)
{
    int evalConfirmedStones = 0;

    // 4つの角から確定石を数える
    evalConfirmedStones += countConfirmedStonesFromCorner2(board, player, 0, 0);                           // 左上
    evalConfirmedStones += countConfirmedStonesFromCorner2(board, player, BOARD_SIZE - 1, 0);              // 右上
    evalConfirmedStones += countConfirmedStonesFromCorner2(board, player, 0, BOARD_SIZE - 1);              // 左下
    evalConfirmedStones += countConfirmedStonesFromCorner2(board, player, BOARD_SIZE - 1, BOARD_SIZE - 1); // 右下

    return evalConfirmedStones;
}

// ------盤面の評価------

float evaluateBoardInactive(int board[][BOARD_SIZE])
{
    Vec2 enemyMoves[MAX_MOVES];
    Vec2 playerMoves[MAX_MOVES];
    int enemyMovesLen = getMoves(board, enemyMoves, -1);
    int playerMovesLen = getMoves(board, playerMoves, 1);

    // 石の数の評価
    // float evalStoneCount = -evaluateStoneCount2(board);
    // 基本的な石の評価
    // float evalBase = evaluateBase2(board);
    // 確定石の評価
    // float evalConfirmedStones = countConfirmedStones2(board, 1) - countConfirmedStones2(board, -1);
    // 手数の評価
    // float evalMoves = (float)(playerMovesLen - enemyMovesLen);
    // return (evalStoneCount + evalBase + evalConfirmedStones + evalMoves);

    float evalMoves = (float)(playerMovesLen - enemyMovesLen);
    return evalMoves;
}