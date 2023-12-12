#include "OthelloLogic.h"
#include "ActiveEvaluate.h"
#include <stdio.h>
#include <stdbool.h>

const int baseBoardPoint[BOARD_SIZE][BOARD_SIZE] = {
    {30, -12, 0, -1, -1, 0, -12, 30},
    {-12, -15, -3, -3, -3, -3, -15, -12},
    {0, -3, 0, -1, -1, 0, -3, 0},
    {-1, -3, -1, -1, -1, -1, -3, -1},
    {-1, -3, -1, -1, -1, -1, -3, -1},
    {0, -3, 0, -1, -1, 0, -3, 0},
    {-12, -15, -3, -3, -3, -3, -15, -12},
    {30, -12, 0, -1, -1, 0, -12, 30}};

const Vec2 leftUpAround[3] = {{0, 1}, {1, 0}, {1, 1}};
const Vec2 rightUpAround[3] = {{0, 6}, {1, 6}, {1, 7}};
const Vec2 leftDownAround[3] = {{6, 0}, {6, 1}, {7, 1}};
const Vec2 rightDownAround[3] = {{6, 6}, {6, 7}, {7, 6}};

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

float evaluateStoneCount(int board[BOARD_SIZE][BOARD_SIZE])
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
    return (float)(playerStones - enemyStones) / (playerStones + enemyStones) * 5;
}

float evaluateBase(int board[BOARD_SIZE][BOARD_SIZE])
{
    int playerScore = 0, enemyScore = 0;

    for (int x = 0; x < BOARD_SIZE; x++)
    {
        for (int y = 0; y < BOARD_SIZE; y++)
        {
            if (board[x][y] == 1)
            {
                int score = isSpecialCornerAround(x, y, board, 1) ? 0 : baseBoardPoint[x][y];
                playerScore += score;
            }
            else if (board[x][y] == -1)
            {
                int score = isSpecialCornerAround(x, y, board, -1) ? 0 : baseBoardPoint[x][y];
                enemyScore += score;
            }
        }
    }
    return (float)(playerScore - enemyScore);
}

float evaluateBoard(int board[][BOARD_SIZE])
{
    // evalCnt++;
    float stoneCount = evaluateStoneCount(board);
    float base = evaluateBase(board);
    return (stoneCount + base);
}