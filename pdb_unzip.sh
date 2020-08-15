#!/bin/bash

input="proteins_to_extract.txt"

while IFS= read -r line
do
	echo "$line"	
	gunzip -c "atom/$line.atom.gz" > "pdb_atom/$line.atom"

done < "$input"
 
echo -e "\n"

