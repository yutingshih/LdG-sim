#ifndef GRID_H
#define GRID_H

#include <stdlib.h>
#include <assert.h>
#include "matrix.h"
#include "param.h"

typedef enum {BULK, UNI, DEG} type;

struct grid {
    int x;
    int y;
    int z;
    type t;
    matrix* Q;
    matrix* h;
    matrix* Qb;
};

typedef struct grid grid;

grid* new_grid(int x, int y, int z, type t);
void free_grid(void* self);

int get_x(const grid* self);
int get_y(const grid* self);
int get_z(const grid* self);
char get_type(const grid* self);
matrix* get_Q(const grid* self);
matrix* get_h(const grid* self);
matrix* get_Qb(const grid* self);

void molefield(grid* self, const param* prm, 
               const matrix* top, const matrix* bottom,
               const matrix* right, const matrix* left,
               const matrix* front, const matrix* back, 
               const matrix* bound, const matrix* normal);
void evolute(grid* self, const param* prm);

#endif // GRID_H