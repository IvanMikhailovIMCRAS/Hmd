## Instruction for using hoomd

1. Install Anaconda:
\```
https://conda.io/projects/conda/en/latest/user-guide/install/linux.html
\```

\```
conda create -n hmd python=3.11
\```

conda activate hmd
#возможно придётся установит cuda 12.0 
export CONDA_OVERRIDE_CUDA="12.0"
conda install -c conda-forge "hoomd=4.2.1=*gpu*" "cuda-version=12.0"
conda install -c conda-forge gsd

    мониторинг загрузки видеокарты:
sudo add-apt-repository ppa:flexiondotorg/nvtop
sudo apt install nvtop

nvtop
