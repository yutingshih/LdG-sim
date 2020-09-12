#include <stdio.h>
#include <stdlib.h>
#include "matrix.h"
#include "grid.h"
#include "param.h"

void test_matrix(void);
void test_grid(void);

#ifdef DEBUG_
int main(void)
{
    printf("\n====== Matrix Tests ======\n\n");
    test_matrix();
    printf("\n====== Grid Tests ======\n\n");
    test_grid();
    printf("\n====== Tests End ======\n\n");

    return 0;
}
#endif // DEBUG

void test_matrix(void)
{
    matrix* mtx1 = new_matrix(3, 2);
    matrix* mtx2 = new_matrix(2, 4);
    
    for (int i = 0; i < get_row(mtx1); i++)
        for (int j = 0; j < get_col(mtx1); j++)
            set_item(mtx1, i, j, i * get_col(mtx1) + j);
    
    for (int i = 0; i < get_row(mtx2); i++)
        for (int j = 0; j < get_col(mtx2); j++)
            set_item(mtx2, i, j, i * get_col(mtx2) + j);

    matrix* mtx3 = dot_mm(mtx1, mtx2);

    print(mtx1, "A =\n");
    print(mtx2, "\nB =\n");
    print(mtx3, "\nA dot B =\n");

    printf("\nsum(A) = %f\n", sum_m(mtx1));
    
    mul_s(mtx1, 0.1);
    print(mtx1, "\n0.1 * A =\n");

    add_m(mtx1, mtx1);
    print(mtx1, "\n(0.1 * A) + (0.1 * A) =\n");

    add_s(mtx1, 1.0);
    print(mtx1, "\n0.2 * A + 1.0 =\n");

    free_matrix(mtx1);
    free_matrix(mtx2);
    free_matrix(mtx3);
}

void test_grid(void)
{
    int x = 0, y = 1, z = 2;
    grid* gd = new_grid(x, y, z, BULK);

    printf("x = %d\n", get_x(gd));
    printf("y = %d\n", get_y(gd));
    printf("z = %d\n", get_z(gd));
    printf("t = %d\n", get_type(gd));
    print(get_Q(gd), "\nQ =\n");
    print(get_h(gd), "\nh =\n");

    free_grid(gd);
}