#!/bin/bash -l
#SBATCH -J  ShalCNN
#SBATCH -o ShallCNN-%j.out
#SBATCH --partition gpu3
#SBATCH --nodes=1
#SBATCH --ntasks=1         # leave at '1' unless using a MPI code
#SBATCH --cpus-per-task=1  # cores per task
#SBATCH --mem=100G
#SBATCH --mem-per-cpu=10G  # memory per core (default is 1GB/core)
#SBATCH --time 2-00:00     # days-hours:minutes
#SBATCH --qos=normal
#SBATCH --account=general-gpu  # investors will replace this with their account name
#SBATCH --gres gpu:"GeForce GTX 1080 Ti":1

module load cuda/cuda-9.0.176
module load cudnn/cudnn-7.1.4-cuda-9.0.176
export GPUARRAY_FORCE_CUDA_DRIVER_LOAD=""
export HDF5_USE_FILE_LOCKING=FALSE
## ENV_FLAG
source /storage/htc/bdm/zhiye/DNCON4/env/dncon4_virenv/bin/activate
#python train_v3_all_data.py <X-feature-directory> <Y-Label-directory> <list-files-directory>
python train_v3_all_data.py /storage/htc/bdm/farhan/DNCON2_features_homodimers/feat /storage/htc/bdm/farhan/DNCON2_features_homodimers/Y-Labels ../training_lists/same/

