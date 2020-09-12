#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <math.h>
#include "matrix.h"
#include "grid.h"
#include "param.h"

void init(grid* mesh);
double norm(int count, ...);
void load_Q(grid* mesh);
void save_Q(const grid* mesh);

void printmesh(const grid* mesh);

const int N = NX * NY * NZ; // 27 * 27 * 17 = 12393

// #ifndef DEBUG
int main(int argc, char const *argv[])
{
    grid mesh[N];
    init(mesh);

    load_Q(mesh);
    save_Q(mesh);

    printf("\n");

    return 0;
}
// #endif // DEBUG

void init(grid* mesh)
{
    double distance;

    for (int i = 0; i < NX * NY * NZ; i++) {
        mesh[i].x = i / (NY * NZ);
        mesh[i].y = i % (NY * NZ) / NZ;
        mesh[i].z = i % NZ;
        mesh[i].Q = new_matrix(3, 3);
        mesh[i].h = new_matrix(3, 3);

        distance = norm(DIMENSION, mesh[i].x, mesh[i].y, mesh[i].z);

        if (mesh[i].z == 0 || mesh[i].z == NZ - 1)
            mesh[i].t = DEG;
        else if (fabs(distance - RADIUS) <= THICKNESS)
            mesh[i].t = UNI;
        else
            mesh[i].t = BULK;
    }
}

double norm(int count, ...)
{
    va_list ap;
    va_start(ap, count);

    int x, sum = 0;
    for (int i = 0; i < count; i++) {
        x = va_arg(ap, int);
        sum += x * x;
    }

    va_end(ap);
    return sqrt(sum);
}

void load_Q(grid* mesh)
{
    for (int i = 0; i < N; i++)
        for (int j = 0; j < 9; j++)
            scanf("%lf ", (double *)(get_Q(mesh + i) + j));
}

void save_Q(const grid* mesh)
{
    for (int i = 0; i < N; i++)
        for (int j = 0; j < 9; j++)
            printf("%.1lf ", *(double *)(get_Q(mesh + i) + j));
}

void printmesh(const grid* mesh)
{
    for (int i = 0; i < N; i++) {
        printf("%d %d %d %d\t%f\n", mesh[i].x, mesh[i].y, mesh[i].z, mesh[i].t,
            norm(DIMENSION, mesh[i].x, mesh[i].y, mesh[i].z) - RADIUS);
        // print(mesh[i].Q, "");
        // print(mesh[i].h, "");
    }
}