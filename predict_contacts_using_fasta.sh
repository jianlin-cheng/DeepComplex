#!/bin/bash -l
#$1=fasta_sequence
#$2=output_folder
thisdir=$(dirname $(readlink -f $0))
if ![ -f $1 ]; then
    echo "Fasta file $1 not found...Quitting!"
    exit 1
fi

if ![ -d $2 ]; then
    mkdir -p $2
fi

perl $thisdir/inter_chain_contact_predictor/homo_dimer/feature/feature_gen_dncon2/feature_gen_dncon2.pl $1 $2
