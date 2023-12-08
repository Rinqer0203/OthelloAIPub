#ifndef _OTHELLO_LOGIC_H_
#define _OTHELLO_LOGIC_H_

#define BOARD_SIZE 8
#define MAX_MOVES 60

typedef struct
{
    int x;
    int y;
} Vec2;

int getMoves(int board[][BOARD_SIZE], Vec2 moves[MAX_MOVES]);
void PrintBoard(int board[][BOARD_SIZE]);
void PrintMoves(int moves[][2], int movesLength);
void PrintMoves2(Vec2 moves[MAX_MOVES], int movesLength);

#endif