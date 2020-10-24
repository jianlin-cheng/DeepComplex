#!/usr/bin/env python3

import os
import platform
import sys
import numpy as np
from keras.models import model_from_json

project_root = os.path.dirname(os.path.abspath(sys.argv[0]))
print(project_root)
if not project_root.endswith("/"): project_root += "/"
from lib.DNCON2_library import *
from lib.training_strategy import *


def usage_printer():
    print('Please follow the sample command ' + '\n')
    print(' Python contact_predictor <input feature file > <output feature file >')


def writeToRRFile(pred, filename, L, label_flag=False):
    pred_new = pred[0:L, 0:L]
    np.savetxt(filename + "_matrix.txt", pred_new)
    with open(filename, "w") as f:
        for i in range(L):
            for j in range(L):
                if label_flag:
                    if pred[i][j] == 1.0: f.write(str(i + 1) + " " + str(j + 1) + " 0 6.0 " + str(pred[i][j]) + "\n")
                else:
                    f.write(str(i + 1) + " " + str(j + 1) + " 0 6.0 " + str(pred[i][j]) + "\n")


def read_file(_input):
    output_array = []
    if os.path.isfile(_input):
        _file = open(_input, "r")
        if _file.mode == 'r':
            output_array = _file.read().strip().splitlines()
        _file.close()
    return output_array


current_os_name = platform.platform()
print('%s' % current_os_name)
sysflag = ""
if 'Ubuntu' in current_os_name.split('-'):  # on local
    sysflag = 'local'
elif 'centos' in current_os_name.split('-'):  # on lewis or multicom
    sysflag = 'lewis'
else:
    sysflag = "local"
print("sysflag=", sysflag)

gpu_mem = gpu_schedul_strategy(sysflag, gpu_mem_rate=0.8, allow_growth=True)
project_root = os.path.dirname(os.path.abspath(sys.argv[0]))
print(project_root)

# FEATURE FILE
# feat_file_dir = '/home/rajroy/feat-1A0F.txt'
feat_file_dir = sys.argv[1]
# PROVIDED
outdir = sys.argv[2]
if len(sys.argv) != 3:
    usage_printer()

# MODEL_DIR
model_dir = project_root + '/models/resnet32_with_dilation/'
model = "model_resnet32_with_dilation.json"
# BEST WEIGHTS
best_weights = "weights_resnet32_with_dilation.hdf5"
# LOAD MODEL
print('Loading model ....' + '\n')
json_file = open(model_dir + model, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
print('Loading weights  ....' + '\n')

# load weights into new model
model.load_weights(model_dir + best_weights)

# output directory setup
name = os.path.basename(feat_file_dir).split('.')[0]
final_file = outdir + '/' + name + '/'
#current Model was ran with best max length of 500
print(' Output File Provided at ' + final_file + '\n')
MAX_LENGTH = 500

if not os.path.exists(final_file):
    os.system('mkdir -p ' + final_file)

if not os.path.exists(feat_file_dir):
    print(' Feature file not found')
    exit()

X = get_x_from_this_file(feat_file_dir, MAX_LENGTH)
lenght_of_seq = X.shape[1]
print('Sequence of length ' + str(lenght_of_seq) + '\n')
print("Getting X-features from  " + feat_file_dir)

print('len ' + str(lenght_of_seq) + '\n')
if lenght_of_seq <= MAX_LENGTH:
    print("X.shape=", X.shape)
    P = model.predict([X], batch_size=1)
    P = P.squeeze().reshape(MAX_LENGTH, MAX_LENGTH)
    filename = final_file + name + "_predicted.rr"
    writeToRRFile(P, filename, L=lenght_of_seq)
    if os.path.exists(filename):
        print('[ Finished Successfully ] : Output is locatied at ' + str(filename))
    else:
        print(' Something went wrong ')
else:
    print('It can now only work with lenght less than or equal to ' + str(MAX_LENGTH))
