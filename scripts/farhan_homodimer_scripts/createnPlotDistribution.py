#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:26:40 2019

@author: farhan
"""

#takes a list of interchain contact distances or rr files. and plots a distance distribution

import os,sys,subprocess

file_title="/data/farhan/SoftwareTools/HomopolymerProject/scripts/4zuk_out/4zuk_multimer_dist_8_"

subscript=["AB_dist.txt","AC_dist.txt","AD_dist.txt"]
line_dict={}
for subs in subscript:
    file=file_title+subs
    if (not os.path.exists(file)): 
        print (file+ " not found")
        continue
    lnnum = subprocess.check_output("wc -l < "+file,shell = True)
    lnnum = lnnum.rstrip()
    lnnum = str(lnnum)
    lnnum = int(lnnum.strip("b").strip("'"))-1
    line_dict[subs.split("_")[0]]=lnnum

import plotly.plotly as py
import plotly.tools as tls

import matplotlib.pyplot as plt

dictionary = plt.figure()

D = line_dict

plt.bar(D.keys(),D.values(),label="4ZUK", color="g")
plt.legend()
plt.xlabel("Interacting chains")
plt.ylabel("Frequency")
plt.title("Interchain Contact distribution among different chains in the homooligomer 4ZUK")
plt.show()