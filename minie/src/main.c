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

matrix* Q_tensor(const matrix* n, double S);
// void simulate(grid* mesh);

void printmesh(const grid* mesh);
void count_types(grid* mesh);

const int N = NX * NY * NZ; // 25 * 25 * 15 = 9375

// #ifndef DEBUG
int main(int argc, char const *argv[])
{
    param prm;
    prm.L = 4e-9;
    prm.A = -0.172e6;
    prm.B = -2.12e6;
    prm.C = 1.73e6;
    prm.W_uni = 1e0;
    prm.W_deg = 1e-1;
    prm.gamma = 1;
    prm.dx = 1;
    prm.dy = 1;
    prm.dz = 1;
    prm.dt = 3e-7;
    prm.t = 3e-2;

    n_subs = init_matrix(new_matrix(1, 3), 1.0, 0.0, 0.0);
    n_shel = init_matrix(new_matrix(1, 3), 1.0, 0.0, 0.0);

    S_subs = 0.9;
    S_shel = 0.9;
    S_cent = 0.5;
    S_init = 0.1;

    grid mesh[N];
    init(mesh);
    load_Q(mesh);

    matrix* lapQ;
    matrix* gradQx = new_matrix(3, 3);
    matrix* gradQy = new_matrix(3, 3);
    matrix* gradQz = new_matrix(3, 3);
    matrix* inner;

    for (int i = 0; i < (int)(prm.t / prm.dt); i++) {
        for (int j = 0; j < N; j++) {

            int top = (j + 1) % NZ;
            int bottom = (j - 1) % NZ;
            int right = (j + NZ) % NY;
            int left = (j - NZ) % NY;
            int front = (j + NZ * NY) % NX;
            int back = (j - NZ * NY) % NX;

            lapQ = laplacian(mesh[j].Q, 6, mesh[top].Q, mesh[bottom].Q, mesh[right].Q, mesh[left].Q, mesh[front].Q, mesh[back].Q);

            for (int k = 0; k < 9; k++) {
                set_elem(gradQx, k, (get_elem(mesh[front].Q, k) - get_elem(mesh[back].Q, k)) / (2 * prm.dx));
                set_elem(gradQy, k, (get_elem(mesh[right].Q, k) - get_elem(mesh[left].Q, k)) / (2 * prm.dy));
                set_elem(gradQz, k, (get_elem(mesh[top].Q, k) - get_elem(mesh[bottom].Q, k)) / (2 * prm.dz));
            }

            inner = dot_mm(mesh[j].Q, mesh[j].Q);
            double coeff = sum_m(mul_mm(mesh[j].Q, trans(mesh[j].Q)));

            switch (mesh[j].t) {
                case BULK:
                    for (int k = 0; k < 9; k++) {
                        set_elem(mesh[j].h, k, (prm.L * get_elem(lapQ, k))
                                             - (prm.A * get_elem(mesh[j].Q, k))
                                             - (prm.B * get_elem(inner, k))
                                             - (prm.C * get_elem(mesh[j].Q, k)) * coeff);
                    }
                    break;
                
                case UNI:
                    for (int k = 0; k < 9; k++) {
                        set_elem(mesh[j].h, k,
                            prm.L * (get_elem(gradQx, k) * mesh[j].x + get_elem(gradQy, k) * mesh[j].y + get_elem(gradQz, k) * mesh[j].z)
                          + prm.W_uni * (get_elem(mesh[j].Q, k) - get_elem(mesh[j].Qb, k)));
                    }
                    break;
                
                case DEG:
                    for (int k = 0; k < 9; k++) {
                        set_elem(mesh[j].h, k,
                            prm.L * (get_elem(gradQx, k) * mesh[j].x + get_elem(gradQy, k) * mesh[j].y + get_elem(gradQz, k) * mesh[j].z)
                          + prm.W_deg * (get_elem(mesh[j].Q, k) - get_elem(mesh[j].Qb, k)));
                    }
                    break;
            }

        }

        for(int j = 0; j < N; j++) {
            add_m(mesh[j].Q, mul_sm(prm.dt / prm.gamma, mesh[j].h));
        }
    }

    free_matrix(lapQ);
    free_matrix(gradQx);
    free_matrix(gradQy);
    free_matrix(gradQz);
    free_matrix(inner);

    save_Q(mesh);
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

        if (mesh[i].z == 0 || mesh[i].z == NZ - 1) {
            mesh[i].t = DEG;
            mesh[i].Qb = Q_tensor(n_subs, S_subs); // degenerate
        }
        else if (fabs(distance - RADIUS) <= THICKNESS) {
            mesh[i].t = UNI;
            mesh[i].Qb = Q_tensor(n_shel, S_shel); // uniform
        }
        else {
            mesh[i].t = BULK;
            mesh[i].Qb = NULL;
        }
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

matrix* Q_tensor(const matrix* n, double S)
{
    assert(get_row(n) == 1);
    assert(get_col(n) == 3);

    matrix* Q = dot_mm(trans(n), n);

    for (int i = 0; i < get_row(Q); i++) {
        for (int j = 0; j < get_col(Q); j++) {
            set_item(Q, i, j, (S / 2) * (3 * get_elem(n, i) * get_elem(n, j) - DELTA(i, j)));
        }
    }
    return Q;
}

void load_Q(grid* mesh)
{
    for (int i = 0; i < N; i++)
        for (int j = 0; j < 9; j++)
            scanf("%lf,", (double *)(get_Q(mesh + i) + j));
}

void save_Q(const grid* mesh)
{
    for (int i = 0; i < N; i++)
        for (int j = 0; j < 9; j++)
            printf("%lf,", *(double *)(get_Q(mesh + i) + j));
}

// void simulate(grid* mesh, const param* prm)
// {
//     for (int i = 0; i < N; i++) {
//         molefield(mesh[i], prm,
//             mesh[(i + 1) % NZ].Q,
//             mesh[(i - 1) % NZ].Q,
//             mesh[(i + NZ) % NY].Q,
//             mesh[(i - NZ) % NY].Q,
//             mesh[(i + NZ * NY) % NX].Q,
//             mesh[(i - NZ * NY) % NX].Q,
//             mesh[], normal);
//         evolute(mesh[i], prm);
//     }
// }

void printmesh(const grid* mesh)
{
    for (int i = 0; i < N; i++) {
        printf("%d %d %d %d\t%f\n", mesh[i].x, mesh[i].y, mesh[i].z, mesh[i].t,
            norm(DIMENSION, mesh[i].x, mesh[i].y, mesh[i].z) - RADIUS);
        // print(mesh[i].Q, "");
        // print(mesh[i].h, "");
    }
}

void count_types(grid* mesh) {
    int bulk = 0, uni = 0, deg = 0;
    for (int i = 0; i < N; i++) {
        switch (mesh[i].t) {
            case BULK: bulk++; break;
            case UNI: uni++; break;
            case DEG: deg++; break;
        }
    }
    printf("bulk: %d\nuniform: %d\ndegenerate: %d\n", bulk, uni, deg);
    printf("ratio: %f\n", (double)(uni + deg) / (bulk + uni + deg));
}