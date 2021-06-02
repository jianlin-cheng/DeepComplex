#!/bin/bash -l

start=$(date +%s.%N)

source /exports/store2/deepcomplex/deepcomplex/tools/envs/tf_114/trRosetta/bin/activate

fasta_A=$(readlink -f $1)
fasta_B=$(readlink -f $2) 
outfolder=$(readlink -f $3)
alnfolder=$(readlink -f $4)
paths_file=$(readlink -f $5)

if [ ! -d $outfolder ]; then
    mkdir -p $outfolder
fi

python /var/www/cgi-bin/deepcomplex/deepcomplex/scripts/feature_gen_hetero_v2/pipeline.py $fasta_A $fasta_B $outfolder $alnfolder $paths_file
end=$(date +%s.%N)

echo "End: $end"
echo "Start: $start"

#runningtime=$($end-$start)

#echo "Running time: $end-$start"
#echo "$runningtime"
deactivate
exit 0


