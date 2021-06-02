

import os
import sys
import glob
from math import sin, cos
import math
import random
from random import randrange as rand_num
import numpy as np

import sys
from rosetta import *
from pyrosetta import *
from rosetta.protocols.rigid import *
from rosetta.core.scoring import *
from pyrosetta import PyMOLMover
from rosetta.protocols.rigid import *
import pyrosetta.rosetta.protocols.rigid as rigid_moves
import pyrosetta.rosetta.protocols.rigid as rigid_moves


init()



first_pdb = sys.argv[1]
second_pdb = sys.argv[2]
res_file = sys.argv[3]
OUT = sys.argv[4]
weight_file = sys.argv[5]




def add_chain(pdb_file, letter):
    new_pdb = []
    with open(pdb_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            if line.startswith('ATOM'):
                newline = line[0:21] + letter + line[22:]
                new_pdb.append(newline)
            else:
                new_pdb.append(line)


    with open(pdb_file, 'w') as f:
        for new_line in new_pdb:
            f.write(new_line)
            


def append_pdbs(pdb_file1, pdb_file2, path=os.getcwd()):
    new_pdb = []
    with open(pdb_file1, 'r') as f:
        lines = f.readlines()

        for line in lines:
            if line.startswith('ATOM'):
                new_pdb.append(line)
    separating_line = 'TER' + '\n'
    new_pdb.append(separating_line)

    with open(pdb_file2, 'r') as f:
        lines = f.readlines()

        for line in lines:
            if line.startswith('ATOM'):
                new_pdb.append(line)

    end_line = 'END'
    new_pdb.append(end_line)

    filename = os.path.basename(pdb_file1)
    target_id = filename.split('.')[0]
    new_pdb_file = path + "/" + target_id[:-1] + '.pdb'

    with open(new_pdb_file, 'w') as f:
        for new_line in new_pdb:
            f.write(new_line)
            
    return new_pdb_file
            
            


def get_rotation_matrix(axis_name, degree_magnitude):
    degree_magnitude = math.radians(degree_magnitude)
    if axis_name == 'x':
        rotation_matrix = np.array([[1, 0, 0],[0, cos(degree_magnitude), -sin(degree_magnitude)],[0, sin(degree_magnitude), cos(degree_magnitude)]])
    elif axis_name == 'y':
        rotation_matrix = np.array([[cos(degree_magnitude), 0, sin(degree_magnitude)],[0, 1, 0],[-sin(degree_magnitude), 0, cos(degree_magnitude)]])
    elif axis_name == 'z':
        rotation_matrix = np.array([[cos(degree_magnitude), -sin(degree_magnitude), 0],[sin(degree_magnitude), cos(degree_magnitude), 0],[0, 0, 1]])

    return rotation_matrix

def rotatePose(pose, R):
    start_A = pose.conformation().chain_begin(1)
    end_A = pose.conformation().chain_end(1)
    for r in range(start_A, end_A+1):
        for a in range(1, len(pose.residue(r).atoms())+1):
            v = np.array([pose.residue(r).atom(a).xyz()[0], pose.residue(r).atom(a).xyz()[1], pose.residue(r).atom(a).xyz()[2]])
            newv = R.dot(v)
            pose.residue(r).atom(a).xyz(numeric.xyzVector_double_t(newv[0], newv[1], newv[2]))
            
    return pose
            
    
    
def translatePose(pose, t):
    start_A = pose.conformation().chain_begin(1)
    end_A = pose.conformation().chain_end(1)
    for r in range(start_A, end_A+1):
        for a in range(1, len(pose.residue(r).atoms())+1):
            newx = pose.residue(r).atom(a).xyz()[0] + t[0]
            newy = pose.residue(r).atom(a).xyz()[1] + t[1]
            newz = pose.residue(r).atom(a).xyz()[2] + t[2]
            pose.residue(r).atom(a).xyz(numeric.xyzVector_double_t(newx, newy, newz))
            
    return pose
        


add_chain(first_pdb, 'A')
add_chain(second_pdb, 'B')

initial_start = append_pdbs(first_pdb, second_pdb)
pose = pyrosetta.pose_from_pdb(initial_start)

pose = translatePose(pose, [rand_num(1, 60), 0, 0]).clone()

for i in range(40):
    R_X = get_rotation_matrix('x', rand_num(1, 360))
    R_Y = get_rotation_matrix('y', rand_num(1, 360))
    R_Z = get_rotation_matrix('z', rand_num(1, 360))
    
    pose = rotatePose(pose, R_X).clone()
    pose = rotatePose(pose, R_Y).clone()
    pose = rotatePose(pose, R_Z).clone()
    
    
pose = translatePose(pose, [0, rand_num(1, 60), 0]).clone()
pose = translatePose(pose, [0, 0, rand_num(1, 60)]).clone()

pose.dump_pdb(initial_start)



cmd = 'python /exports/store1/elham/docking_gd_parallel.py ' + initial_start + ' ' + res_file + ' ' + OUT + ' ' +  weight_file
os.system(cmd)
