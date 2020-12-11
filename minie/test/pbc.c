/* Test for the formula of 3-dimensional periodic boundary condition */

#include <stdio.h>

#define MOD(a, b) (a) < 0 ? (a) % (b) + (b) : (a) % (b)

// periodic boundary condition
int pbc(int index, int shift, int period) {
    return MOD(index + shift, period) + index / period * period;
}

int main(void) {
	int size[3], tmp;
	
	printf("mesh size (x, y, z): ");
	for (int i = 0; i < 3; i++) {
		scanf("%d", &tmp);
		size[i] = tmp > 0 ? tmp : 1;
	}

    for (int i = 0; i < size[0] * size[1] * size[2]; i++) {
        int zp = pbc(i, -1, 				size[2]);
        int zn = pbc(i,  1, 				size[2]);
        int yp = pbc(i, -size[2], 			size[2] * size[1]);
        int yn = pbc(i,  size[2], 			size[2] * size[1]);
        int xp = pbc(i, -size[1] * size[2], size[2] * size[1] * size[0]);
        int xn = pbc(i,  size[1] * size[2], size[2] * size[1] * size[0]);
        printf("%2d %2d %2d %2d %2d %2d %2d\n", i, zp, zn, yp, yn, xp, xn);
    }
    return 0;
}
