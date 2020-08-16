# LdG-sim

[![license](https://img.shields.io/github/license/tings0802/LdG-sim)](https://github.com/tings0802/LdG-sim/blob/master/LICENSE)
[![tag](https://img.shields.io/github/v/tag/tings0802/LdG-sim)](https://github.com/tings0802/LdG-sim/tags)
![code-size](https://img.shields.io/github/languages/code-size/tings0802/LdG-sim)
![repo-size](https://img.shields.io/github/repo-size/tings0802/LdG-sim)

An implementation of Landau-de Gennes's model of nematic liquid crystal simulation  

## Feature  
- `src` contains the C source files which can be compiled to run the numerical simulation  
- `utils` includes the preprocessing and post-processing tools used to generate the meshgrids, configure the simulation, and visualize the results  
- `bench` provides a general-purpose benchmark script to evaluate the computational efficiencies of programs  

## Download  
```shell
git clone https://github.com/tings0802/LdG-sim.git
```

## Prerequisites  
- C compiler that supports C99 standard  
- GNU Make  
- Python 3.6 or later  
- Numpy  
- Matplotlib  

After cloning the LdG-sim repository, you can use the following command to install the SDKs and packages of dependencies.  

#### With Package manager  
For **Ubuntu 18.04**, **Debain 10**, or later versions, directly type the following command to install GCC, Make, Python, and pip:  
```bash
sudo apt update && sudo apt install -y build-essential python3 python3-pip
```

You can check the versions of Python and pip with the following commands:  
```bash
python3 --version
pip3 --version
```

Then you can use the command to install Numpy and Matplotlib:
```shell
pip3 install -r utils/requirements.txt
```

#### From source code  
For older versions of operating system or users that doesn't have the root permission to use package manager, You should build dependencies from source code.  

> If you don't have pip, see this documentation to [install pip](https://pip.pypa.io/en/stable/installing/).  

## Compilation  
Navigate to the `src` folder, and then `make` it.  

```bash
make
```

## Usage
To run a simulation with `LdG-sim`, you have to follow the instructions below:  
1. modify the `utils/param.py` to configure the system to be simulated (e.g. box size, time steps)  
2. run `utils/main.py` to generate the meshgrid with Q-tensors initialized and store it in `data/`  
3. execute `bin/minie` with the given meshgrid to run the simulation  
4. use `utils/visual.py` to visualize the system  

<!-- ## Contributing -->

<!-- ## Citation -->

## License
`LdG-sim` is released under the [MIT License](https://github.com/tings0802/LdG-sim/blob/master/LICENSE).  
Please cite the following paper if you use this package for published research:  
<a href="https://doi.org/10.1080/02678290903056095" target="_blank">M. Ravnik, S. Žumer, Liquid Crystals **36**, 1201-1214 (2009)</a>