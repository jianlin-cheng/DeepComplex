#!/bin/bash
fasta=$(readlink -f $1)
db_path=/storage/htc/bdm/farhan/string_db/combined_strings_db/filter_combo/all_sequences.txt
outfolder=$(readlink -f $2)
fn=$(basename $fasta)
fasta_name=${fn%.*}
mkdir -p $outfolder
mkdir -p $outfolder/tmpdir$fasta_name

echo $fasta
echo $fasta_name
echo $db_path
echo $outfolder

#/home/casp14/tools/hmmer-3.1b2-linux-intel-x86_64/src/jackhmmer --cpu 8 -N 3 -E 10 --incE 1e-4 --noali --tblout $outfolder/tmpdir$fasta_name/prot_ebi.tbl $fasta $db_path
/home/casp14/tools/hmmer-3.1b2-linux-intel-x86_64/src/jackhmmer --cpu 8 -N 5 -E 1e-4 -A $outfolder/tmpdir$fasta_name/prot-1e-4.ali $fasta $db_path
perl /home/casp14/scripts/feature_gen/reformat.pl -l 1500 -d 1500 sto a3m $outfolder/tmpdir$fasta_name/prot-1e-4.ali $outfolder/tmpdir$fasta_name/prot-1e-4.a3m
grep -v "^>" $outfolder/tmpdir$fasta_name/prot-1e-4.a3m | sed 's/[a-z]//g' > $outfolder/tmpdir$fasta_name/prot-1e-4.aln

/home/casp14/tools/hmmer-3.1b2-linux-intel-x86_64/src/jackhmmer --cpu 8 -N 5 -E 1e-20 -A $outfolder/tmpdir$fasta_name/prot-1e-20.ali $fasta $db_path
perl /home/casp14/scripts/feature_gen/reformat.pl -l 1500 -d 1500 sto a3m $outfolder/tmpdir$fasta_name/prot-1e-20.ali $outfolder/tmpdir$fasta_name/prot-1e-20.a3m
grep -v "^>" $outfolder/tmpdir$fasta_name/prot-1e-20.a3m | sed 's/[a-z]//g' > $outfolder/tmpdir$fasta_name/prot-1e-20.aln

/home/casp14/tools/hmmer-3.1b2-linux-intel-x86_64/src/jackhmmer --cpu 8 -N 5 -E 1e-10 -A $outfolder/tmpdir$fasta_name/prot-1e-10.ali $fasta $db_path
perl /home/casp14/scripts/feature_gen/reformat.pl -l 1500 -d 1500 sto a3m $outfolder/tmpdir$fasta_name/prot-1e-10.ali $outfolder/tmpdir$fasta_name/prot-1e-10.a3m
grep -v "^>" $outfolder/tmpdir$fasta_name/prot-1e-10.a3m | sed 's/[a-z]//g' > $outfolder/tmpdir$fasta_name/prot-1e-10.aln


/home/casp14/tools/hmmer-3.1b2-linux-intel-x86_64/src/jackhmmer --cpu 8 -N 5 -E 1 -A $outfolder/tmpdir$fasta_name/prot-1.ali $fasta $db_path
perl /home/casp14/scripts/feature_gen/reformat.pl -l 1500 -d 1500 sto a3m $outfolder/tmpdir$fasta_name/prot-1.ali $outfolder/tmpdir$fasta_name/prot-1.a3m
grep -v "^>" $outfolder/tmpdir$fasta_name/prot-1.a3m | sed 's/[a-z]//g' > $outfolder/tmpdir$fasta_name/prot-1.aln

#mv $outfolder/tmpdir$fasta_name/prot.aln $outfolder/$fasta_name.aln


