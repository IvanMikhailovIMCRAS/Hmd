## Instruction for installing hoomd

1. Install Anaconda:
```
https://conda.io/projects/conda/en/latest/user-guide/install/linux.html
```
Python version 3.11 must be installed
After Anaconda installing, change ```conda``` configuration setting to disable the automatic base activation:
```
conda config --set auto_activate_base false
```

2. Create a conda virtual enviroment
```
conda create -n hmd python=3.11
```
where ```hmd``` is some name of the virtual enviroment

3. Activate the created virtual enviroment:
```
conda activate hmd
```

4. Install CUDA (if it is not installed and you use NVIDIA GPU):
```
sudo apt update
sudo apt install nvidia-cuda-toolkit
```

5. Install hoomd for GPU:
```
export CONDA_OVERRIDE_CUDA="12.0"
conda install -c conda-forge "hoomd=4.2.1=*gpu*" "cuda-version=12.0"
```
or install hoomd for CPU:
```
conda install "hoomd=4.2.1=*cpu*"
```

6. You should also install the GSD framework (```https://gsd.readthedocs.io/en/stable/installation.html ```):
```
conda install -c conda-forge gsd
```

7. Also you can use ```nvtop```, for example, to monitor a video card
```
sudo add-apt-repository ppa:flexiondotorg/nvtop
sudo apt install nvtop
```
nvtop
