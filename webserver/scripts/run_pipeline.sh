#!/bin/bash -l

#check homodimer or heterodimer flags

$homo_flag=$1

if [ $homoflag == '1' ]; then
{
    #run homodimer prediction
}
else
{
   #run heterodimer prediction code
}

fi

#run the optimizer

source ../tools/pyrosettta-env/bin/activate

weight_file = ../optimizer_code/talaris2013.wts

python ../optimizer/do_dock.py first_pdb second_pdb restraint_file output_dir $weight_file


