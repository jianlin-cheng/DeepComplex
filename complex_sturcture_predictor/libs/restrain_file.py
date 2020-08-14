import importlib
import os
import sys
from pathlib import Path
import re
util_library = importlib.util.spec_from_file_location("utils", str(Path(__file__).parent.absolute().parent)+"/libs/utils.py")
util_config = importlib.util.module_from_spec(util_library)
util_library.loader.exec_module(util_config)



def convert_dist_to_restrain(_input_dir, _segment_1, _segment_2):
    if not os.path.isfile(_input_dir):
        print(_input_dir, " does not exist.")
        sys.exit(1)

    file_content_array = []
    for y in util_config.file_array_return(_input_dir).split("\n"):
        if len(y.strip()) > 0:
            match = re.search("\D", y[0])
            if not match:
                temp_array = y.split(' ')
                dist_array = [temp_array[0], temp_array[1], temp_array[2], temp_array[3], temp_array[4]]
                file_content_array.append(dist_array)
    string_res = ""
    for values in file_content_array:
        string_res = string_res + "       assign ( resid " + values[0] + " and segid " + str(
            _segment_1) + " ) " + " ( resid " + \
                     str(values[1]) + " and segid " + str(_segment_2) + " ) " + "6.0" + " 1.0 1.0 " + "\n"

    return string_res
    # write_restrain_file(_input_dir, file_content_array, _segment_1, _segment_2, _output_dir)

def get_res_dict(_input):
    res_dict = {}
    temp = util_config.read_file_lines(_input_file=_input)
    for res in temp:
        if len(res.strip()) > 0:
            if os.path.isfile(res):
                res_base_name = os.path.basename(res)
                res_chain_name = res_base_name.split("_")[len(res_base_name.split("_")) - 1].split(".")[0]
                res_dict[res_chain_name] = res
            else:
                print("This restrain file " + str(res) + " not found")
                exit()
    return res_dict

def write_restrain_file(_array, _output_dir):
    # name_of_file = _input_dir.split('/')
    # dir_str = "/"
    # i = 0
    # while len(name_of_file) - 1 > i:
    #     dir_str = dir_str + name_of_file[i] + "/"
    #     i = i + 1

    f = open(_output_dir, "w")

    f.write("noe" + "\n")
    f.write("   nres=500000" + "\n")
    f.write("   class inter" + "\n")
    f.write("   ceiling=1000" + "\n")
    f.write("   averaging inter cent" + "\n")
    f.write("   potential inter square" + "\n")
    f.write("   sqconstant inter 1." + "\n")
    f.write("   sqexponent inter 2" + "\n")
    f.write("   scale inter 50." + "\n")
    f.write("{ remarks: segid A is synaptobrevin, segid B is syntaxin, segid C,D is SNAP-25 , segid S is "
            "synaptotagmin }" + "\n")
    f.write(" { assign <selection> <selection> distance dminus dplus }" + "\n")
    f.write("   { FRET pairs near Ro}" + "\n")
    f.write(_array + "\n")
    f.write("end")
    f.close()


def dist_file_reader(_dist_file):
    file_content_array = []
    for y in util_config.file_array_return(_dist_file).split("\n"):
        temp_array = []
        if len(y.split(' ')) == 5:
            temp_array.append(y.split(' '))

            file_content_array.append(temp_array)
    return file_content_array


