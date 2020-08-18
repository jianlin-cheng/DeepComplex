#!/bin/bash
#Usage: sh filtersequences.sh <fasta_file> <threshold>

export PATH=$PATH:/home/casp14/tools/MMseqs2_static/bin
echo "Current working directory is $(pwd)"
echo "Creating sequenceDB"
#echo $?
mmseqs createdb $1 sequenceDB
if [ ! $?==0 ]; then
    echo "######### 1st: Error $?"
    exit
fi
echo "sequenceDB created!"
echo "filtering sequenceDB"
mmseqs clusthash sequenceDB resultDB --min-seq-id $2
if [ ! $?==0 ]; then
    echo "######### 2nd: Error $?"
    exit
fi
echo "sequenceDB filtered with $2 similarity!"
###mmseqs clust sequenceDB resultDB clusterDB
###mmseqs result2repseq sequenceDB clusterDB clusterDB_rep
###mmseqs result2flat sequenceDB sequenceDB clusterDB_rep clu_rep.fasta --use-fasta-header    
echo "Trying to recreate filtered fasta"
mmseqs clust sequenceDB resultDB clusterDB
if [ ! $?==0 ]; then
    echo "######### 3rd: Error $?"
    exit
fi
mmseqs result2repseq sequenceDB clusterDB DB_clu_rep 
if [ ! $?==0 ]; then
    echo "######### 4th: Error $?"
    exit
fi
mmseqs result2flat sequenceDB sequenceDB DB_clu_rep $3_$2 --use-fasta-header
if [ ! $?==0 ]; then
    echo "######### 5th: Error $?"
    exit
fi
echo "Filtered fasta file called $3_$2 created!"
