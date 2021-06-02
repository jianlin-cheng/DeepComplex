import os
import sys
import math


rr_file = sys.argv[1]

probs = []
with open(rr_file) as f:
    for line in f:
        content = line.strip().split()
        if content[0].isdigit():
            probs.append(float(content[4]))
			
			

def get_num_of_zeros(num):
    num_of_zeros  = 0
    while not (num//1):
        num *= 10
        num_of_zeros +=1

    return num_of_zeros
    
    
#print(get_num_of_zeros(max(probs)))
#print(round(max(probs), get_num_of_zeros(max(probs))))

thre1 = round(max(probs), get_num_of_zeros(max(probs))) - 10 ** -get_num_of_zeros(max(probs))
thre2 = thre1 - 10 ** -get_num_of_zeros(max(probs))
thre3 = thre2 - 10 ** -get_num_of_zeros(max(probs))
thre4 = thre3 - 10 ** -get_num_of_zeros(max(probs))
thre5 = thre4 - 10 ** -get_num_of_zeros(max(probs))

#print(thre1, thre2, thre3, thre4, thre5)