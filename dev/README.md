# Development Plan
### Rewrite the computation kernel with C language
Computing finite difference discrete Laplacian, and compare the efficiency of C version and Python + Numpy version.

### Feature
- `main.c` is the C source files of computing Laplancian.
- `Makefile` describes how to build the C codes in the `src` directory.
- `lap.exe` is the executable file that computes Laplacian. It will appear after you finish the compilation.
- `lap.py` is the Python script for computing Laplancian.
- `bench.sh` is the benchmark written in Bash; shows the time spent by the two programs.

### Requirement
To build these two version of programs, you need the following build tools or packages:
- GNU Compiler Collection or other C compiler
- GNU Make
- Python 3.6 or later
- Numpy package

### Usage
#### Compile the C program
Navigate to the `dev` directory, and `make` it.  
```bash
make bench
```
After comilaltion, you will see an executable file named `lap.exe` appears in the current directory.

#### Run the benchmark script
Stay at the `dev` directory, and then source the script. The argument of `bench.sh` assigns the size of array the codes runs, it runs 10 elements by default.  
```bash
./bench.sh 10
```
