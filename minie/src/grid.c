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

void molefield(grid* self, const param* prm, 
               const matrix* top, const matrix* bottom,
               const matrix* left, const matrix* right,
               const matrix* front, const matrix* back, 
               const matrix* Qbound, const matrix* normal)
{

    matrix* lapQ = new_matrix(3, 3);
    matrix* gradQx_nx = new_matrix(3, 3);
    matrix* gradQy_ny = new_matrix(3, 3);
    matrix* gradQz_nz = new_matrix(3, 3);

    for (int i = 0; i < 9; i++) {
        set_elem(lapQ, i, (get_elem(top, i) + get_elem(bottom, i)
                         + get_elem(left, i) + get_elem(right, i)
                         + get_elem(front, i) + get_elem(back, i)) / 6.0 - get_elem(self->Q, i));
        set_elem(gradQz_nz, i, (get_elem(top, i) - get_elem(bottom, i)) / (2 * prm->dz) * get_elem(normal, 2));
        set_elem(gradQy_ny, i, (get_elem(left, i) - get_elem(right, i)) / (2 * prm->dy) * get_elem(normal, 1));
        set_elem(gradQx_nx, i, (get_elem(front, i) - get_elem(back, i)) / (2 * prm->dx) * get_elem(normal, 0));
    }

    matrix* inner = dot_mm(self->Q, self->Q);
    double coeff = sum_m(mul_mm(self->Q, trans(self->Q)));

    switch (self->t) {
        case BULK:
            for (int i = 0; i < 9; i++) {
                set_elem(self->h, i, (prm->L * get_elem(lapQ, i))
                                   - (prm->A * get_elem(self->Q, i))
                                   - (prm->B * get_elem(inner, i))
                                   - (prm->C * get_elem(self->Q, i)) * coeff);
            }
            break;
        
        case UNI:
            for (int i = 0; i < 9; i++) {
                set_elem(self->h, i,
                    prm->L * (get_elem(gradQx_nx, i) + get_elem(gradQy_ny, i) + get_elem(gradQz_nz, i))
                  + prm->W_uni * (get_elem(self->Q, i) - get_elem(Qbound, i)));
            }
            break;
        
        case DEG:
            for (int i = 0; i < 9; i++) {
                set_elem(self->h, i,
                    prm->L * (get_elem(gradQx_nx, i) + get_elem(gradQy_ny, i) + get_elem(gradQz_nz, i))
                  + prm->W_deg * (get_elem(self->Q, i) - get_elem(Qbound, i)));
            }
            break;
    }

    free_matrix(lapQ);
    free_matrix(gradQx_nx);
    free_matrix(gradQy_ny);
    free_matrix(gradQz_nz);
}

void evolute(grid* self, const param* prm)
{
    add_m(self->Q, mul_sm(prm->dt / prm->gamma, self->h));
}