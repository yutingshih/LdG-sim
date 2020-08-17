#ifndef GRID_H
#define GRID_H

#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>
#include "matrix.h"

struct grid {
    int x;
    int y;
    int z;
    char tag;
    matrix* Q;
    matrix* h;
};

typedef struct grid grid;

grid* new_grid(int x, int y, int z, char tag);
void free_grid(void* self);

int get_x(const grid* self);
int get_y(const grid* self);
int get_z(const grid* self);
char get_tag(const grid* self);
matrix* get_Q(const grid* self);
matrix* get_h(const grid* self);



#endif // GRID_H