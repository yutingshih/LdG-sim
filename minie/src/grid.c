#include "grid.h"

grid* new_grid(int x, int y, int z, type t)
{
    assert(&x != NULL);
    assert(&y != NULL);
    assert(&z != NULL);
    assert((t == BULK) || (t == UNI) | (t == DEG));

    grid* self = malloc(sizeof(grid));
    if (!self) return self;

    self->x = x;
    self->y = y;
    self->z = z;
    self->t = t;
    self->Q = new_matrix(3, 3);
    self->h = new_matrix(3, 3);

    if (!(self->Q) || !(self->h)) {
        if (!(self->Q)) {
            free_matrix(self->Q);
            self->Q = NULL;
        }
        if (!(self->h)) {
            free_matrix(self->h);
            self->h = NULL;
        }
        free(self);
        self = NULL;
        return self;
    }

    return self;
}

void free_grid(void* self)
{
    if (!self) return;

    matrix* ptr;
    
    ptr = ((grid*)self)->Q;
    if (ptr) free(ptr);

    ptr = ((grid*)self)->h;
    if (ptr) free(ptr);

    free(self);
}

int get_x(const grid* self)
{
    assert(self);
    return self->x;
}

int get_y(const grid* self)
{
    assert(self);
    return self->y;
}

int get_z(const grid* self)
{
    assert(self);
    return self->z;
}

char get_type(const grid* self)
{
    assert(self);
    return self->t;
}

matrix* get_Q(const grid* self)
{
    assert(self);
    return self->Q;
}

matrix* get_h(const grid* self)
{
    assert(self);
    return self->h;
}
