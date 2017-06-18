#pragma once

extern double S;        // stock price at time 0
extern double X;        // strike price
extern double T;        // maturity in years
extern double sigma;    // annual volatility
extern double r;        // continuously compounded annual interest rate
extern int n;           // number of periods
extern int k;           // number of simulation paths

void get_arguments(int argc, char *argv[]);
