#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:08:09 2020

@author: farhan
"""

contact_table_file="contact_table.txt"
contact_density_table_file="contact_density_table.txt"

ctable_dict={}

with open (contact_density_table_file,"r")  as f:
    for line in f:
        if (line.startswith("Name")): continue
        split=line.strip().split()
        