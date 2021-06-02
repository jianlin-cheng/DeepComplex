#!/bin/sh
#!/bin/bash -l
#SBATCH -J  strings
#SBATCH -o Aln_hetero-\%j.out
#SBATCH --partition Lewis,hpc4,hpc5
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=150G
#SBATCH --time 01-00:00:00

#$1=list_file
#$2=a3m_aln_folder
#$3=ppi_dict
#$4=outdir
start=$(date +%s.%N)
source /storage/htc/bdm/zhiye/DNCON4/env/dncon4_virenv/bin/activate
python /storage/htc/bdm/farhan/string_db/hetero30_aln_run/joinAlignments4Hetero_one.py $1 $2 $3 $4 
deactivate
end=$(date +%s.%N)
echo "Starttime $start"
echo "Endtime $end"
runtime=$(end-start)
echo "Runningtime $runtime"
exit 0

