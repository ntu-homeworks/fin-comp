#pragma once

double nrand(double mean, double std);

// From https://rosettacode.org/wiki/Polynomial_regression#C
void polynomialfit(int obs, int degree,
                   double *dx, double *dy, double *store);
