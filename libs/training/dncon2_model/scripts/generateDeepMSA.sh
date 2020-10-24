#!/bin/bash -l
#SBATCH -J DeepMSA
#SBATCH -o result-%j.out
#SBATCH -p Lewis,hpc5,hpc4,Interactive
#SBATCH -N 1
#SBATCH -n 8
####SBATCH --cpus-per-task=8
#SBATCH -t 00-04:00:00
#SBATCH --mem 20G
#SBATCH --mem-per-cpu 10G


echo "Activating python virtual environment..."
source /storage/hpc/data/fqg7h/penv/bin/activate

if [ ! $?==0 ];then
        echo "Could not activate python virtual environment. Please check if the environment exists."
        exit 1
fi
fasta_full=$(readlink -f $1)
fasta=$(basename $(readlink -f $1))
fasta_name=${fasta%.*}
outdir=$(readlink -f $2)

echo "Running DeepMSA for $fasta_name on file $fasta_full ..."

cd /storage/htc/bdm/zhiye/DNCON4_db_tools/tools/deepmsa/hhsuite2/scripts/
python build_MSA.py $fasta_full -hhblitsdb=/storage/htc/bdm/zhiye/DNCON4_db_tools/databases/UniRef30_2020_01/UniRef30_2020_01 -jackhmmerdb=/storage/htc/bdm/zhiye/DNCON4_db_tools/databases/myg_uniref100_01
_2020/myg_uniref100 -hmmsearchdb=/storage/htc/bdm/zhiye/DNCON4_db_tools/databases/Metaclust_2018_06/metaclust_50 -tmpdir=$outdir/temp/$fasta_name/tmp -outdir=$outdir -ncpu=8 -overwrite=0

if [ !$?==0 ]; then
	echo "Alignments for $fasta_name.fasta has been successfully generated!"
	echo "Results are stored in $outdir"
	deactivate
	exit 0
	exit 0
fi
echo "Error!"
deactivate
exit 1
exit 1
