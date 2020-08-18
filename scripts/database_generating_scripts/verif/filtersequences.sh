#!/bin/bash
export PATH=$PATH:/data/farhan/SoftwareTools/DeepComplexToolBox/tools/MMseqs2_static/bin
echo "Current working directory is $(pwd)"
echo "Creating sequenceDB"
mmseqs createdb $1 sequenceDB
echo "sequenceDB created!"
echo "filtering sequenceDB"
mmseqs clusthash sequenceDB resultDB --min-seq-id $2
echo "sequenceDB filtered with $2 similarity!"
#mmseqs clust sequenceDB resultDB clusterDB
#mmseqs result2repseq sequenceDB clusterDB clusterDB_rep
#mmseqs result2flat sequenceDB sequenceDB clusterDB_rep clu_rep.fasta --use-fasta-header    
echo "Trying to recreate filtered fasta"
mmseqs clust sequenceDB resultDB clusterDB
mmseqs result2repseq sequenceDB clusterDB DB_clu_rep 
mmseqs result2flat sequenceDB sequenceDB DB_clu_rep  $3 --use-fasta-header
echo "Filtered fasta file called $3 created!"
