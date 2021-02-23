#ifndef PARAM_H
#define PARAM_H

#include "matrix.h"

typedef struct {
    double L;
    double A;
    double B;
    double C;
    double W_uni;
    double W_deg;
    double gamma;
    double dx;
    double dy;
    double dz;
    double dt;
    double t;
} param;

#define DIMENSION 3
#define NX 25
#define NY 25
#define NZ 15
#define RADIUS 7
#define THICKNESS 1
#define DELTA(i, j) (i == j ? 1 : 0)
#define MOD(a, b) ((a) >= 0 ? (a) % (b) : (a) % (b) + (b))

matrix* n_subs;
matrix* n_shel;

double S_subs;
double S_shel;
double S_cent;
double S_init;

#endif // PARAM_H
