#include "OthelloLogic.h"
#include "ActiveEvaluate.h"
#include <stdio.h>
#include <stdbool.h>

// ------基本的な石の評価------

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

// ------石の数の評価------

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

    float normalizedDiff = (float)(playerStones - enemyStones) / (playerStones + enemyStones) * 5;
    return normalizedDiff;
}

// ------確定石の評価------

int countInDirection(int board[BOARD_SIZE][BOARD_SIZE], int player, int startX, int startY, int deltaX, int deltaY)
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

int countConfirmedStonesFromCorner(int board[BOARD_SIZE][BOARD_SIZE], int player, int cornerX, int cornerY)
{
    int confirmed = 0;

    confirmed += board[cornerX][cornerY] == player ? 1 : 0;
    // 水平方向
    confirmed += countInDirection(board, player, cornerX, cornerY, (cornerX == 0) ? 1 : -1, 0);
    // 垂直方向
    confirmed += countInDirection(board, player, cornerX, cornerY, 0, (cornerY == 0) ? 1 : -1);
    // 対角線方向
    confirmed += countInDirection(board, player, cornerX, cornerY, (cornerX == 0) ? 1 : -1, (cornerY == 0) ? 1 : -1);

    return confirmed;
}

int countConfirmedStones(int board[BOARD_SIZE][BOARD_SIZE], int player)
{
    int evalConfirmedStones = 0;

    // 4つの角から確定石を数える
    evalConfirmedStones += countConfirmedStonesFromCorner(board, player, 0, 0);                           // 左上
    evalConfirmedStones += countConfirmedStonesFromCorner(board, player, BOARD_SIZE - 1, 0);              // 右上
    evalConfirmedStones += countConfirmedStonesFromCorner(board, player, 0, BOARD_SIZE - 1);              // 左下
    evalConfirmedStones += countConfirmedStonesFromCorner(board, player, BOARD_SIZE - 1, BOARD_SIZE - 1); // 右下

    return evalConfirmedStones;
}

// ------盤面の評価------

float evaluateBoard(int board[][BOARD_SIZE])
{
    Vec2 enemyMoves[MAX_MOVES];
    Vec2 playerMoves[MAX_MOVES];
    int enemyMovesLen = getMoves(board, enemyMoves, -1);
    int playerMovesLen = getMoves(board, playerMoves, 1);

    // 石の数の評価
    float evalStoneCount = evaluateStoneCount(board);
    // 終局時は石の数の評価を優先
    if (enemyMovesLen == 0 && playerMovesLen == 0)
        return evalStoneCount * 50;
    // 基本的な石の評価
    float evalBase = evaluateBase(board);
    // 確定石の評価
    float evalConfirmedStones = countConfirmedStones(board, 1) - countConfirmedStones(board, -1);
    // 手数の評価
    float evalMoves = (float)(playerMovesLen - enemyMovesLen);
    return (evalStoneCount + evalBase + evalConfirmedStones + evalMoves);
}