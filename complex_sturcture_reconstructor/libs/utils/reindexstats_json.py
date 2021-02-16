import json
import os
import pickle
import sys

import numpy as np

stats_list = []


def loadFastaDictionary(dict_file):
    fasta_dict = {}
    #    i=0
    with open(dict_file, "r") as f:
        for line in f:
            #            i+=1
            fasta_dict[line.strip().split(":")[0].strip()] = line.strip().split(":")[1].strip()

    #    print (len(fasta_dict.keys()),i)
    return fasta_dict


class protein_in_dimer_classes:
    # def __init__(self, _name, _hetero, _homo, _perfect_homo, _imperfect_homo):
    #     self.name = _name
    #     self.hetero = _hetero
    #     self.homo = _homo
    #     self.perfect_homo = _perfect_homo
    #     self.imperfect_homo = _imperfect_homo
    name = ""
    hetero = []
    homo = []
    perfect_homo = []
    imperfect_homo = []


def read_pair_file_into_array(_input):
    output_array = []
    file = open(_input, "r")
    if file.mode == 'r':
        output_array = file.read().splitlines()
        file.close()
    return output_array


def dimer_number_stats(_stats_list):
    outstring = ""
    counter = 0
    for val in stats_list:
        outstring = outstring + val.name + ',' + str(len(val.hetero)) + ',' + str(len(val.homo)) + "," + str(len(
            val.perfect_homo)) + "," + str(len(val.imperfect_homo)) + "\n"
        counter = counter + 1
        print("stat_list " + str(counter))
        # if counter > 100:
        #     print("stat_list " + str(counter))
    write2file("/home/rajroy/dimer_stats.txt", outstring)


def protein_name_four_letter_generateor():
    protein_name_four_letters = []
    for val in homo_list:
        temp = val.split(',')
        protein_name_four_letters.append(temp[0][0:4])
        protein_name_four_letters.append(temp[1][0:4])
    for val in hetero_file:
        temp = val.split(',')
        protein_name_four_letters.append(temp[0][0:4])
        protein_name_four_letters.append(temp[1][0:4])
    print(len(protein_name_four_letters))
    protein_name_four_letters = list(dict.fromkeys(protein_name_four_letters))
    print(len(protein_name_four_letters))
    str_out = ""
    for val in protein_name_four_letters:
        str_out = str_out + val + "\n"
    # write2file("/home/rajroy/protein_names_4_letters.txt", str_out)


def write2file(file, contents):
    with open(file, "w") as f:
        f.writelines(contents)


def get_object_string(_temp):
    new_temp = protein_in_dimer_classes()
    new_temp = _temp

    out_string = "name:"
    out_string = out_string + new_temp.name + ","

    # hetero
    out_string = out_string + "hetero:"
    out_string = out_string + "["
    heter_counter_len = len(new_temp.hetero)
    for val in new_temp.hetero:
        if new_temp.hetero.index(val) < heter_counter_len - 1:
            out_string = out_string + val + ","
        else:
            out_string = out_string + val
    out_string = out_string + "],"

    # homo
    out_string = out_string + "homo:"
    out_string = out_string + "["
    homo_counter_len = len(new_temp.homo)
    for val in new_temp.homo:
        if new_temp.homo.index(val) < homo_counter_len - 1:
            out_string = out_string + val + ","
        else:
            out_string = out_string + val
    out_string = out_string + "],"

    # perfect
    out_string = out_string + "perfect:"
    out_string = out_string + "["
    perfect_counter_len = len(new_temp.perfect_homo)
    for val in new_temp.perfect_homo:
        if new_temp.perfect_homo.index(val) < perfect_counter_len - 1:
            out_string = out_string + val + ","
        else:
            out_string = out_string + val
    out_string = out_string + "],"

    out_string = out_string + "imperfect:"
    imperfect_counter_len = len(new_temp.imperfect_homo)
    out_string = out_string + "["
    for val in new_temp.imperfect_homo:
        if new_temp.imperfect_homo.index(val) < imperfect_counter_len - 1:
            out_string = out_string + val + ","
        else:
            out_string = out_string + val
    out_string = out_string + "]"

    return out_string + "\n"


def get_stats(_name):
    out_string = ""
    temp_val = protein_in_dimer_classes()
    temp_val.name = _name
    occurrences = lambda s, lst: (e for i, e in enumerate(lst) if s in e)
    temp_val.homo = list(occurrences(_name, homo_list))
    temp_val.hetero = list(occurrences(_name, hetero_list))
    temp_val.perfect_homo = list(occurrences(_name, perfect_list))
    temp_val.imperfect_homo = list(occurrences(_name, imperfect_list))
    stats_list.append(temp_val)
    alpha_string.append(get_object_string(temp_val))

    print("process_list " + str(len(stats_list)))
    return alpha_string


# dimer_file = "/media/rajroy/fbc3794d-a380-4e0f-a00a-4db5aad57e75/rajroy/back_up/input_files/DIMERS/contact_info" \
#              "/contact_6/classified_dimer_in_contact_6.txt"
# # seq_file = "/media/rajroy/fbc3794d-a380-4e0f-a00a-4db5aad57e75/rajroy/back_up/input_files/DIMERS/seq_aln_dictionary.txt"
# homo_file = "/media/rajroy/fbc3794d-a380-4e0f-a00a-4db5aad57e75/rajroy/back_up/input_files/DIMERS/contact_info" \
#             "/contact_6/homodimers.txt"
# hetero_file = "/media/rajroy/fbc3794d-a380-4e0f-a00a-4db5aad57e75/rajroy/back_up/input_files/DIMERS/contact_info" \
#               "/contact_6/hetero.txt"
# imperfect_file = "/media/rajroy/fbc3794d-a380-4e0f-a00a-4db5aad57e75/rajroy/back_up/input_files/DIMERS/contact_info" \
#                  "/contact_6/homo_95.txt"
# perfect_file = "/media/rajroy/fbc3794d-a380-4e0f-a00a-4db5aad57e75/rajroy/back_up/input_files/DIMERS/contact_info" \
#                "/contact_6/perfect.txt"
# # four_letter_protein_name_file = "/home/rajroy/protein_names_4_letters.txt"
# five_letter_protein_name_file = "/home/rajroy/protein_names_5_letters.txt"
# OUTPUT_DIR=
dimer_file = sys.argv[1]
# seq_file = "/media/rajroy/fbc3794d-a380-4e0f-a00a-4db5aad57e75/rajroy/back_up/input_files/DIMERS/seq_aln_dictionary.txt"
homo_file = sys.argv[2]
hetero_file = sys.argv[3]
perfect_file = sys.argv[4]
imperfect_file = sys.argv[5]

# four_letter_protein_name_file = "/home/rajroy/protein_names_4_letters.txt"
five_letter_protein_name_file = sys.argv[6]
OUTPUT_DIR=sys.argv[7]

# alll_ist only contact
all_dimer_list = np.array(read_pair_file_into_array(dimer_file))
# # seq_dict
# seq_dict = loadFastaDictionary(seq_file)
# homo_list
homo_list = np.array(read_pair_file_into_array(homo_file))
# hetaro_list
hetero_list = np.array(read_pair_file_into_array(hetero_file))
# perfect
perfect_list = np.array(read_pair_file_into_array(perfect_file))
# imperfect
imperfect_list = np.array(read_pair_file_into_array(imperfect_file))
# 4list
# protein_name_four_letters = np.array(read_pair_file_into_array(four_letter_protein_name_file))
# 5List
protein_name_five_letters = np.array(read_pair_file_into_array(five_letter_protein_name_file))

# occurrences = lambda s, lst: (e for i,e in enumerate(lst) if s in  e)
# list(occurrences("1", ["1","2","3","1"]))

# homo_list_atom = [i for i, x in enumerate(homo_list) if  "11BAA" in x]
# print(homo_list_atom)
#


import concurrent.futures
import time

alpha_string = []
stats_list = []
# filer = protein_name_five_letters[0:100]
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     # first parameter is the method name and second is the input
#     results = executor.map(get_stats, filer)
#
# print_string =""
# alpha_string =results.gi_frame.f_locals['iterable'].gi_frame.f_locals['fs']
# for val in alpha_string:
#     print_string = print_string + val._result[0][0]+"\n"
print_string = ""
my_dictionary = {}
counter = 0
for val in protein_name_five_letters:
    temp_val = protein_in_dimer_classes()
    temp_val.name = val
    occurrences = lambda s, lst: (e for i, e in enumerate(lst) if s in e)
    temp_val.homo = list(occurrences(val, homo_list))
    temp_val.hetero = list(occurrences(val, hetero_list))
    temp_val.perfect_homo = list(occurrences(val, perfect_list))
    temp_val.imperfect_homo = list(occurrences(val, imperfect_list))
    stats_list.append(temp_val)
    my_dictionary[val] = temp_val
    counter = counter+1
    print (counter)
    # print(json.dumps(temp_val.__dict__))
    # alpha_string.append(get_object_string(temp_val))

print_string = ""
# json_print = "["+"\n"
# for val in alpha_string:
#
#     print_string=print_string+val
# json_print= json_print+str(val.__dict__)
# json_print=json_print+"\n,"
# print_string = print_string + val
#
# json_print =json_print+ "]"
#
np.save(OUTPUT_DIR+'/protein_chain_details.npy', my_dictionary)
# np.save('/home/rajroy/protein_chain_details.npy', my_dictionary)
# write2file("/home/rajroy/protein_chain_details.txt", print_string)
# write2file("/home/rajroy/protein_chain_details.json", json_print)
# f = open("file.pkl","wb")
# pickle.dump(my_dictionary,f)
# f.close()
dimer_number_stats(stats_list)
# load_dimer = np.load('/home/rajroy/protein_chain_details.npy', allow_pickle='TRUE').item()
# val = load_dimer.get('1A0HD')
# print(val.perfect_homo)
# print(val.homo)
# print(val.imperfect_homo)
# print(len(val.hetero))
#
# val2 = load_dimer.get('1A0FFHD')
# print(val2)
# dict = eval(open("/home/rajroy/protein_chain_details.txt").read())
# sample = loadFastaDictionary("/home/rajroy/protein_chain_details.txt")
# sample.get('11BGA')
