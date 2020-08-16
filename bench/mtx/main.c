#include <stdio.h>
#include <stdlib.h>
#include "matrix.h"

void print(matrix* mtx, int row, int col, char* prompt);

int main()
{
	const int row = 3, col = 3;
	matrix* mtx1 = new_matrix(row, col);
	matrix* mtx2 = new_matrix(row, col);
	matrix* mtx3 = new_matrix(row, col);
	
	for (int i = 0; i < row; i++) {
		for (int j = 0; j < col; j++) {
			set_item(mtx1, i, j, i * col + j);
			set_item(mtx2, i, j, i * col + j);
			set_item(mtx3, i, j, 0);
		}
	}

	mtx3 = dot_mm(mtx1, mtx2);

	#ifdef DEBUG
	print(mtx1, row, col, "A =\n");
	print(mtx2, row, col, "\nB =\n");
	print(mtx3, row, col, "\nA dot B =\n");
	#endif

	free_matrix(mtx1);
	free_matrix(mtx2);
	free_matrix(mtx3);

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