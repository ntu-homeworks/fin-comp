Pricing American Puts using Least-squares Monte Carlo Method
============================================================
梁智湧

### About the Source Code
This program is written in C, cooperated with *[GNU Scientific Library][GSL]* (GSL), and built with CMake. The following files shall be included:

- `CMakeLists.txt`: CMake configuration to build the program.
- `arguments.h`, `arguments.c`: Input arguments handler.
- `utilities.h`, `utilities.c`: The polynomial regression calculator[^polyfit].
- `main.c`: The main algorithm.

### Usage

#### Install Required Library (GSL)
```bash
$ sudo apt-get install libgsl-dev
```

#### Build the Program
Using CMake:
```bash
$ mkdir build && cd build
$ cmake -DCMAKE_BUILD_TYPE=Release ..
$
$ # Do this only if you don't want the pseudo random number generator
$ # and desire the real random number generator:
$ cmake -DPSEUDO_RANDOM=Off .
$
$ make
```

#### Run the Program
```bash
$ ./LSMAmerPut <S> <X> <T> <σ> <r> <n> <k>
```

For the detail usage, run the program without any argument to show the help message.

### Testing Environment

CPU
: Intel(R) Xeon(R) CPU E5-2620 0 @ 2.00GHz (Max 2500MHz)
Operating system
: Ubuntu 16.04 x86\_64
Compiler
: gcc (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609
GSL (libgsl-dev)
: 2.1+dfsg-2
CMake version
: 3.5.1
GNU Make version
: 4.1

### Example Output

The program can usually finish in about 2.8 seconds under the environment described above.

#### Using Pseudo Random Number Generator
```bash
$ ./LSMAmerPut 101 105 1 0.15 0.02 50 100000
Put price:      7.353672
Standard error: 0.022143
```

#### Using Real Random Number Generator
```bash
$ ./LSMAmerPut 101 105 1 0.15 0.02 50 100000
Put price:      7.362269
Standard error: 0.022282
$ ./LSMAmerPut 101 105 1 0.15 0.02 50 100000
Put price:      7.330704
Standard error: 0.022062
$ ./LSMAmerPut 101 105 1 0.15 0.02 50 100000
Put price:      7.368418
Standard error: 0.022208
$ ./LSMAmerPut 101 105 1 0.15 0.02 50 100000
Put price:      7.361743
Standard error: 0.022085
$ ./LSMAmerPut 101 105 1 0.15 0.02 50 100000
Put price:      7.350437
Standard error: 0.021943
```

[GSL]: https://www.gnu.org/software/gsl/
[^polyfit]: Provided by [Rosettacode.org](https://rosettacode.org/wiki/Polynomial_regression#C)
