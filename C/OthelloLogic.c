#include "OthelloLogic.h"
#include <stdio.h>
#include <stdbool.h>

const Vec2 DIRS[8] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};

bool executeFlip(int board[][BOARD_SIZE], int player, int x, int y, Vec2 dir)
{
    if (x + dir.x < 0 || x + dir.x >= BOARD_SIZE || y + dir.y < 0 || y + dir.y >= BOARD_SIZE)
    {
        return false;
    }

    if (board[x + dir.x][y + dir.y] == -player)
    {
        int tempX = x + dir.x;
        int tempY = y + dir.y;

        while (true)
        {
            tempX += dir.x;
            tempY += dir.y;

            if (tempX < 0 || tempX >= BOARD_SIZE || tempY < 0 || tempY >= BOARD_SIZE)
            {
                return false;
            }

            if (board[tempX][tempY] == player)
            {
                // Flip the pieces
                while (tempX != x || tempY != y)
                {
                    tempX -= dir.x;
                    tempY -= dir.y;
                    board[tempX][tempY] = player;
                }
                return true;
            }
            else if (board[tempX][tempY] == 0)
            {
                return false;
            }
        }
    }

    return false;
}

void execute(int board[][BOARD_SIZE], Vec2 action, int player)
{
    board[action.x][action.y] = player;

    for (int i = 0; i < 8; i++)
    {
        executeFlip(board, player, action.x, action.y, DIRS[i]);
    }
}

bool search(int board[][BOARD_SIZE], Vec2 putCell, Vec2 dir, int player, Vec2 *result)
{
    Vec2 nextCell = {putCell.x + dir.x, putCell.y + dir.y};

    // 次のセルが範囲外か、空でない場合は0を返す
    if (nextCell.x < 0 || nextCell.x >= BOARD_SIZE ||
        nextCell.y < 0 || nextCell.y >= BOARD_SIZE ||
        board[nextCell.x][nextCell.y] != 0)
        return false;

    Vec2 reverseDir = {-dir.x, -dir.y};
    Vec2 current = {putCell.x + reverseDir.x, putCell.y + reverseDir.y};

    while (current.x >= 0 && current.x < BOARD_SIZE &&
           current.y >= 0 && current.y < BOARD_SIZE)
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

int getMoves(int board[][BOARD_SIZE], Vec2 moves[MAX_MOVES])
{
    int movesCount = 0;

    for (int y = 0; y < BOARD_SIZE; y++)
    {
        for (int x = 0; x < BOARD_SIZE; x++)
        {
            // 相手プレイヤーの駒は-1と仮定
            if (board[x][y] != -1)
                continue;

            for (int i = 0; i < 8; i++)
            {
                Vec2 result;
                if (!search(board, (Vec2){x, y}, DIRS[i], 1, &result))
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
                if (movesCount >= MAX_MOVES)
                    return movesCount;
            }
        }
    }

    return movesCount;
}

void PrintBoard(int board[][BOARD_SIZE])
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