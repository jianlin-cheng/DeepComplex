#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 22:42:08 2020

@author: farhan
"""

#this script is used to read the paths.txt file which contains the full paths to the tools that we use
def getToolPaths(pathsfile):
    paths_dict={}
    with open (pathsfile,"r") as f:
        for line in f:
            if line.startswith("#"): continue
            if (":" in line ):split=line.strip().split(":")
            if ("=" in line ):split=line.strip().split("=")
            paths_dict[split[0]]=split[1]
    
    return paths_dict