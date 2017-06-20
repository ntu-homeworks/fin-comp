Pricing American Put Option based on the GARCH Model (Ritchken-Trevor Algorithm)
============================================================
梁智湧

### Usage

#### Run the Program
```
usage: python run.py [-h] E r S h0 β0 β1 β2 c X n1 n2

Pricing American put options based on Ritchken-Trevor algorithm.

positional arguments:
  E           days before expiration
  r           annual interest rate
  S           stock price at time 0
  h0
  β0
  β1
  β2
  c
  X           strike price
  n1          number of partitions per day
  n2          number of variances per node

optional arguments:
  -h, --help  show this help message and exit
```

#### Example
```bash
$ python run.py 30 0.01 100 0.010469 0.000006575 0.9 0.04 0 100 2 2
2.18830467605
```