#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 01:41:37 2020

@author: farhan
"""

from shutil import copyfile
import platform
import os
import numpy as np
import math
import sys
import random
import keras.backend as K
import itertools
from operator import itemgetter
from sklearn.metrics import recall_score, f1_score, confusion_matrix, matthews_corrcoef, precision_score
from DNCON2_library import *

epsilon = K.epsilon()

def print_detailed_evaluations_4(dict_l, PL5, PL2, PL, P, Y):
  datacount = len(dict_l)

  avg_prec_l5 = 0.0
  avg_prec_l2 = 0.0
  avg_prec_1l = 0.0
  avg_recall_l5 = 0.0
  avg_recall_l2 = 0.0
  avg_recall_1l = 0.0
  avg_f1_l5 = 0.0
  avg_f1_l2 = 0.0
  avg_f1_1l = 0.0
  avg_mcc_l5 = 0.0
  avg_mcc_l2 = 0.0
  avg_mcc_1l = 0.0
  i = -1
  for pdb in sorted(dict_l):
    mcc_l5    = matthews_corrcoef(Y[i], PL5[i, :])
    mcc_l2    = matthews_corrcoef(Y[i], PL2[i, :])
    mcc_1l    = matthews_corrcoef(Y[i], PL[i, :])
    prec_l5   = precision_score(Y[i], PL5[i, :])
    prec_l2   = precision_score(Y[i], PL2[i, :])
    prec_1l   = precision_score(Y[i], PL[i, :])
    recall_l5 = recall_score(Y[i], PL5[i, :])
    recall_l2 = recall_score(Y[i], PL2[i, :])
    recall_1l = recall_score(Y[i], PL[i, :])
    F1_l5     = f1_score(Y[i], PL5[i, :])
    F1_l2     = f1_score(Y[i], PL2[i, :])
    F1_1l     = f1_score(Y[i], PL[i, :])
    # pc_l5 = np.logical_and(Y[i], PL5[i, :]).sum()
    # pc_l2 = np.logical_and(Y[i], PL2[i, :]).sum()
    # pc_1l = np.logical_and(Y[i], PL[i, :]).sum()
    # prec_l5 = float(pc_l5) / (float(L5) + epsilon)
    # prec_l2 = float(pc_l2) / (float(L2) + epsilon)
    # prec_1l = float(pc_1l) / (float(L) + epsilon)
    avg_mcc_l5 += mcc_l5
    avg_mcc_l2 += mcc_l2
    avg_mcc_1l += mcc_1l
    avg_prec_l5 += prec_l5
    avg_prec_l2 += prec_l2
    avg_prec_1l += prec_1l
    avg_recall_l5 += recall_l5
    avg_recall_l2 += recall_l2
    avg_recall_1l += recall_1l
    avg_f1_l5 += F1_l5
    avg_f1_l2 += F1_l2
    avg_f1_1l += F1_1l
  avg_mcc_l5 /= datacount
  avg_mcc_l2 /= datacount
  avg_mcc_1l /= datacount
  avg_prec_l5 /= datacount
  avg_prec_l2 /= datacount
  avg_prec_1l /= datacount
  avg_recall_l5 /= datacount
  avg_recall_l2 /= datacount
  avg_recall_1l /= datacount
  avg_f1_l5 /= datacount
  avg_f1_l2 /= datacount
  avg_f1_1l /= datacount
  # print("   Avg                           %6s        %6s %6s %6s    %.4f    %.4f    %.4f" % (avg_nc, avg_pc_l5, avg_pc_l2, avg_pc_1l, avg_prec_l5, avg_prec_l2, avg_prec_1l))
  # print ("")
  return (avg_prec_l5, avg_prec_l2, avg_prec_1l, avg_mcc_l5, avg_mcc_l2, avg_mcc_1l, avg_recall_l5, avg_recall_l2, avg_recall_1l, avg_f1_l5, avg_f1_l2, avg_f1_1l)

######################################################################################################################################################
def evaluate_prediction_4 (dict_l, P, Y, min_seq_sep):
  datacount = len(Y[:, 0])
  L = int(math.sqrt(len(Y[0, :])))
  P2 = np.copy(P).reshaped(datacount,L*L)
  Y1 = np.copy(Y)
  #list_acc_l5 = []
  #list_acc_l2 = []
  #list_acc_1l = []
  P3L5 = ceil_top_xL_to_one_4(dict_l, P2, Y, 0.2)
  P3L2 = ceil_top_xL_to_one_4(dict_l, P2, Y, 0.5)
  P31L = ceil_top_xL_to_one_4(dict_l, P2, Y, 1)
  avg_prec_l5, avg_prec_l2, avg_prec_1l, avg_mcc_l5, avg_mcc_l2, avg_mcc_1l, avg_recall_l5, avg_recall_l2, avg_recall_1l, avg_f1_l5, avg_f1_l2, avg_f1_1l = print_detailed_evaluations_4(dict_l, P3L5, P3L2, P31L, P2, Y)
  return (avg_prec_l5, avg_prec_l2, avg_prec_1l, avg_mcc_l5, avg_mcc_l2, avg_mcc_1l, avg_recall_l5, avg_recall_l2, avg_recall_1l, avg_f1_l5, avg_f1_l2, avg_f1_1l)

######################################################################################################################################################
# Ceil top xL predictions to 1, Length according to the Y
def ceil_top_xL_to_one_4(ref_file_dict, XP, Y, x):
  X_ceiled = np.copy(XP)
  i = -1
  for pdb in sorted(ref_file_dict):
    i = i + 1
    if x >1: 
        xL=int(x)
    else:
        xL = int(x * int(math.sqrt(len(Y[i]))))
    X_ceiled[i, :] = np.zeros(len(XP[i, :]))
    X_ceiled[i, np.argpartition(XP[i, :], -xL)[-xL:]] = 1
  return X_ceiled
