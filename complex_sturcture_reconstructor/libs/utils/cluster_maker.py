import copy
import os

import numpy as np

CLUSTALW_dir = "/home/rajroy/Downloads/clustalw-2.1-linux-x86_64-libcppstatic/clustalw2"
fasta_dir = "/home/rajroy/Downloads/fasta_dictionary.txt"
four_letter_protein_name_file = "/home/rajroy/protein_names_4_letters.txt"
five_letter_protein_name_file = "/home/rajroy/protein_names_5_letters.txt"
# homo_file = "/media/rajroy/fbc3794d-a380-4e0f-a00a-4db5aad57e75/rajroy/back_up/input_files/DIMERS/contact_info" \
#             "/contact_6/homodimers.txt"
# dimer_file = "/media/rajroy/fbc3794d-a380-4e0f-a00a-4db5aad57e75/rajroy/back_up/input_files/DIMERS/contact_info" \
#              "/contact_6/classified_dimer_in_contact_6.txt"

input_dir = "/home/rajroy/Documents/Clustlw_alignment/input/"

output_dir = "/home/rajroy/Documents/Clustlw_alignment/output/"


def read_pair_file_into_array(_input):
    output_array = []
    file = open(_input, "r")
    if file.mode == 'r':
        output_array = file.read().splitlines()
        file.close()
    return output_array


class protein_in_dimer_classes:
    name = ""
    initial_fasta = ""
    final_fasta = ""
    removed_index = []
    aln_seq_history = []


def string_pair_to_array(_array):
    array = []
    for val in _array:
        temp = val.split(",")
        array.append(temp[0].strip)
        array.append(temp[1].strip)

    return list(dict.fromkeys(array))


def protein_reindex_class():
    name = ""
    hetero = []
    homo = []
    perfect_homo = []
    imperfect_homo = []


def clustalW_cmd(_input, _output):
    final_in = input_dir + _input
    final_out = output_dir + _output
    # "/home/rajroy/Downloads/clustalw-2.1-linux-x86_64-libcppstatic/clustalw2 -INFILE=/home/rajroy/Downloads/input.fasta -ALIGN -OUTFILE=/home/rajroy/cmd_os.fasta"
    cmd = CLUSTALW_dir + " -INFILE=" + final_in + " " + "-ALIGN " + "-OUTFILE=" + final_out
    print(cmd)
    return cmd


def get_connected_nodes(node, visited):
    nodes = set()
    nodes.add(node)
    visited.append(node.name)
    for child in node.homo:
        if node.name != child.split(",")[0]:
            val = child.split(",")[0]
        else:
            val = child.split(",")[1]
        if val not in visited:
            nodes.add(loaded_dimer_stats_dictionary.get(val))
            nodes = nodes.union(get_connected_nodes(loaded_dimer_stats_dictionary.get(val), visited))
    return nodes


def write2file(file, contents):
    with open(file, "w") as f:
        f.writelines(contents)


def loadFastaDictionary(dict_file):
    fasta_dict = {}
    with open(dict_file, "r") as f:
        for line in f:
            fasta_dict[line.strip().split(":")[0].strip()] = line.strip().split(":")[1].strip()
    return fasta_dict


# input_dir = ""
# output_dir = ""
processed_chains = []
loaded_dimer_stats_dictionary = np.load('/home/rajroy/protein_chain_details.npy', allow_pickle='TRUE').item()
occurrences = lambda s, lst: (e for i, e in enumerate(lst) if s in e)
# protein_name_four_letters = np.array(read_pair_file_into_array(four_letter_protein_name_file))
protein_name_five_letters = np.array(read_pair_file_into_array(five_letter_protein_name_file))

fasta_dict = loadFastaDictionary(fasta_dir)

for value in protein_name_five_letters:

    if value not in processed_chains and len(loaded_dimer_stats_dictionary.get(value).homo)>0:

        all_connected_homos = get_connected_nodes(loaded_dimer_stats_dictionary.get(value), [])
        file_out_string = ""
        for val in all_connected_homos:
            processed_chains.append(val.name)
            seq = fasta_dict.get(val.name)
            file_out_string = file_out_string + ">" + val.name + "\n"
            file_out_string = file_out_string + seq + "\n"
        name = value + "_" + "cluster.seq"
        # name = value + "_" + "cluster.seq"
        write2file(input_dir + name, file_out_string)
        os.system(clustalW_cmd(name, name))

        # print(value + " "+str(len(all_connected_homos)))
        # take all of their fasta and write a seq file

        # os system

    # get  dict by chains
    # append in homolist
    # a_chain = loaded_dimer_stats_dictionary.get(value)
    # homo_list_processed.extend(a_chain.homoimer)
    # list= list(occurrences(value, protein_name_five_letters))
    # a_protein_chain = loaded_dimer_stats_dictionary.get(protein)
