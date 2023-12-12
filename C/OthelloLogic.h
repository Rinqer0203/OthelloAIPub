#ifndef _OTHELLO_LOGIC_H_
#define _OTHELLO_LOGIC_H_

#define BOARD_SIZE 8
#define MAX_MOVES 60

#define IS_IN_BOARD(x, y) (0 <= x && x < BOARD_SIZE && 0 <= y && y < BOARD_SIZE)

typedef struct
{
    int x;
    int y;
} Vec2;

const Vec2 leftUpAround[3];
const Vec2 rightUpAround[3];
const Vec2 leftDownAround[3];
const Vec2 rightDownAround[3];

void execute(int board[][BOARD_SIZE], Vec2 move, int player);
int getMoves(int board[][BOARD_SIZE], Vec2 moves[MAX_MOVES], int player);
void PrintBoard(int board[][BOARD_SIZE]);
void PrintMoves(int moves[][2], int movesLength);
void PrintMoves2(Vec2 moves[MAX_MOVES], int movesLength);

#endif