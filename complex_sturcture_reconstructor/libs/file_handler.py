import os
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.absolute().parent
prog_dir = str(parent_dir)+"/libs/"
def file_array_return(_input_dir):
    output_array = []
    true_distance_file = open(_input_dir, "r")

    if true_distance_file.mode == 'r':
        output_array = true_distance_file.read()
        true_distance_file.close()
    return output_array


def write_restrain_file(_input_dir, _array, _segment_1, _segment_2, _output_dir):
    name_of_file = _input_dir.split('/')
    dir_str = "/"
    i = 0
    while len(name_of_file) - 1 > i:
        dir_str = dir_str + name_of_file[i] + "/"
        i = i + 1

    f = open(_output_dir, "w")
    val = 0
    f.write("noe" + "\n")
    f.write("   nres=5000" + "\n")
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
    for values in _array:
        f.write("       assign ( resid " + values[0] + " and segid " + str(_segment_1) + " ) " + " ( resid " + values[
            1] + " and segid " + str(_segment_2) + " ) " +
                "6.0" + " 1.0 1.0 " + "\n")
        val = val + 1
    f.write("end")
    f.close()


def convert_dist_to_restrain(_input_dir, _segment_1, _segment_2, _output_dir):
    if not os.path.isfile(_input_dir):
        print(_input_dir, " does not exist.")
        sys.exit(1)

    file_content_array = []
    for y in file_array_return(_input_dir).split("\n"):
        if 32 > len(y) > 0:
            temp_array = y.split(' ')
            dist_array = [temp_array[0], temp_array[1], temp_array[2], temp_array[3], temp_array[4]]
            file_content_array.append(dist_array)
    write_restrain_file(_input_dir, file_content_array, _segment_1, _segment_2, _output_dir)


def docking_inp_file():
    f = open("docking_inp.txt", "r")
    if f.mode == 'r':
        contents = f.read()
        f.close()
    return contents

def file_reader(_input_dir):
    f = open(_input_dir, "r")
    if f.mode == 'r':
        contents = f.read()
        f.close()
    return contents

def docking_inp(_input_pdb, _fixed_chain,_fixed_moving_chain, _restrain_file,_output_dir,_model_count):
    final_content = ''
    f = open('docking_inp.txt', "r")
    if f.mode == 'r':
        content= f.read()
        f.close()
    final_content = content.replace('_coordinate_file_replace_',_input_pdb) #replace pdb    _coordinate_file_replace_
    final_content = final_content.replace('_restrains_file_', _restrain_file)# restrains    _restrains_file_
    final_content = final_content.replace('_fixed_atom_replace_', _fixed_chain) #fixed atom place _fixed_atom_replace_
    final_content = final_content.replace('_fixed_moving_replace_', _fixed_moving_chain) #fixed atom place _fixed_atom_replace_
    final_content = final_content.replace('_model_count_replace_', str(_model_count)) #fixed atom place _fixed_atom_replace_
    fw = open(_output_dir+'docking.inp', "w")
    fw.write(final_content)
    fw.close()


def docking_inp_file():
    f = open("docking_inp.txt", "r")
    if f.mode == 'r':
        contents = f.read()
        f.close()
    return contents





def job_docking(_cns_solve_dir, _output_dir):
    content = file_reader(prog_dir + '/' + 'job_docking.txt')
    final_content = content.replace('_cns_solve_source_replace_',
                                    _cns_solve_dir)  # replace source   _cns_solve_source_replace_
    final_content = final_content.replace('_output_file_directory_replace_',
                                          _output_dir)  # restrains    _output_file_directory_replace_
    fw = open(_output_dir + 'job_docking.sh', "w")
    fw.write(final_content)
    fw.close()

def docking_inp(_input_pdb, _restrain_file, _output_dir,
                _model_count):
    final_content = ''
    f = open(prog_dir + '/' + 'docking_inp.txt', "r")
    if f.mode == 'r':
        content = f.read()
        f.close()
    final_content = content.replace('_coordinate_file_replace_', _input_pdb)  # replace pdb    _coordinate_file_replace_
    final_content = final_content.replace('_restrains_file_', _restrain_file)  # restrains    _restrains_file_

    final_content = final_content.replace('_model_count_replace_',
                                          str(_model_count))  # fixed atom place _fixed_atom_replace_
    fw = open(_output_dir + 'docking.inp', "w")
    fw.write(final_content)
    fw.close()


def main():
    print("dist to restrain called")


if __name__ == '__main__':
    main()
