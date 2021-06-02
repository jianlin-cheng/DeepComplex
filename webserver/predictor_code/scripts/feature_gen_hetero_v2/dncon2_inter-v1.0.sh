#!/bin/bash -e
# Farhan Quadir
# The main script for making DNCON2 interchain contact prediction

if [ $# != 2 ]; then
	echo "$0 <fasta> <output-directory>"
	exit
fi

ROOT=$(dirname $0)

$ROOT/scripts/dncon2-main_inter.pl $1 $2
