#!/bin/bash
fasta=$(readlink -f $1)
db_path=$(readlink -f $2)
outfolder=$(readlink -f $3)
fasta_name=$(basename $fasta)
mkdir -p $outfolder
mkdir -p $outfolder/tmpdir$fasta_name

echo $fasta
echo $fasta_name
echo $db_path
echo $outfolder

#/home/casp14/tools/hmmer-3.1b2-linux-intel-x86_64/src/jackhmmer --cpu 8 -N 3 -E 10 --incE 1e-3 --noali --tblout $outfolder/tmpdir$fasta_name/prot_ebi.tbl $fasta $db_path
/home/casp14/tools/hmmer-3.1b2-linux-intel-x86_64/src/jackhmmer --cpu 8 -N 3 -E 10 --incE 1e-3 -A $outfolder/tmpdir$fasta_name/prot.ali $fasta $db_path
perl /home/casp14/scripts/feature_gen/reformat.pl -l 1500 -d 1500 sto a3m $outfolder/tmpdir$fasta_name/prot.ali $outfolder/tmpdir$fasta_name/prot.a3m
grep -v "^>" $outfolder/tmpdir$fasta_name/prot.a3m | sed 's/[a-z]//g' > $outfolder/tmpdir$fasta_name/prot.aln
#/home/casp14/tools/hmmer-3.1b2-linux-intel-x86_64/easel/miniapps/esl-sfetch -f $db_path $outfolder/tmpdir$fasta_name/prot_ebi.tbl > $outfolder/tmpdir$fasta_name/prot_ebi.fseqs
#cat $fasta $outfolder/tmpdir$fasta_name/prot_ebi.fseqs > $outfolder/tmpdir$fasta_name/prot.fseqs
#mv $outfolder/tmpdir$fasta_name/prot.fseqs $outfolder/$fasta_name.jacln
mv $outfolder/tmpdir$fasta_name/prot.aln $outfolder/$fasta_name.aln


