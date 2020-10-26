import importlib
import re
import time
import glob
import copy
import os
import sys
from pathlib import Path

custom_libraries = importlib.util.spec_from_file_location("existing_contact_finder_hetero", str(Path(__file__).parent.absolute())+"/config.py")
config = importlib.util.module_from_spec(custom_libraries)
custom_libraries.loader.exec_module(config)

_target_id = sys.argv[1]
_pdb_list_file = sys.argv[2]
_res_list_file = sys.argv[3]
_output_file = sys.argv[4]
# _target_id = 'example'
# _pdb_list_file = "/home/rajroy/pdb_list.txt"
# _res_list_file = '/home/rajroy/res_list.txt'
# _output_file ='/home/rajroy/'+str(_target_id+str('ss'))
# for Calla


CNS_DIRECTORY = config.CNS_DIRECTORY
MODEL_COUNT = config.MODEL_COUNT

def main():
    _model_count = MODEL_COUNT
    if not os.path.isfile(_pdb_list_file):
        print("PDB List File does not exist " + str(_pdb_list_file) + "\n")
        sys.exit()
    if not os.path.isfile(_res_list_file):
        print("Restrain List File does not exist" + str(_res_list_file) + "\n")
        sys.exit()

    output_file = _output_file + '/' + str(_target_id) + '/'
    if not os.path.exists(output_file):
        os.system("mkdir -p " + output_file + '\n')
    else:
        print(output_file + '\n')
    cns_dir = CNS_DIRECTORY
    if not os.path.exists(cns_dir):
        print(cns_dir)
        print("CNS Directory not found " + "\n")
        sys.exit()

    print("Fetching the Restrain List" + '\n')
    res_dict = config.restrain_config.get_res_dict(_res_list_file)
    input_dir_name = output_file + '/input/'
    print('Creating input folder \n')
    os.system("mkdir -p " + input_dir_name + '\n')

    print("Fetching the PDB List" + '\n')
    pdb_dict = config.pdb_config.get_pdb_dict(_pdb_list_file)



    input_dir_name = output_file + '/input/'
    for key in pdb_dict:
        print(pdb_dict.get(key) + str(" is being copied to ") + str(input_dir_name + key  ) + "\n")
        os.system('cp ' + pdb_dict.get(key) + ' ' + input_dir_name + key)

    for key in res_dict:
        print(res_dict.get(key) + str(" is being copied to ") + str(
            input_dir_name + os.path.basename(res_dict.get(key))) + "\n")
        os.system('cp ' + res_dict.get(key) + ' ' + input_dir_name + os.path.basename(res_dict.get(key)))

    # Clean_pdb
    # Read check chain insert chain
    temp_models = []
    for key in pdb_dict:
        config.pdb_config.contents_to_info(config.pdb_config.read_pdb(input_dir_name + key))
        temp_model = config.pdb_config.add_chain(config.pdb_config.contents_to_info(config.pdb_config.read_pdb(input_dir_name + key )),
                               key.split("_")[len(key.split("_")) - 1].split(".")[0])
        temp_models.extend(temp_model)

    config.pdb_config.fix_serial(temp_models, 1)
    merged_pdb_name = output_file + str('cns_format.pdb')
    config.pdb_config.convert_to_cns(temp_models, merged_pdb_name)

    # mkdir initialzaion
    initialization_dir = output_file + 'initialization/'
    os.system("mkdir -p " + initialization_dir)
    print("Restrains files are being created ..."+"\n")
    restrains_string = ""
    for key in res_dict:
        restrains_string = restrains_string +  config.restrain_config.convert_dist_to_restrain(_input_dir=res_dict.get(key), _segment_1=key[0],
                                                                       _segment_2=key[1])
    res_file = initialization_dir + "res.restrains"
    config.restrain_config.write_restrain_file(restrains_string, res_file)
    print('Restrain file created  \n')

    print('file merged  \n')
    docking_dir = output_file + '/docking/'
    print('Initializing docking  \n')
    os.system('mkdir -p ' + docking_dir)
    config.file_handler_config.docking_inp(_input_pdb=merged_pdb_name,
                _restrain_file=res_file, _output_dir=docking_dir, _model_count=_model_count)

    # number can be very few adjust it and add the change things
    config.file_handler_config.job_docking(cns_dir, docking_dir)
    os.system('chmod +x ' + docking_dir + '/job_docking.sh')
    # run the file
    os.chdir(docking_dir)
    start = time.time()
    print('submitting job  \n')
    print('Job will take some hours to complete  \n')
    process_state = os.system('./job_docking.sh')
    print('execution code ' + str(process_state))
    # select low scoring file
    break_val = False

    done = time.time()
    elapsed = done - start
    print(' time elapsed ' + str(elapsed) + '\n')

    # read_file and get value and  keep the track

    os.chdir(docking_dir)
    file_list = []
    for file in glob.glob("docking_*.pdb"):
        if not "start" in file:
            file_list.append(docking_dir + "/" + file)

    details_array_all = config.util_config.docking_details_returner(file_list, docking_dir)

    details_array_all = sorted(details_array_all, key=lambda energy: energy[1])
    if len(details_array_all) < _model_count / 2:
        print('Something went wrong ' + '\n')
        print('Please check if the PDB\'s are overlapping ' + '\n')
        exit()

    # docked_pdb = pdb_reader.contents_to_info(pdb_reader.read_pdb(copy.deepcopy(details_array_all[0][0])))
    top_5 = output_file + '/sorted/'
    os.system('mkdir -p ' + top_5)
    print(' Top 5 file would be saved in ' + str(top_5))
    for counter in range(5):
        os.system('cp ' + details_array_all[counter][0] + ' ' + top_5 + '/' + _target_id + '_' + str(counter) + '.pdb')


if __name__ == "__main__":
    main()
