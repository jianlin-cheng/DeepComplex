import copy
import os
import time

from Bio import pairwise2
import re


class protein_in_dimer_classes:
    name = ""
    old_fasta = ""
    aligned_fasta = ""
    new_fasta = ""
    index_to_remove = []


class pdb_lines:
    atom = ''
    serial = ''
    atom_name = ''
    alt_loc = ''
    res_name = ''
    chain = ''
    res_num = ''
    icode = ''
    x = ''
    y = ''
    z = ''
    occupancy = ''
    temp_fact = ''
    element = ''
    charge = ''

    pass


def split_line_to_tuple(line):
    a_pdb_line = pdb_lines()

    a_pdb_line.atom = line[0:6].strip()
    a_pdb_line.serial = line[6:12].strip()
    a_pdb_line.atom_name = line[12:16].strip()
    a_pdb_line.alt_loc = line[16].strip()
    a_pdb_line.res_name = line[17:20]  # for this not parsing everything as not needed
    a_pdb_line.chain = line[20:22].strip()
    a_pdb_line.res_num = line[22:26].strip()
    a_pdb_line.icode = line[26:30].strip()
    a_pdb_line.x = line[30:38].strip()
    a_pdb_line.y = line[38:46].strip()
    a_pdb_line.z = line[46:54].strip()
    a_pdb_line.occupancy = line[54:60].strip()
    # a_pdb_line.temp_fact = line[60:76].strip()
    a_pdb_line.temp_fact = line[60:66].strip()
    a_pdb_line.element = line[76:78].strip()
    a_pdb_line.charge = line[78:80].strip()

    return a_pdb_line


def convert_to_pdb(_pdb, _name):
    content = ''
    for x in _pdb:
        content += correct_format(x) + '\n'
    # f = open(_name, "w")
    # f.write(content)
    # f.close()
    return content + "END"


def space_returner(_input):
    i = 0
    space = ""
    while i < _input:
        space = space + " "
        i = i + 1
    return space


def read_pdb(pdb):
    contents = []
    with open(pdb, "r") as f:
        for line in f:
            # if (line.startswith("ATOM")):
            #    pass
            contents.append(line)
    return contents


def contents_to_info(contents):  # reads the ATOM line. Then splits the info into respective frames and returns the data
    split_contents = []
    for lines in contents:
        if lines.startswith("ATOM"):
            pdb_line = split_line_to_tuple(lines.strip())
            split_contents.append(pdb_line)
    return split_contents

def correct_format(_pdb_row):
    _pdb_copy = copy.deepcopy(_pdb_row)
    # https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
    _pdb_copy.atom = _pdb_copy.atom  # 1-4
    _pdb_copy.serial = space_returner(5 - len(str(_pdb_copy.serial))) + _pdb_copy.serial  # 7-11
    _pdb_copy.atom_name = _pdb_copy.atom_name + space_returner(3 - len(_pdb_copy.atom_name))  # 13-16
    _pdb_copy.alt_loc = space_returner(1 - len(_pdb_copy.alt_loc)) + _pdb_copy.alt_loc  # 17
    _pdb_copy.res_name = _pdb_copy.res_name  # 18-20
    _pdb_copy.chain = space_returner(1 - len(_pdb_copy.chain)) + _pdb_copy.chain  # 22
    _pdb_copy.res_num = space_returner(4 - len(_pdb_copy.res_num)) + _pdb_copy.res_num  # 23-26
    _pdb_copy.icode = space_returner(2 - len(_pdb_copy.chain)) + _pdb_copy.icode  # 27
    _pdb_copy.x = space_returner(8 - len(_pdb_copy.x)) + _pdb_copy.x  # 31-38
    _pdb_copy.y = space_returner(8 - len(_pdb_copy.y)) + _pdb_copy.y  # 39-46
    _pdb_copy.z = space_returner(8 - len(_pdb_copy.z)) + _pdb_copy.z  # 47-54
    _pdb_copy.occupancy = space_returner(6 - len(_pdb_copy.occupancy)) + _pdb_copy.occupancy  # 55-60
    _pdb_copy.temp_fact = space_returner(6 - len(_pdb_copy.temp_fact)) + _pdb_copy.temp_fact  # 61-66
    _pdb_copy.element = space_returner(4 - len(_pdb_copy.element)) + _pdb_copy.element  # 73-76
    _pdb_copy.charge = space_returner(2 - len(_pdb_copy.charge)) + _pdb_copy.charge  # 77-78
    content = _pdb_copy.atom + space_returner(2) + _pdb_copy.serial

    if len(_pdb_copy.atom_name) < 4:
        content = content + space_returner(2) + _pdb_copy.atom_name
    elif len(_pdb_copy.atom_name) == 4:
        content = content + " " + _pdb_copy.atom_name

    content = content + _pdb_copy.alt_loc + _pdb_copy.res_name + space_returner(
        1) + _pdb_copy.chain + _pdb_copy.res_num + _pdb_copy.icode + space_returner(
        3) + _pdb_copy.x + _pdb_copy.y + _pdb_copy.z + _pdb_copy.occupancy + _pdb_copy.temp_fact + space_returner(
        8) + _pdb_copy.element + _pdb_copy.charge

    return content

def write2file(file, contents):
    with open(file, "w") as f:
        f.writelines(contents)

import numpy as np

input_dir = "/home/rajroy/reindexed_good_but_four_failedcase/"
output_dir = "/home/rajroy/redo_reindexing/"
removed_alternated_sequence = "/media/rajroy/fbc3794d-a380-4e0f-a00a-4db5aad57e75/rajroy/back_up/input_files/DIMERS" \
                              "/dimers/pdb_alt_seq_removed/"

if not os.path.exists(output_dir):
    os.system("mkdir -p " + output_dir + '\n')

dimer_reindex_info_dictionary = np.load(input_dir + 'reindex_fasta.npy', allow_pickle='TRUE').item()
count = 0
miss_str = ""

for val in dimer_reindex_info_dictionary:
    print(count)
    count=count+1
    a_protein = dimer_reindex_info_dictionary.get(val)

    # get the pdb  removed alternating sequence ones
    pdb_name = removed_alternated_sequence + a_protein.name + ".atom"
    # read
    # check path
    if os.path.isfile(pdb_name):

        number_to_del_from_pdb = []
        # remove the indices remover +1
        if len(a_protein.index_to_remove) > 0:
            for indexes in a_protein.index_to_remove:
                indexes = int(indexes) + 1
                number_to_del_from_pdb.append(indexes)
            pdb = contents_to_info(read_pdb(pdb_name))
            # so that
            deleted_res = []
            last_res_number = 0
            filter_pdb = []
            serial = 1
            for rows in pdb:

                # if last_res_number in number_to_del_from_pdb:
                    #print(last_res_number)
                # if not match cool  just reduce the num of the value
                if int(rows.res_num) not in deleted_res:
                    # check if already all checked
                    if len(number_to_del_from_pdb) > len(deleted_res):
                        number_to_compare = number_to_del_from_pdb[len(deleted_res)]
                    else:
                        # no need to check so high number
                        number_to_compare = 99999
                    # compare current number with number to compare
                    if int(rows.res_num) != number_to_compare:
                        temp_row = copy.deepcopy(rows)
                        temp_row.serial = str(serial)
                        temp_row.res_num = str(int(temp_row.res_num) - len(deleted_res))
                        filter_pdb.append(temp_row)
                        serial = serial + 1
                    else:
                        if last_res_number not in deleted_res:
                            deleted_res.append(number_to_del_from_pdb[len(deleted_res)])
                last_res_number = int(rows.res_num)

            new_pdb = convert_to_pdb(filter_pdb, a_protein.name)
            # print(len(pdb))
            f = open( output_dir+a_protein.name+".pdb" , "w")
            f.write(new_pdb)
            f.close()
        else:
            os.system("cp " + pdb_name + " " + output_dir+a_protein.name+".pdb")
    else:
        print(pdb_name)
        miss_str=miss_str+pdb_name+"\n"
        print("missing")
write2file("/home/rajroy/missing_files.txt",miss_str)
    # reindex serial number and using skip count
    # atom_no
    # output dir
