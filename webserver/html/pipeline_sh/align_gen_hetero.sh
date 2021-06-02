#!/bin/bash -l

#this script will generate concatenated alignments of the interlogs

fasta_A=$1 #name if A.fasta
fasta_B=$2 #name it B.fasta
outputfolder=$3
db_path=/exports/store2/deepcomplex/datasets/strings_bd_monomer_fasta.txt


sh /var/www/cgi-bin/deepcomplex/deepcomplex/scripts/runJackAln.sh $fasta_A $outfolder/A/alignments $db_path

sh /var/www/cgi-bin/deepcomplex/deepcomplex/scripts/runJackAln.sh $fasta_B $outfolder/B/alignments $db_path

sh /var/www/cgi-bin/deepcomplex/deepcomplex/scripts/joinAln_one.sh $outfolder/A/alignments/A.a3m $outfolder/B/alignments/B.a3m
