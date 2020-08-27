#include "grid.h"

grid* new_grid(int x, int y, int z, char tag)
{
    assert(&x != NULL);
    assert(&y != NULL   );
    assert(&z != NULL);
    assert(tag);

    grid* self = malloc(sizeof(grid));
    if(!self) return self;

    self->x = x;
    self->y = y;
    self->z = z;
    self->tag = tag;
    self->Q = new_matrix(3, 3);
    self->h = new_matrix(3, 3);

    if (!(self->Q) || !(self->h)) {
        (self->Q) ? free(self->Q) : free(self->h);
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

char get_tag(const grid* self)
{
    assert(self);
    return self->tag;
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