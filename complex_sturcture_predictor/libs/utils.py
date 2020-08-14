
def space_returner(_input):
    i = 0
    space = ""
    while i < _input:
        space = space + " "
        i = i + 1
    return space

def read_file_lines(_input_file):
    output_array = []
    copy_file = open(_input_file, "r")

    if copy_file.mode == 'r':
        output_array = copy_file.read().splitlines()
        copy_file.close()
    return output_array



def file_reader(_input_dir):
    f = open(_input_dir, "r")
    if f.mode == 'r':
        contents = f.read()
        f.close()
    return contents


def docking_details_returner(_file_list, _output_file):
    details_array_all = []
    for x in _file_list:
        f = open(x, "r")
        if f.mode == 'r':
            contents = f.read()
            f.close()
        details_array = []
        for item in contents.split("\n"):
            if "Etotal=" in item:
                e_total = item.strip().split("=")[1].strip().split(" ")[0]
                details_array.append(x)
                details_array.append(float(e_total))
            if "Enoe=" in item:
                e_noe = item.strip().split("=")[2].strip().split(" ")[0]
                details_array.append(float(e_noe))
            if "rmsd bonds==" in item:
                rmsd_bonds = item.strip().split("=")[1].strip().split(" ")[0]
                details_array.append(float(rmsd_bonds))
            if "rmsd angles=" in item:
                rmsd_angles = item.strip().split("=")[2].strip().split(" ")[0]
                details_array.append(float(rmsd_angles))
                details_array_all.append(details_array)
                break
    return details_array_all


def file_array_return(_input_dir):
    output_array = []
    true_distance_file = open(_input_dir, "r")

    if true_distance_file.mode == 'r':
        output_array = true_distance_file.read()
        true_distance_file.close()
    return output_array