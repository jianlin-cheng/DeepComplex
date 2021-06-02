import shutil
# from libcommon import *
import os, sys, math
import numpy as np
import random

from keras.models import Sequential
from keras.layers import Activation, Flatten
from keras.layers import Convolution2D, Conv2D
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Nadam, Adam
import numpy as np
import math
import os
import sys
import random
import keras.backend as K
# from Model_lib import *
epsilon = K.epsilon()

def get_dncon_2_x_from_this_file(feature_file, max_len=0):
    L = 0
    if max_len==0: 
        with open(feature_file) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                L = line.strip().split()
                L = int(round(math.exp(float(L[0]))))
                max_len=L
                break
    #x = getX(feature_file, L)
    #F = len(x[0, 0, :])
    #X = np.zeros((1, L, L, F))
    x = getX(feature_file, max_len)
    F = len(x[0, 0, :])
    X = np.zeros((1, max_len, max_len, F))
    X[0, :, :, :] = x
    return X
# Training hyperparameters
def read_train_param(file_config):
    if not os.path.isfile(file_config):
        print ('Error! Could not find config file ' + file_config)
        sys.exit(1)
    train_param = {}
    with open(file_config) as f:
        for line in f:
            if line.startswith('#'):
                continue
            if len(line) < 2:
                continue
            cols = line.strip().split()
            if len(cols) < 2:
                print ('Error! Config file ' + file_config + ' line ' + line + '??')
                sys.exit(1)
            if cols[0] == 'optimizer':
                train_param[cols[0]] = cols[1]
            else:
                train_param[cols[0]] = int(cols[1])
    print ('')
    print ('Read training parameters:')
    for k, v in sorted(train_param.items()):
        print ("%-15s : %-3s" %(k, v))
    print ('')
    return train_param


def build_dataset_dictionaries(path_lists):
    length_dict = {}
#    n_dict = {}
#    neff_dict = {}
    with open(path_lists + 'all_training_protein_length.txt') as f:
        for line in f:
            cols = line.strip().split()
            length_dict[cols[0]] = int(cols[1])
#    with open(path_lists + 'N.txt') as f:
#        for line in f:
#            cols = line.strip().split()
#            n_dict[cols[0]] = int(float(cols[1]))
#    with open(path_lists + 'Neff.txt') as f:
#        for line in f:
#            cols = line.strip().split()
#            neff_dict[cols[0]] = int(float(cols[1]))
    tr_l = {}
#    tr_n = {}
#    tr_e = {}
    with open(path_lists + 'train_list.txt') as f:
        for line in f:
            tr_l[line.strip()] = length_dict[line.strip()]
#            tr_n[line.strip()] = n_dict[line.strip()]
#            tr_e[line.strip()] = neff_dict[line.strip()]
    te_l = {}
#    tv_l = {}
    tv_l = {}
#    te_e = {}
    with open(path_lists + 'test_list.txt') as f:
        for line in f:
            te_l[line.strip()] = length_dict[line.strip()]
#            te_n[line.strip()] = n_dict[line.strip()]
#            te_e[line.strip()] = neff_dict[line.strip()]
    with open(path_lists + 'validation_list.txt') as f:
        for line in f:
            tv_l[line.strip()] = length_dict[line.strip()]

    print ('')
    print ('Data counts:')
    print ('Total       : ' + str(len(length_dict)))
    print ('Train       : ' + str(len(tr_l)))
    print ('Test        : ' + str(len(te_l)))
    print ('Validation  : ' + str(len(tv_l)))
    print ('')
    return (tr_l, te_l, tv_l)
    #return (tr_l, te_l, tv_l)

def subset_pdb_dict(dict, minL, maxL, count, randomize_flag):
    selected = {}
    # return a dict with random 'X' PDBs
    if (randomize_flag == 'random'):
        pdbs = list(dict.keys())
        random.shuffle(pdbs)
        i = 0
        for pdb in pdbs:
            if (dict[pdb] >= minL and dict[pdb] <= maxL):
                selected[pdb] = dict[pdb]
                i = i + 1
                if i == count:
                    break
    # return first 'X' PDBs sorted by L
    if (randomize_flag == 'ordered'):
        i = 0
        for key, value in sorted(dict.items(), key=lambda  x: x[1]):
            if (dict[key] > minL and dict[key] <= maxL):
                selected[key] = value
                i = i + 1
                if i == count:
                    break
    return selected
 

def get_x_from_this_list(selected_ids, path, l_max):
    xcount = len(selected_ids)
    sample_pdb = ''
    for pdb in selected_ids:
        sample_pdb = pdb
        break
    if not os.path.exists(path+"X-"+sample_pdb+".txt"):
        x = getX(path + 'feat-'  + sample_pdb + '.txt', l_max)
    else:
        x = getX(path + 'X-'  + sample_pdb + '.txt', l_max)

    F = len(x[0, 0, :])
    print ("L_max=",l_max)
    X = np.zeros((xcount, l_max, l_max, F))
    i = 0
    for pdb in sorted(selected_ids):
        if not os.path.exists(path+"X-"+pdb+".txt"):
            T = getX(path + 'feat-'  + pdb + '.txt', l_max)
        else:
            T = getX(path + 'X-'  + pdb + '.txt', l_max)
        #T = getX(path + 'X-'  + pdb + '.txt', l_max)
        if len(T[0, 0, :]) != F:
            print ('ERROR! Feature length of ' + sample_pdb + ' not equal to ' + pdb)
        X[i, :, :, :] = T
        i = i + 1
    return X

def get_y_from_this_list(selected_ids, path, min_seq_sep, l_max, y_dist):
    xcount = len(selected_ids)
    sample_pdb = ''
    for pdb in selected_ids:
        sample_pdb = pdb
        break
    y = getY(path + 'Y' + y_dist + '-' + sample_pdb + '.txt', min_seq_sep, l_max)
    if (l_max * l_max != len(y)):
        print ('Error!! y does not have L * L feature values!!')
        sys.exit()
    Y = np.zeros((xcount, l_max * l_max))
    i = 0
    for pdb in sorted(selected_ids):
        Y[i, :]       = getY(path + 'Y' + y_dist + '-' + pdb + '.txt', min_seq_sep, l_max)
        i = i + 1

    return Y

def getY(true_file, min_seq_sep, l_max):
    # calcualte the length of the protein (the first feature)
    L = 0
    with open(true_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            L = line.strip().split()
            L = len(L)
            break
    Y = np.zeros((l_max, l_max))
    i = 0
    with open(true_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            this_line = line.strip().split()
            Y[i, 0:L] = feature2D = np.asarray(this_line)
            i = i + 1
    #for p in range(0,L):
    #    for q in range(0,L):
            # updated only for the last project 'p19' to test the effect
    #        if ( abs(q - p) < min_seq_sep):
    #            Y[p][q] = 0
    Y = Y.flatten()
    if np.any(Y>1) or np.isnan(np.sum(Y)):
        os.system("echo '"+true_file+"' >> naninY.txt")
    return Y

def train_on_this_X_Y (model_arch, train_param, X, Y, prev_weights, out_file_weights):
    print ('')
    print ('X Train shape : ' + str(X.shape))
    print ('Y Train shape : ' + str(Y.shape))
    print ('')
    model = build_model_for_this_input_shape(model_arch, X)
    if os.path.isfile(prev_weights):
        print ('Loading previously saved weights..')
        print ('')
        model.load_weights(prev_weights)
    else:
        print (model.summary())
    print ('')
    print ('Compiling model..')
    model.compile(loss = 'binary_crossentropy', optimizer = train_param['optimizer'], metrics = ['accuracy'])
    print ('')
    print ('Fitting model..')
    model.fit(X, Y, verbose = 1, batch_size = train_param['batch_size'], epochs = train_param['inner_epochs'])
    model.save_weights(out_file_weights)

def get_x_from_this_file(feature_file,dncon_path, max_len=0):
    L = 0
    # if max_len==0:
    #     with open(feature_file) as f:
    #         for line in f:
    #             if line.startswith('#'):
    #                 continue
    #             L = line.strip().split()
    #             L = int(round(math.exp(float(L[0]))))
    #             max_len=L
    #             break
    #x = getX(feature_file, L)
    #F = len(x[0, 0, :])
    #X = np.zeros((1, L, L, F))
    # print(feature_file)
    content = np.load(feature_file)

    feature_2D_all = content.f.arr_0.squeeze()
    fea_len = feature_2D_all[0].shape[0]

    

    # dncon_2_path='/data/commons/DeepComplex_common/datasets/hetero_algae/features/dncon2_features/'
    # feat_file_name=dncon_2_path+ "feat-"+os.path.basename(feature_file).replace("npz","txt")
    feat_file_name=dncon_path
    print("########################################################################")
    print(feat_file_name)
    print("########################################################################")
 
    dncon_x=get_dncon_2_x_from_this_file(feat_file_name)

    exp_feature = np.concatenate([dncon_x.squeeze(), feature_2D_all], -1)
    print(exp_feature.shape)

    print(dncon_x.shape)
    print(feature_2D_all.shape)

    channel=exp_feature.shape[2]

    X = np.zeros((max_len, max_len, channel))
    for m in range(0, fea_len):
        X[m, 0:fea_len, 0:channel] = exp_feature[m]
    # x = getX(feature_file, max_len)
    # F = len(x[0, 0, :])
    # X = np.zeros((1, max_len, max_len, F))
    # X[0, :, :, :] = x
    return X

 


# Model architectures / Layers information
def read_model_arch(file_config):
    if not os.path.isfile(file_config):
        print ('Error! Could not find config file ' + file_config)
        sys.exit(1)
    layers = {}
    with open(file_config) as f:
        for line in f:
            if line.startswith('#'):
                continue
            if len(line) < 2:
                continue
            cols = line.strip().split()
            if len(cols) != 5:
                print ('Error! Config file ' + file_config + ' line ' + line + '??')
                sys.exit(1)
            layers[cols[0]] = cols[1] + ' ' + cols[2] + ' ' +  cols[3] + ' ' + cols[4]
    print ('')
    print ('Reading model architecture:')
    for k, v in sorted(layers.items()):
        print (k + ' : ' + v)
    print ('')
    return layers

# Feature file that has 0D, 1D, and 2D features (L is the first feature)
# Output size (a little >= L) to which all the features will be rolled up to as 2D features
def getX(feature_file, l_max):
    # calcualte the length of the protein (the first feature)
    reject_list = []
    reject_list.append('# PSSM')
    reject_list.append('# AA composition')
    L = 0
    with open(feature_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            L = line.strip().split()
            L = int(round(math.exp(float(L[0]))))
            break
    Data = []
    with open(feature_file,"r") as f:
        accept_flag = 1
        for line in f:
            if line.startswith('#'):
                if line.strip() in reject_list:
                    accept_flag = 0
                else:
                    accept_flag = 1
                continue
            if accept_flag == 0:
                continue
            if line.startswith('#'):
                continue
            this_line = line.strip().split()
            if len(this_line) == 0:
                continue
            if len(this_line) == 1:
                # 0D/Scalar feature
                feature2D = np.zeros((L, L))
                feature2D[:, :] = float(this_line[0])
                Data.append(feature2D)
            elif len(this_line) == L:
                # 1D feature
                feature2D1 = np.zeros((L, L))
                feature2D2 = np.zeros((L, L))
                for i in range (0, L):
                    feature2D1[i, :] = float(this_line[i])
                    feature2D2[:, i] = float(this_line[i])
                Data.append(feature2D1)
                Data.append(feature2D2)
            elif len(this_line) == L * L:
                # 2D feature
                feature2D = np.asarray(this_line).reshape(L, L)
                Data.append(feature2D)
            else:
                print (line)
                print ('Error!! Unknown length of feature in !!' + feature_file)
                print ('Expected length 0, ' + str(L) + ', or ' + str (L*L) + ' - Found ' + str(len(this_line)))
                sys.exit()
    F = len(Data)
    X = np.zeros((l_max, l_max, F))
    for i in range (0, F):
        X[0:L, 0:L, i] = Data[i]
    if np.isnan(np.sum(X)):
        os.system("echo '"+feature_file+"' >> naninX.txt")
    return X

def build_model_for_this_input_shape(model_arch, X):
    model = Sequential()
    for layer in range(1, 1000):
        if 'layer' + str(layer) not in model_arch:
            break
        parameters = model_arch['layer' + str(layer)]
        cols = parameters.split()
        num_kernels = int(cols[0])
        filter_size = int(cols[1])
        b_norm_flag = cols[2]
        activ_funct = cols[3]
        if layer == 1:
            #model.add(Convolution2D(num_kernels, filter_size, filter_size, border_mode='same', input_shape=X[0, :, :, :].shape))
            model.add(Conv2D(num_kernels, (filter_size, filter_size), padding='same', input_shape=X[0, :, :, :].shape))
        else:
            #model.add(Convolution2D(num_kernels, filter_size, filter_size, border_mode='same'))
            model.add(Conv2D(num_kernels, (filter_size, filter_size), padding='same'))
        if b_norm_flag == '1':
            model.add(BatchNormalization())
        model.add(Activation(activ_funct))
    model.add(Flatten())
    return model

def make_prediction_new(model_arch, file_weights, X):
#    model = DNCON2_net(inputs=X,filters=16,layers=6,kernel_size=5,act_func="relu",normalize="BatchNormalization")
    model = DNCON2_net(inputs=X,layers=6,filters=16,kernel_size=5,act_func="relu",normalize="BatchNormalize")
    print ("Loading weights...")
    model.load_weights(file_weights)
    print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  The input shape for prediction is :", X.shape)
    P = model.predict(X,batch_size=1)
    return P

def make_prediction(model_arch, file_weights, X):
#    model_arch = build_model_for_this_input_shape(model_arch, X)
    if (file_weights!=None): model_arch.load_weights(file_weights)
    print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  The input shape for prediction is :", X.shape)
    P = model_arch.predict(X)
    return P


def build_dataset_dictionaries_train(path_lists):
  length_dict = {}
  with open(path_lists + 'L.txt') as f:
    for line in f:
      cols = line.strip().split()
      length_dict[cols[0]] = int(cols[1])
  tr_l = {}
  with open(path_lists + 'train.lst') as f:
    for line in f:
      if line.strip() not in length_dict:
        continue
      else:
        tr_l[line.strip()] = length_dict[line.strip()]
  return (tr_l)

def data_generator(data_dict,path_of_lists, path_of_X, path_of_Y, min_seq_sep,dist_string, batch_size, reject_fea_file='None',
    child_list_index=0, list_sep_flag=False, dataset_select='train', feature_2D_num = 441, if_use_binsize=False, predict_method='bin_class', Maximum_length = 500):
    accept_list = []
    if reject_fea_file != 'None':
        with open(reject_fea_file) as f:
            for line in f:
                if line.startswith('#'):
                    feature_name = line.strip()
                    feature_name = feature_name[0:]
                    accept_list.append(feature_name)
    tr_l,te_l,tv_l=build_dataset_dictionaries(path_of_lists)
    if (dataset_select == 'train'):
        dataset_list = tr_l#build_dataset_dictionaries_train(path_of_lists)
    elif (dataset_select == 'vali'):
        dataset_list = tv_l#build_dataset_dictionaries_test(path_of_lists)
    else:
        dataset_list = te_l#build_dataset_dictionaries_train(path_of_lists)
    dataset_list=data_dict
#    print (len(data_dict))
    if (list_sep_flag == False):
        training_dict = data_dict #subset_pdb_dict(dataset_list, 30, Maximum_length, 20000, 'random') #can be random ordered
        training_list = list(training_dict.keys())
        training_lens = list(training_dict.values())
        all_data_num = len(training_dict)
        loopcount = all_data_num // int(batch_size)
        # print('crop_list_num=',all_data_num)
        # print('crop_loopcount=',loopcount)
    else:
        training_dict = data_dict #subset_pdb_dict(dataset_list, 30, Maximum_length, 20000, 'ordered') #can be random ordered
        all_training_list = list(training_dict.keys())
        all_training_lens = list(training_dict.values())
        if ((child_list_index + 1) * 15 > len(training_dict)):
            print("Out of list range!\n")
            child_list_index = len(training_dict)/15 - 1
        child_batch_list = all_training_list[child_list_index * 15:(child_list_index + 1) * 15]
        child_batch_list_len = all_training_lens[child_list_index * 15:(child_list_index + 1) * 15]
        all_data_num = 15
        loopcount = all_data_num // int(batch_size)
        print('crop_list_num=',all_data_num)
        print('crop_loopcount=',loopcount)
        training_list = child_batch_list
        training_lens = child_batch_list_len
    index = 0

    Found =True 
    
    while(True):
        Found =True 
#        print ("Am I here!!!!!!!!!!!!!!!!!!!!")
        if index >= loopcount:
            training_dict = data_dict #subset_pdb_dict(dataset_list, 0, Maximum_length, 20000, 'random') #can be random ordered
            training_list = list(training_dict.keys())
            training_lens = list(training_dict.values())
            index = 0
        batch_list = training_list[index * batch_size:(index + 1) * batch_size]
        batch_list_len = training_lens[index * batch_size:(index + 1) * batch_size]
        index += 1
        # print(index, end='\t')
        if if_use_binsize:
            max_pdb_lens = Maximum_length
        else:
            max_pdb_lens = max(batch_list_len)

        data_all_dict = dict()
        batch_X=[]
        batch_Y=[]
#        print ("Loop_count=",loopcount," Index=",index," len(batch_list)=",len(batch_list)," batch_size=",batch_size)
        for i in range(0, len(batch_list)):


             
            pdb_name = batch_list[i]
            pdb_len = batch_list_len[i]
            notxt_flag = True
            if '__' in pdb_name:
                print('skipping because of --  ')
                Found =False
                continue

            if '__' in pdb_name:
                name_arr = pdb_name.replace('__','_').split('_')
                featurefile = path_of_X + '/' + name_arr[0] + '_' + name_arr[1] + '.npz'
            else:
                name_arr= pdb_name.split('_')
                featurefile = path_of_X + '/' +  name_arr[0]+'_'+name_arr[1] + '.npz'

            # featurefile =path_of_X + + '/' +  name_arr[0]+'_'+name_arr[1] +  '.npz'
            print(featurefile)

            # if not os.path.exists(featurefile): featurefile=featurefile =path_of_X + 'feat-'  + pdb_name + '.txt'
            if not os.path.exists(featurefile): 
                print('skipping because of '+featurefile)
                Found =False
                continue
            if ((len(accept_list) == 1 and ('# cov' not in accept_list and '# plm' not in accept_list and '# pre' not in accept_list and '# spa' not in accept_list and '# netout' not in accept_list)) or
                  (len(accept_list) == 2 and ('# cov' not in accept_list or '# plm' not in accept_list or '# pre' not in accept_list or '# spa' not in accept_list or '# netout' not in accept_list)) or (len(accept_list) > 2)):
                notxt_flag = False
                if not os.path.isfile(featurefile):
                    print("feature file not exists: ",featurefile, " pass!")
                    continue
            if '__' in pdb_name:
                name_arr = pdb_name.replace('__','_').split('_')
                targetfile = path_of_Y + '/' + name_arr[1] + '_' + name_arr[0] + '.txt'
            else:
                name_arr= pdb_name.split('_')
                targetfile = path_of_Y + '/' +  name_arr[0]+'_'+name_arr[1] + '.txt'

            if not os.path.isfile(targetfile):
                    print("target file not exists: ",targetfile, " pass!")
                    continue

            content = np.load(featurefile )

            feature_2D_all = content.f.arr_0.squeeze()
            fea_len = feature_2D_all[0].shape[0]

            
            dncon_2_path='/data/commons/DeepComplex_common/datasets/hetero_algae/features/dncon2_features/'
            feat_file_name=dncon_2_path+ "feat-"+os.path.basename(featurefile).replace("npz","txt")
            print("########################################################################")
            print(feat_file_name)
            print("########################################################################")
            if not os.path.exists(feat_file_name):
                Found =False
                print('skipping beacuse of '+feat_file_name)
                continue
            dncon_x=get_dncon_2_x_from_this_file(feat_file_name)

            print(dncon_x.shape)
            print(feature_2D_all.shape)


            # exp_feature =  np.expand_dims(np.concatenate([dncon_x.squeeze(), feature_2D_all], -1), axis=0) 
            exp_feature = np.concatenate([dncon_x.squeeze(), feature_2D_all], -1)
            print(exp_feature.shape)
            F =exp_feature.shape[2]








            if F != 582:
                Found =False
                print("Target %s has wrong feature shape! Continue!" % pdb_name)
                continue
            #X = np.zeros((max_pdb_lens, max_pdb_lens, F))
            # X= np.zeros((max_pdb_lens, max_pdb_lens, F))
            channel=F
            X = np.zeros((max_pdb_lens, max_pdb_lens, channel))
            for m in range(0, fea_len):
                X[m, 0:fea_len, 0:channel] = exp_feature[m]


            l_max = max_pdb_lens

            if predict_method == 'bin_class':
                print(targetfile)
                Y = getY(targetfile, min_seq_sep, l_max)
                if (l_max * l_max != len(Y)):
                    print('Error!! y does not have L * L feature values!!, pdb_name = %s'%(pdb_name))
                    continue

        if Found ==False       :
            print('skipping beacuse of Found = '+str(Found))
            continue

        if np.any(Y>1) or np.isnan(np.sum(Y)):
            os.system("echo '"+pdb_name+"' >> naninY.txt")
            del X, Y
            continue
        if np.isnan(np.sum(X)):
            os.system("echo '"+pdb_name+"' >> naninX.txt")
            del X, Y
            continue
        batch_X.append(X)
        batch_Y.append(Y)
        del X
        del Y
        batch_X =  np.array(batch_X)
        batch_Y =  np.array(batch_Y)

        if len(batch_X.shape) < 4 or len(batch_Y.shape) < 2:
            # print('Data shape error, pass!\n')
            continue

        yield batch_X, batch_Y
#    print ("No way out#$#$#$#$#$#$#$#$")
