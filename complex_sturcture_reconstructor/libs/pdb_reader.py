import copy
import importlib
import os
import sys
import math
from pathlib import Path


util_library = importlib.util.spec_from_file_location("utils", str(Path(__file__).parent.absolute())+"/utils.py")
util_config = importlib.util.module_from_spec(util_library)
util_library.loader.exec_module(util_config)



pdb_class = importlib.util.spec_from_file_location("pdb_line_class", str(Path(__file__).parent.absolute().parent) + "/classes/pdb_lines.py")
pdb_class_config = importlib.util.module_from_spec(pdb_class)
pdb_class.loader.exec_module(pdb_class_config)

def get_name(file):
    return file.split("/")[-1][0:4]


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
        print(lines)
        if lines.startswith("ATOM"):
            pdb_line = split_line_to_tuple(lines.strip())
            split_contents.append(pdb_line)
    return split_contents


def add_chain(pdb, val):
    for pdb_line in pdb:
        pdb_line.chain = str(val)
    return pdb


def remove_chain(pdb):
    for pdb_line in pdb:
        pdb_line.chain = ''
    return pdb


def write2File(_filename, _cont):
    with open(_filename, "w") as f:
        f.writelines(_cont)
        if _cont[len(_cont) - 1].strip() != "END":
            f.write("END")
    return


def separate_by_chain(_pdb, _name):
    result = list(filter(lambda x: (x.chain == _name), _pdb))
    return result



def correct_format(_pdb_row):
    _pdb_copy = copy.deepcopy(_pdb_row)
    # https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
    _pdb_copy.atom = _pdb_copy.atom  # 1-4
    _pdb_copy.serial = space_returner(5 - len(str(_pdb_copy.serial))) + str(_pdb_copy.serial)  # 7-11
    _pdb_copy.atom_name = _pdb_copy.atom_name + space_returner(3 - len(_pdb_copy.atom_name))  # 13-16
    _pdb_copy.alt_loc = space_returner(1 - len(_pdb_copy.alt_loc)) + _pdb_copy.alt_loc  # 17
    _pdb_copy.res_name = space_returner(3 - len(_pdb_copy.res_name)) + _pdb_copy.res_name  # 18-20
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

def space_returner(_input):
    i = 0
    space = ""
    while i < _input:
        space = space + " "
        i = i + 1
    return space


def convert_to_pdb(_pdb, _name):
    content = ''
    for x in _pdb:
        content += correct_format(x) + '\n'
    f = open(_name, "w")
    f.write(content)
    f.close()
    return _pdb


def get_name(file):
    return file.split("/")[-1][0:4]


def read_pdb(pdb):
    contents = []
    with open(pdb, "r") as f:
        for line in f:
            # if (line.startswith("ATOM")):
            #    pass
            contents.append(line)
    return contents



    return a_pdb_line

def contents_to_info(contents):  # reads the ATOM line. Then splits the info into respective frames and returns the data
    split_contents = []
    for lines in contents:
        if lines.startswith("ATOM"):
            pdb_line = split_line_to_tuple(lines.strip())
            split_contents.append(pdb_line)
    return split_contents


def split_line_to_tuple(line):
    a_pdb_line = pdb_class_config.pdb_lines()

    a_pdb_line.atom = line[0:6].strip()
    a_pdb_line.serial = line[6:12].strip()
    a_pdb_line.atom_name = line[12:16].strip()
    a_pdb_line.alt_loc = line[16].strip()
    a_pdb_line.res_name = line[17:20].strip()
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

    return  a_pdb_line
# cns format

def convert_to_cns_format(_pdb_row):
    _pdb_copy = copy.deepcopy(_pdb_row)
    # https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
    _pdb_copy.atom = _pdb_copy.atom  # 1-4
    _pdb_copy.serial = space_returner(5 - len(str(_pdb_copy.serial))) + str(_pdb_copy.serial)  # 7-11
    _pdb_copy.atom_name = _pdb_copy.atom_name + space_returner(3 - len(_pdb_copy.atom_name))  # 13-16
    _pdb_copy.alt_loc = space_returner(1 - len(_pdb_copy.alt_loc)) + _pdb_copy.alt_loc  # 17
    _pdb_copy.res_name = space_returner(3 - len(_pdb_copy.res_name)) + _pdb_copy.res_name  # 18-20
    _pdb_copy.chain = space_returner(1 - len(_pdb_copy.chain)) + _pdb_copy.chain  # 22
    _pdb_copy.res_num = space_returner(4 - len(_pdb_copy.res_num)) + _pdb_copy.res_num  # 23-26
    _pdb_copy.icode = space_returner(2 - len(_pdb_copy.chain)) + _pdb_copy.icode  # 27
    _pdb_copy.x = space_returner(8 - len(_pdb_copy.x)) + _pdb_copy.x  # 31-38
    _pdb_copy.y = space_returner(8 - len(_pdb_copy.y)) + _pdb_copy.y  # 39-46
    _pdb_copy.z = space_returner(8 - len(_pdb_copy.z)) + _pdb_copy.z  # 47-54
    _pdb_copy.occupancy = space_returner(6 - len(_pdb_copy.occupancy)) + _pdb_copy.occupancy  # 55-60
    _pdb_copy.temp_fact = space_returner(6 - len(_pdb_copy.temp_fact)) + _pdb_copy.temp_fact  # 61-66
    _pdb_copy.element = _pdb_copy.chain  # 73-76
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


def convert_to_cns(_pdb, _filename):
    # file is outputted
    array = []
    content = ''
    for x in _pdb:
        val = convert_to_cns_format(x)
        array.append(val)
        content = content + val + '\n'
    f = open(_filename, "w")
    f.write(content + 'END')
    f.close()
    return array


def fix_serial(_array, _no=1):
    number = _no
    for x in _array:
        x.serial = number
        number = number + 1
    return _array


def write_to_pdb(_pdb, _file_name):
    content = ''
    for x in _pdb:
        content = content + x + '\n'
    f = open(_file_name, "w")
    f.write(content)
    f.close()
    return _pdb


def if_contains_chain(_pdb):
    for atom in _pdb:
        if len(atom.chain.strip()) > 0:
            return True
        else:
            return False








def calc_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((round(x1, 11) - (round(x2, 11))) ** 2 +
                     (round(y1, 11) - (round(y2, 11)) ** 2) +
                     (round(z1, 11) - (round(z2, 11))) ** 2)



def get_pdb_dict(_input):
    pdb_dict = {}
    temp = util_config.read_file_lines(_input_file=_input)
    for pdb in temp:
        if len(pdb.strip()) >0:
            print(pdb)
            if os.path.isfile(pdb):
                pdb_base_name = os.path.basename(pdb)
                pdb_dict[pdb_base_name] = pdb
            else:
                print("This pdb " + str(pdb) + " not found")
                exit()
    return pdb_dict


def pdb_array_sender(_pdb_file):
    file_content_array = []
    for y in util_config.file_array_return(_pdb_file).split("\n"):
        temp_array = []
        if y.split(' ')[0] != 'REMARK':
            for x in y.split(" "):
                if len(x.strip()) > 0 and x != "ATOM" and x != "\nATOM" and x != "END":
                    temp_array.append(x)

            file_content_array.append(temp_array)
    return file_content_array

