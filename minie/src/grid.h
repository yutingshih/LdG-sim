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

#endif // GRID_H