#include <stdio.h>
#include <stdlib.h>
#include "matrix.h"
#include "grid.h"

void print(matrix* mtx, int row, int col, char* prompt);
void test_matrix(void);
void test_grid(void);

int main(void)
{
	test_grid();
	return 0;
}

void print(matrix* mtx, int row, int col, char* prompt)
{
	printf("%s", prompt);
	for (int i = 0; i < row; i++) {
		for (int j = 0; j < col; j++) {
			printf("%lf ", get_item(mtx, i, j));
		}
		printf("\n");
	}
}

void test_matrix(void)
{
	const int row = 3, col = 3;
	matrix* mtx1 = new_matrix(row, col);
	matrix* mtx2 = new_matrix(row, col);
	
	for (int i = 0; i < row; i++) {
		for (int j = 0; j < col; j++) {
			set_item(mtx1, i, j, i * col + j);
			set_item(mtx2, i, j, i * col + j);
		}
	}

	matrix* mtx3 = dot_mm(mtx1, mtx2);

	#ifdef DEBUG
	print(mtx1, row, col, "A =\n");
	print(mtx2, row, col, "\nB =\n");
	print(mtx3, row, col, "\nA dot B =\n");
	#endif

	free_matrix(mtx1);
	free_matrix(mtx2);
	free_matrix(mtx3);
}

void test_grid(void)
{
	int x = 0, y = 1, z = 2;
	char tag = 'b';
	grid* gd = new_grid(x, y, z, tag);

	printf("%d\n", get_x(gd));
	printf("%d\n", get_y(gd));
	printf("%d\n", get_z(gd));
	print(get_Q(gd), 3, 3, "\nQ =\n");
	print(get_h(gd), 3, 3, "\nh =\n");

	free_grid(gd);
}