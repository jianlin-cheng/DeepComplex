#!/bin/bash -l
thisdir=$(dirname $(readlink -f $0))
python $thisdir/inter_chain_contact_predictor/homo_dimer/feature/feature_gen_dncon2/setup_dependency_paths.py ./paths.txt
