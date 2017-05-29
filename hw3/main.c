#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "arguments.h"
#include "utilities.h"

static inline double discounted_future(double *cash_flow_j, int i, int n, double discount_factor) {
    for (int ii=1; i+ii<n; ii++) {
        if (cash_flow_j[i+ii] != 0) {
            return cash_flow_j[i+ii] * pow(discount_factor, ii);
        }
    }

    return 0;
}

int main(int argc, char *argv[]) {
#ifndef PSEUDO_RANDOM
    srand48(time(NULL));
#endif

    get_arguments(argc, argv);

    double delta_t         = T / n;
    double discount_factor = exp(-r * delta_t);

    // Generate stock price path table
    double (*stock_prices)[n] = (double (*)[n]) malloc(sizeof(double) * k * n);
    for (int j=0; j<k; j++) {
        // S_0
        stock_prices[j][0] = S;

        // S_1 ~ S_n
        for (int i=1; i<n; i++) {
            stock_prices[j][i] = stock_prices[j][i-1] * exp(
                (r - sigma * sigma / 2) * delta_t +
                sigma * sqrt(delta_t) * nrand(0, 1)
            );
        }
    }

    // Initialize from last period
    double (*cash_flow)[n] = (double (*)[n]) malloc(sizeof(double) * k * n);
    for (int j=0; j<k; j++) {
        cash_flow[j][n-1] = fmax(X - stock_prices[j][n-1], 0);
    }

    // Regress cash flow table
    double *x = (double *) malloc(sizeof(double) * k);
    double *y = (double *) malloc(sizeof(double) * k);
    for (int i=n-2; i>=0; i--) {
        // Get x, y
        int in_money_count = 0;

        for (int j=0; j<k; j++) {
            if (X < stock_prices[j][i]) {
                continue;
            }

            x[in_money_count]   = stock_prices[j][i];
            y[in_money_count++] = discounted_future(cash_flow[j], i, n, discount_factor);
        }

        // Perform polynomial regression for x, y
        double coef[3];
        polynomialfit(in_money_count, 3, x, y, coef);

        // Determine values of exercise & continuation.
        // Compare them to decide whether early exercise.
        for (int j=0; j<k; j++) {
            double exercise = fmax(X - stock_prices[j][i], 0);
            if (!exercise) {
                cash_flow[j][i] = 0;
                continue;
            }

            double continuation =
                coef[0] +                                           // x^0
                stock_prices[j][i] * coef[1] +                      // x^1
                stock_prices[j][i] * stock_prices[j][i] * coef[2];  // x^2

            if (continuation > exercise) {
                cash_flow[j][i] = 0;
            } else {
                cash_flow[j][i] = exercise;

                // Early exercised, so following time periods are valueless.
                for (int ii=i+1; ii<n; ii++) {
                    cash_flow[j][ii] = 0;
                }
            }
        }
    }

    // Calculate the put price
    double value_sum = 0;
    for (int j=0; j<k; j++) {
        value_sum += discounted_future(cash_flow[j], 0, n, discount_factor);
    }
    double put_price = fmax(value_sum / (double) k, X - S);

    printf("Put price: %lf\n", put_price);

    free(cash_flow);
    free(stock_prices);
    free(x);
    free(y);
}
