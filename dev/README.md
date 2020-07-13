# Development Plan
### Rewrite the computation kernel with C language
Computing finite difference discrete Laplacian, and compare the efficiency of C version and Python + Numpy version.

### Feature
- `main.c` is the C source files of computing Laplancian.
- `Makefile` describes how to build the C codes in the `src` directory.
- `lap.exe` is the executable file that computes Laplacian. It will appear after you finish the compilation.
- `lap.py` is the Python script for computing Laplancian.
- `bench.sh` is the benchmark that repeatedly runs the programs and shows the time it/they spent.

### Requirement
To build these two version of programs, you need the following build tools and packages:
- GNU Compiler Collection or other C compiler
- GNU Make
- Python 3.6 or later
- Numpy package

For Ubuntu or other Debian-derived Linux distributions, directly type the following commands to install the tools and packages above  
```bash
sudo apt update
sudo apt install gcc make python3 python3-pip
pip3 install -r ../requirements.txt
```

### Usage
#### Compile the C program
Navigate to the `dev` directory, and `make` it.  
```bash
make
```
After comilaltion, you will see an executable file named `lap.exe` appears in the current directory.  

If you want an executable which prints the calculation results for debugging, `make` it by the following commands.  
```bash
make clean debug
```

#### Run the benchmark script
Here is a script `bench.sh` used to execute the programs repeatedly to evaluate the effieciency of the programs.  

Stay at the `dev` directory, and then source the script.  
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