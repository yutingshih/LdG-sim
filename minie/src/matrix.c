#include "matrix.h"

matrix* new_matrix(size_t row, size_t col)
{
    assert(row > 0);
    assert(col > 0);

    matrix* self = malloc(sizeof(matrix));
    if (!self) return self;

    self->row = row;
    self->col = col;
    self->elements = calloc(row * col, sizeof(double));

    if (!(self->elements)) {
        free(self);
        self = NULL;
        return self;
    }

    return self;
}

matrix* init_matrix(matrix* self, double value, ...)
{
    va_list ap;
    va_start(ap, value);

    self->elements[0] = value;
    for (int i = 1; i < self->row * self->col; i++)
        self->elements[i] = va_arg(ap, double);

    va_end(ap);
    return self;
}

void free_matrix(void* self)
{
    if (!self) return;

    double* elements = ((matrix*)self)->elements;
    
    if (elements) free(elements);
    
    free(self);
}

size_t get_row(const matrix* self)
{
    assert(self);
    return self->row;
}

size_t get_col(const matrix* self)
{
    assert(self);
    return self->col;
}

double get_item(const matrix* self, size_t row, size_t col)
{
    assert(row < get_row(self));
    assert(col < get_col(self));
    return self->elements[row * get_col(self) + col];
}

double get_elem(const matrix* self, size_t index)
{
    assert(index < get_row(self) * get_col(self));
    return self->elements[index];
}

void set_item(matrix* self, size_t row, size_t col, double value)
{
    assert(row < get_row(self));
    assert(col < get_col(self));
    self->elements[row * get_col(self) + col] = value;
}

void set_elem(matrix* self, size_t index, double value)
{
    assert(index < get_row(self) * get_col(self));
    self->elements[index] = value;
}

bool equal(const matrix* m, const matrix* n)
{
    if (get_row(m) != get_col(n)) return false;
    if (get_col(m) != get_col(n)) return false;

    for (size_t i = 0; i < get_row(m); i++)
        for (size_t j = 0; j < get_col(m); j++)
            if (fabs(get_item(m, i, j)) - get_item(n, i, j) > EQUAL_TH)
                return false;

    return true;
}

bool symmetric(const matrix* self)
{
    if (get_row(self) != get_col(self)) return false;

    for (size_t i = 0; i < get_row(self); i++)
        for (size_t j = get_col(self); j > i; j--)
            if (fabs(get_item(self, i, j) - get_item(self, j, i)) > EQUAL_TH)
                return false;

    return true;
}

bool traceless(const matrix* self)
{
    if (get_row(self) == get_col(self)) return false;

    double temp = 0.0;
    for (size_t i = 0; i < get_row(self); i++)
        temp += get_item(self, i, i);

    if (fabs(temp) > EQUAL_TH) return false;

    return true;
}

double trace(const matrix* self)
{
    assert(get_row(self) == get_col(self));
    double temp = 0.0;
    for (size_t i = 0; i < get_row(self); i++)
        temp += get_item(self, i, i);
    return temp;
}

double sum_m(const matrix* self)
{
    assert(self);
    double sum = *self->elements;
    for (size_t i = 1; i < get_row(self) * get_col(self); i++)
        sum += self->elements[i];
    return sum;
}

void add_m(matrix* self, const matrix* m)
{
    assert(get_row(self) == get_row(m));
    assert(get_col(self) == get_col(m));
    for (size_t i = 0; i < get_row(self) * get_col(self); i++)
        self->elements[i] += m->elements[i];
}

void add_s(matrix* self, double s)
{
    for (size_t i = 0; i < get_row(self) * get_col(self); i++)
        self->elements[i] += s;
}

void mul_m(matrix* self, const matrix* m)
{
    assert(get_row(self) == get_row(m));
    assert(get_col(self) == get_col(m));
    for (size_t i = 0; i < get_row(self) * get_col(self); i++)
        self->elements[i] *= m->elements[i];
}

void mul_s(matrix* self, double s)
{
    for (size_t i = 0; i < get_row(self) * get_col(self); i++)
        self->elements[i] *= s;
}

matrix* trans(const matrix* m)
{
    matrix* out = new_matrix(get_col(m), get_row(m));
    if (!out) return out;

    for (size_t i = 0; i < get_row(m); i++)
        for (size_t j = 0; j < get_col(m); j++)
            set_item(out, j, i, get_item(m, i, j));

    return out;
}

matrix* add_mm(const matrix* m, const matrix* n)
{
    assert(get_row(m) == get_row(n));
    assert(get_col(m) == get_col(n));

    matrix* out = new_matrix(get_col(m), get_row(m));
    if (!out) return out;

    for (size_t i = 0; i < get_row(m); i++)
        for (size_t j = 0; j < get_col(m); j++)
            set_item(out, i, j, get_item(m, i, j) + get_item(n, i, j));

    return out;
}

matrix* add_ms(const matrix* m, double s)
{
    matrix* out = new_matrix(get_col(m), get_row(m));
    if (!out) return out;

    for (size_t i = 0; i < get_row(m); i++)
        for (size_t j = 0; j < get_col(m); j++)
            set_item(out, i, j, get_item(m, i, j) + s);

    return out;
}

matrix* add_sm(double s, const matrix* m)
{
    return add_ms(m, s);
}

matrix* mul_mm(const matrix* m, const matrix* n)
{
    assert(get_row(m) == get_row(n));
    assert(get_col(m) == get_col(n));

    matrix* out = new_matrix(get_col(m), get_row(m));
    if (!out) return out;

    for (size_t i = 0; i < get_row(m); i++)
        for (size_t j = 0; j < get_col(m); j++)
            set_item(out, i, j, get_item(m, i, j) * get_item(n, i, j));

    return out;
}

matrix* mul_ms(const matrix* m, double s)
{
    matrix* out = new_matrix(get_col(m), get_row(m));
    if (!out) return out;

    for (size_t i = 0; i < get_row(m); i++)
        for (size_t j = 0; j < get_col(m); j++)
            set_item(out, i, j, get_item(m, i, j) * s);

    return out;
}

matrix* mul_sm(double s, const matrix* m)
{
    return mul_ms(m, s);
}

matrix* dot_mm(const matrix* m, const matrix* n)
{
    assert(get_col(m) == get_row(n));

    matrix* out = new_matrix(get_row(m), get_col(n));
    if (!out) return out;

    double temp;
    for (size_t i = 0; i < get_row(m); i++) {
        for (size_t j = 0; j < get_col(n); j++) {
            temp = 0.0f;
            for (size_t k = 0; k < get_col(m); k++) {
                temp += get_item(m, i, k) * get_item(n, k, j);
            }
            set_item(out, i, j, temp);
        }
    }

    return out;
}

matrix* diagonal(size_t size ,double value)
{
    matrix* diag = new_matrix(size, size);
    for (int i = 0; i < size; i++)
        set_item(diag, i, i, value);
    return diag;
}

matrix* laplacian(const matrix* self, int count, ...)
{
    matrix* lapQ = new_matrix(get_row(self), get_col(self));
    va_list ap;
    va_start(ap, count);

    for (int i = 0; i < count; i++)
        add_m(lapQ, va_arg(ap, matrix*));
    mul_s(lapQ, 1.0 / (double)count);
    add_m(lapQ, mul_ms(self, -1.0));

    va_end(ap);
    return lapQ;
}

void print(matrix* mtx, char* prompt)
{
    printf("%s", prompt);
    for (int i = 0; i < get_row(mtx); i++) {
        for (int j = 0; j < get_col(mtx); j++) {
            printf("%6.2f ", get_item(mtx, i, j));
        }
        printf("\n");
    }
}