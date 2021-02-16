import os
import sys

from Bio import pairwise2
import re

import numpy as np


def loadFastaDictionary(dict_file):
    fasta_dict = {}
    with open(dict_file, "r") as f:
        for line in f:
            fasta_dict[line.strip().split(":")[0].strip()] = line.strip().split(":")[1].strip()
    return fasta_dict


def check_number_gaps_before_index(_input, number):
    # remember it is 0 indexed
    gap_counter = 0
    counter = 0
    for i in _input:
        if counter >= number:
            return gap_counter
        if i == "-":
            gap_counter = gap_counter + 1

    return gap_counter


def gap_indices(_input):
    # remember it is 0 indexed
    index = []
    gap_counter = 0
    for i in _input:
        if i == '-':
            index.append(gap_counter)
        gap_counter = gap_counter + 1
    return index


def common_sequence(_array):
    string_val = ""
    array_len = len(_array)
    seq_len = len(_array[0])
    for i in range(seq_len):
        match = True
        for j in range(array_len - 1):
            if _array[j][i] != _array[j + 1][i]:
                match = False
                break
        if match == True:
            string_val = string_val + _array[j][i]
    return string_val


def index_to_remove(old, new):
    aln_val = pairwise2.align.globalms(old, new, 5, -4, -1, -0.1)[0][1]
    ret = gap_indices(aln_val)
    return ret


class protein_in_dimer_classes:
    name = ""
    old_fasta = ""
    aligned_fasta = ""
    new_fasta = ""
    index_to_remove = []


def write2file(file, contents):
    with open(file, "w") as f:
        f.writelines(contents)


def specific_filers(_input):
    os.chdir(_input)
    fileNames = []
    # fileNames = glob.glob(fasta_dir + "/*fasta")
    for root, directories, files in os.walk(_input):
        for file in files:
            if ".seq" in file:
                fileNames.append(os.path.abspath(file))
    return fileNames


from Bio import AlignIO, pairwise2

# output_dir = "/home/rajroy/reindex/"
# new_fasta_dir = output_dir + "/new_fasta/"
# fasta_dir = "/home/rajroy/Downloads/fasta_dictionary.txt"
# seq_dir = "/home/rajroy/Documents/Clustlw_alignment/output/"
# seq_dir = "/home/rajroy/sampoel/out/"



fasta_dir = sys.argv[1]
seq_dir = sys.argv[2]
output_dir = sys.argv[3]

new_fasta_dir = output_dir + "/new_fasta/"
seq_file = specific_filers(seq_dir)
fasta_dict = loadFastaDictionary(fasta_dir)
names = []
failed_cases=[]
val_counter = 0
omega_list = {}
for files in seq_file:

    align = AlignIO.read(files, "clustal")
    temp = align._records
    list_to_align = []
    list_to_output = []
    for val in align._records:
        a_protein_in_dimer_classes = protein_in_dimer_classes()
        a_protein_in_dimer_classes.name = val.description
        # old fasta
        a_protein_in_dimer_classes.old_fasta = fasta_dict.get(a_protein_in_dimer_classes.name)
        names.append(val.description)
        list_to_align.append(val.seq)
        a_protein_in_dimer_classes.aligned_fasta = str(val.seq)
        # print(val.description + " : " + val.seq)
        list_to_output.append(a_protein_in_dimer_classes)
        # new

    new_fasta = common_sequence(list_to_align)
    if len(new_fasta) ==0:
        failed_cases.append(files)
    else:
        for value in list_to_output:
            value.new_fasta = new_fasta

            value.index_to_remove = index_to_remove(old=value.old_fasta, new=new_fasta)
            omega_list[value.name] = value
            fasta_seq = ""
            fasta_seq = ">" + value.name + "\n"
            fasta_seq = fasta_seq + new_fasta
            write2file(new_fasta_dir + value.name + ".fasta", fasta_seq)
        val_counter = val_counter + 1
        print(str(100 * val_counter / len(seq_file)))
        # print("        " + common_sequence(list_to_align))

np.save(output_dir + 'reindex_fasta.npy', omega_list)
print(len(list(dict.fromkeys(names))))
f_string = ""
for f in failed_cases:
    f_string=f_string+f+"\n"
# write2file("/home/rajroy/failed_cases.txt",f_string)
write2file(output_dir+"failed_cases.txt",f_string)
print(len(failed_cases))
#ssems like gets the numbers to remove
# loaded_dimer_stats_dictionary = np.load(output_dir + 'reindex_fasta.npy', allow_pickle='TRUE').item()
#
# for val in loaded_dimer_stats_dictionary.keys():
#     print (val)
