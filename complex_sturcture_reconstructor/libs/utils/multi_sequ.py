import concurrent.futures
import os
import sys
import time

# 65 28 hours
from programs.objective_1.mp_seq_alignment.sequenceAligned import seq_aligner


def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done Sleeping...{seconds}'


def read_pair_file_into_array(_input):
    output_array = []
    file = open(_input, "r")
    if file.mode == 'r':
        output_array = file.read().splitlines()
        file.close()
    return output_array


def loadFastaDictionary(dict_file):
    fasta_dict = {}
    #    i=0
    with open(dict_file, "r") as f:
        for line in f:
            #            i+=1
            fasta_dict[line.strip().split(":")[0].strip()] = line.strip().split(":")[1].strip()

    #    print (len(fasta_dict.keys()),i)
    return fasta_dict


def main_process(_pairs):
    names = _pairs.split(',')
    # x="VVKFTKSEALHKEALEHIVGGVNSPSRSFKAVGGGAPIAERGKGAYFWDVDGNKYIDYLAAYGPIITGHAHPHITKAITTAAENGVLYGTPTALEVKFAKLKEAPALDKVRFVNSGTEAVTTIRVARAYTGRTKIKFAGCYHGHSDLVLVALGTPDSAGVPQSIAQEVITVPFNNVETLKEALDKWGHEVAAILVEPIVGNFGIVEPKPGFLEKVNELVHEAGALVIYDEVITAFRFYGGAQDLLGVTPDLTALGVIGGGLPIGAYGGKKEIEQVAPLGPAYQAGTAGNPASASGIACLEVLQQEGLYEKLDELGATLEKGILEQAAKHNIDITLNRLKGALTVYFTTNTIEDYDAAQDTDGEFGKFFKLLQEGVNLAPSKYEAWFLTTEHTKEDIEYTIEAVGRAFAALADN"
    # y="VVKFTKSEALHKEALEHIVGGVNSPSRSFKAVGGGAPIAERGKGAYFWDVDGNKYIDYLAAYGPIITGHAHPHITKAITTAAENGVLYGTPTALEVKFAKLKEAPALDKVRFVNSGTEAVTTIRVARAYTGRTKIKFAGCYHGHSDLVLVAAGSGPSTLGTPDSAGVPQSIAQEVITVPFNNVETLKEALDKWGHEVAAILVEPIVGNFGIVEPKPGFLEKVNELVHEAGALVIYDEVITAFRFYGGAQDLLGVTPDLTALGVIGGGLPIGAYGGKKEIEQVAPLGPAYQAGTAGNPASASGIACLEVLQQEGLYEKLDELGATLEKGILEQAAKHNIDITLNRLKGALTVYFTTNTIEDYDAAQDTDGEFGKFFKLLQEGVNLAPSKYEAWFLTTEHTKEDIEYTIEAVGRAFAALADNK"

    # mappingfolder = "./reindexed_mapping_function/"  # +pdb_id
    # if not (os.path.isdir(mappingfolder)): os.makedirs(mappingfolder)
    # if not (os.path.isdir("./aligned_seq_folder")): os.makedirs("./aligned_seq_folder")
    print("Print Aligning sequences: ")

    x_key = names[0].split('.')[0]
    y_key = names[1].split('.')[0]
    # print(fasta_dict.get(x_key))
    #
    # print(fasta_dict.get(y_key))
    # cmd = "python sequenceAligned.py " + x_key + " " + fasta_dict.get(x_key) + " " + y_key + " " + fasta_dict.get(
    #     y_key) + " >> aligned_seq_dict.txt"
    # # print(cmd)
    #
    # val = os.system(cmd)
    # print(val)

    if fasta_dict.get(x_key) is not None and fasta_dict.get(y_key) is not None:
        seq_aligner(x_key, y_key, fasta_dict.get(x_key), fasta_dict.get(y_key))
    else:
        cmd_fail = x_key + ' ' + y_key + ' ' + '\n'
        file_object = open('new_failed_cases.txt', 'a')
        file_object.write(cmd_fail)
        file_object.close()

#NECESSARY FILES
# load fasta dict
# fasta_dict = loadFastaDictionary('/home/rajroy/Downloads/experiment_batch/fasta_dictionary.txt')
# # load pair
# pair_array = read_pair_file_into_array('/home/rajroy/Downloads/experiment_batch/pairs.txt')

fasta_dict_path=sys.argv[1]
pair_dimers_path=sys.argv[2]
fasta_dict = loadFastaDictionary(fasta_dict_path)
# load pair

pair_array = read_pair_file_into_array(pair_dimers_path)


len = len(pair_array)
print(len)
counter = 1
start = time.perf_counter()
with concurrent.futures.ProcessPoolExecutor() as executor:
    # secs = [5, 4, 3, 2, 1]
    results = executor.map(main_process, pair_array)

#
# for pa in pair_array:
#     main_process(pa)

done = time.time()
elapsed = done - start
print(' time elapsed ' + str(elapsed) + '\n')
exit()

# for result in results:
#     print(result)

finish = time.perf_counter()

print(f'Finished in {round(finish - start, 2)} second(s)')
