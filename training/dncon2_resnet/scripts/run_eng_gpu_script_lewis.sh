#!/bin/bash
#--------------------------------------------------------------------------------
#  SBATCH CONFIG
#--------------------------------------------------------------------------------
#SBATCH --job-name=VB3D-GPU                     # name for the job
#SBATCH --cpus-per-task=8                       # number of cores
#SBATCH --mem=128G                               # total memory
#SBATCH --time 0-04:00                          # time limit in the form days-hours:minutes
#SBATCH --mail-user=nax35@mail.missouri.edu     # email address for notifications

#SBATCH --partition gpu4                        # max of 1 node and 2 hours
#SBATCH --account=engineering-gpu
#SBATCH --gres gpu:"Tesla V100-PCIE-32GB":1
#--------------------------------------------------------------------------------

echo "### Starting at: $(date) ###"

## Module Commands
# module load cmake
module load gcc/gcc-5.4.0
module load eigen/eigen-3.2.7
module load cuda/cuda-10.0.130

## Need LAPACK
## Need BLAS

## OpenCV is installed manually, this will update the search-path
source ~/.bashrc

./bin/linux/ReconParallelPipeline_MU_VB3D ./configs/albuquerque.txt
