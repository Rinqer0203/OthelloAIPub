#include "OthelloLogic.h"
#include <stdio.h>
#include <stdbool.h>

const Vec2 DIRS[8] = {{-1, -1}, {0, -1}, {1, -1}, {-1, 0}, {1, 0}, {-1, 1}, {0, 1}, {1, 1}};

const Vec2 leftUpAround[3] = {{0, 1}, {1, 0}, {1, 1}};
const Vec2 rightUpAround[3] = {{0, 6}, {1, 6}, {1, 7}};
const Vec2 leftDownAround[3] = {{6, 0}, {6, 1}, {7, 1}};
const Vec2 rightDownAround[3] = {{6, 6}, {6, 7}, {7, 6}};

bool executeFlip(int board[][BOARD_SIZE], int player, Vec2 action, Vec2 dir)
{

    if (IS_IN_BOARD(action.x, action.y) == false)
    {
        return false;
    }

    if (board[action.y + dir.y][action.x + dir.x] == -player)
    {
        int tempX = action.x + dir.x;
        int tempY = action.y + dir.y;

        while (true)
        {
            tempX += dir.x;
            tempY += dir.y;

            if (IS_IN_BOARD(tempX, tempY) == false)
            {
                return false;
            }

            if (board[tempY][tempX] == player)
            {
                while (tempX != action.x || tempY != action.y)
                {
                    tempX -= dir.x;
                    tempY -= dir.y;
                    board[tempY][tempX] = player;
                }
                return true;
            }
            else if (board[tempY][tempX] == 0)
            {
                return false;
            }
        }
    }

    return false;
}

void execute(int board[][BOARD_SIZE], Vec2 action, int player)
{
    board[action.y][action.x] = player;

    for (int i = 0; i < 8; i++)
    {
        executeFlip(board, player, action, DIRS[i]);
    }
}

bool search(int board[][BOARD_SIZE], Vec2 putCell, Vec2 dir, int player, Vec2 *result)
{
    Vec2 nextCell = {putCell.x + dir.x, putCell.y + dir.y};

    // 次のセルが範囲外か、空でない場合は0を返す
    if (IS_IN_BOARD(nextCell.x, nextCell.y) == false ||
        board[nextCell.x][nextCell.y] != 0)
        return false;

    Vec2 reverseDir = {-dir.x, -dir.y};
    Vec2 current = {putCell.x + reverseDir.x, putCell.y + reverseDir.y};

    while (IS_IN_BOARD(current.x, current.y))
    {
        if (board[current.x][current.y] == player)
        {
            result->x = nextCell.y;
            result->y = nextCell.x;
            return true;
        }
        else if (board[current.x][current.y] == 0)
        {
            return false;
        }

        current.x += reverseDir.x;
        current.y += reverseDir.y;
    }

    return false;
}

int getMoves(int board[][BOARD_SIZE], Vec2 moves[MAX_MOVES], int player)
{
    int movesCount = 0;

    for (int y = 0; y < BOARD_SIZE; y++)
    {
        for (int x = 0; x < BOARD_SIZE; x++)
        {
            // 相手プレイヤーの駒は-1と仮定
            if (board[x][y] != -player)
                continue;

            for (int i = 0; i < 8; i++)
            {
                Vec2 result;
                if (!search(board, (Vec2){x, y}, DIRS[i], player, &result))
                    continue;

                // 既存の手が存在するかチェック
                bool alreadyExists = false;
                for (int j = 0; j < movesCount; j++)
                {
                    if (moves[j].x == result.x && moves[j].y == result.y)
                    {
                        alreadyExists = true;
                        break;
                    }
                }
                if (alreadyExists)
                    continue;

                moves[movesCount++] = result;
            }
        }
    }

    return movesCount;
}

void PrintBoard2(int board[][BOARD_SIZE])
{
    printf("board\n");
    for (int i = 0; i < BOARD_SIZE; i++)
    {
        printf("|");
        for (int j = 0; j < BOARD_SIZE; j++)
            printf("%2d|", board[i][j]);
        printf("\n");
    }
}

void PrintBoard(int board[][BOARD_SIZE])
{
    for (int y = 0; y < BOARD_SIZE; y++)
    {
        for (int x = 0; x < BOARD_SIZE; x++)
        {
            char *cell = board[y][x] == 1 ? "○ " : board[y][x] == -1 ? "● "
                                                                     : "  ";
            printf("%s", cell);
        }
        printf("\n");
    }
}

void PrintMoves(int moves[][2], int movesLength)
{
    printf("moves\n");
    for (int i = 0; i < movesLength; i++)
    {
        printf("|%d,%d|", moves[i][0], moves[i][1]);
        printf("\n");
    }
}

void PrintMoves2(Vec2 moves[MAX_MOVES], int movesLength)
{
    printf("moves2\n");
    for (int i = 0; i < movesLength; i++)
    {
        printf("|%d,%d|", moves[i].x, moves[i].y);
        printf("\n");
    }
}