#ifndef PARAM_H
#define PARAM_H

typedef struct {
    double L;
    double A;
    double B;
    double C;
    double W_uni;
    double W_deg;
    double gamma;
    double dt;
} param;

#define DIMENSION 3
#define NX 27
#define NY 27
#define NZ 17
#define RADIUS 7
#define THICKNESS 1

#endif // PARAM_H
