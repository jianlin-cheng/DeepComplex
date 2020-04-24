#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 16:05:43 2020

@author: farhan
"""

#this script is used to read the Y-WXYZ.txt label file into a numpy array
#usage: python readLabelFile.py <Y-WXYZ.txt>
import numpy as np
import sys,os

def readLabelFile(label_file):
    if not (os.path.exists(label_file)): sys.exit("Label file "+label_file+" not found. Quitting!")
    mat=np.loadtxt(label_file)
    return mat

label_file=sys.argv[1]

#matrix=readLabelFile(label_file)
#print (matrix.shape)


    