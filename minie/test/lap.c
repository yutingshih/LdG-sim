#include "../src/matrix.h"

int main()
{
    const int row = 2, col = 2;
    matrix* mat0 = new_matrix(row, col);
    matrix* mat1 = new_matrix(row, col);
    matrix* mat2 = new_matrix(row, col);
    matrix* mat3 = new_matrix(row, col);
    matrix* mat4 = new_matrix(row, col);

    for (int i = 0; i < row * col; i++) {
        set_elem(mat0, i, i - 1);
        set_elem(mat1, i, i + 2);
        set_elem(mat2, i, i - 3);
        set_elem(mat3, i, i + 4);
        set_elem(mat4, i, i - 5);
    }
    
    print(mat0, "mat0 =\n");
    print(mat1, "mat1 =\n");
    print(mat2, "mat2 =\n");
    print(mat3, "mat3 =\n");
    print(mat4, "mat4 =\n");

    matrix* lap = laplacian(mat0, 4, mat1, mat2, mat3, mat4);
    print(lap, "lap = (mat1 + mat2 + mat3 + mat4) / 4 - mat0\n");

    free_matrix(mat0);
    free_matrix(mat1);
    free_matrix(mat2);
    free_matrix(mat3);
    free_matrix(mat4);
    free_matrix(lap);
}
