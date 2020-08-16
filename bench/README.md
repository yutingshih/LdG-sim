# Development Plan
Rewrite the computationally intensive work with C language.  

### Feature
This project has two components, `lap` and `mtx`. Each component contains both the native C and the Python+Numpy implementations.  

- `lap` computes 1D finite difference discrete Laplacian with the periodic boundary condition.
- `mtx` calculates the multiplication between two 3x3 matrices.

This project also provides a general-purpose benchmark script `bench.sh` that repeatedly runs the given programs to evaluate the computational efficiencies of them.  

The C source files need to be compiled, and this project uses a "top level" `Makefile`
to organize the project structure and to call the "lower level" `Makefile`s in each conponent to complete the compilation process automatically.  

### Requirement
To build these two version of programs, you need the following build tools and packages:  
- GNU Compiler Collection or other C compiler
- GNU Make
- Python 3.6 or later
- Numpy package

For Ubuntu or other Debian-derived Linux distributions, directly type the following commands to install the tools and packages above:  
```bash
sudo apt update
sudo apt install gcc make python3 python3-pip
pip3 install numpy
```

### Usage
#### Compile the C programs
Navigate to the `bench` directory, and `make` them.  
```bash
make
```
After comilaltion, you will see the executable files named `lap.exe` and `mtx.exe` appears in their correspoding directories.  

If you want the executables which print the calculation results for debugging, `make` them by the following commands.  
```bash
make clean debug
```

All of these commands above use the "top level" `Makefile`. You can also modify and use the "lower level" `Makefile`s in the `lap` and `mtx` subdirectories, or manually compile the source files.  

#### Run the benchmark script
Here is a script `bench.sh` used to execute the programs repeatedly to evaluate the effieciency of the programs.  

Stay at the `bench` directory, and then source the script.  
```bash
source ./bench.sh
```
call the `bench` function written in `bench.sh`, and give it the program(s) to run.  
```bash
bench ./lap.exe
```
To see the usage of this script, use the `--help` option.  
```bash
bench --help
```
The benchmark runs 10 times by default, use `--times` option to specify the times it runs.  
```bash
bench --times 20 ./lap.exe
```
If you want to store the result as a file, use the `--output` option.  
```bash
bench --output result.txt ./lap.exe
```