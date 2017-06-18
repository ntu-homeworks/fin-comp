#include <stdio.h>
#include <stdlib.h>
#define ARG_COUNT 7

double S;        // stock price at time 0
double X;        // strike price
double T;        // maturity in years
double sigma;    // annual volatility
double r;        // continuously compounded annual interest rate
int n;           // number of periods
int k;           // number of simulation paths

#include "arguments.h"

static const char *symbols[ARG_COUNT] = {
    "S", "X", "T", "σ", "r", "n", "k"
};

static const char *descriptions[ARG_COUNT] = {
    "stock price at time 0",
    "strike price",
    "maturity in years",
    "annual volatility",
    "continuously compounded annual interest rate",
    "number of periods",
    "number of simulation paths"
};

void get_arguments(int argc, char *argv[]) {
    if (argc != ARG_COUNT + 1)
        goto print_usage;

    S     = atof(argv[1]);
    X     = atof(argv[2]);
    T     = atof(argv[3]);
    sigma = atof(argv[4]);
    r     = atof(argv[5]);
    n     = atoi(argv[6]);
    k     = atoi(argv[7]);

    return;

print_usage:
    // Short description
    printf("Usage: %s", argv[0]);
    for (int i=0; i<ARG_COUNT; i++) {
        printf(" <%s>", symbols[i]);
    }
    puts("\n");

    // Long description
    puts("Description:");
    for (int i=0; i<ARG_COUNT; i++) {
        printf("\t- %s: %s.\n", symbols[i], descriptions[i]);
    }

    exit(1);
}
