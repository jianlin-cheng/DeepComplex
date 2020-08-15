
import sys
import pickle

list_file = sys.argv[1]
#file1 = open("1_AB_all_pdb_atom.lst","r")

file1 = open(list_file,"r")
PDBs_list = file1.readlines()
file1.close()

############################## oligomer selection ############################# 

Eliminate_list = [] # proteins that are eliminated because the protein name does not have any chain indication 
monomer_list = []   # proteins with single chain
Oligomer_list = []  # list of lists where each individual list contains chains that belong to the same protein 
dimer = []          # protiens that have two chains only (this is kept for the sake of statistics only)
multimer = []       # proteins with more than two chains
dimer_num = 0
multimer_num = 0
flag = 0
Id_num_temp = 1
Id_num = 0

while Id_num <= len(PDBs_list):
        Id = PDBs_list[Id_num]
        Id = Id.strip()
        pdb_id = Id.split(".")[0]
        temp_list = [] # list of chains that belong to the same protein 
        PDB1 = pdb_id[0:4]
        
        if len(pdb_id) == 4: # proteins to be ingored
            Eliminate_list.append(Id)
            Id_num+ = 1
        else:
            temp_list.append(Id)
            flag = 1
            Id_num_temp = 0
            while flag == 1:
                if Id_num == len(PDBs_list)-1:# last protein in the list
                    flag = 0
                    if len(temp_list) == 1:
                        monomer_list.append(Id)
                    else:
                        Oligomer_list.append(temp_list) 
                    break
                
                else:
                    Id_num_temp = Id_num+1
                    Id_temp = PDBs_list[Id_num_temp]
                    Id_temp = Id_temp.strip()
                    pdb_id_temp = Id_temp.split(".")[0]
                    
                    if len(pdb_id_temp) == 4: # proteins to be ingored
                        Eliminate_list.append(pdb_id_temp)
                        Id_num+= 1
                        continue
                    else:
                        PDB2 = pdb_id_temp[0:4]
                    
                    if PDB1 == PDB2:
                        temp_list.append(Id_temp)
                        flag = 1
                        Id_num = Id_num_temp
                        #print("end of iteration Id_num = ",Id_num)
                    else:
                        Id_num = Id_num_temp
                        flag=0
                        #print("end of iteration Id_num= ",Id_num)
                        
                        if len(temp_list) == 1:
                            monomer_list.append(Id)
                            
                        else:
                            Oligomer_list.append(temp_list)
                            if len(temp_list) == 2:
                                dimer.append(temp_list)
                                dimer_num+= 1
                            else:
                                multimer.append(temp_list)
                                multimer_num+= 1
                            
        if Id_num == len(PDBs_list)-1:
            break

############################## dimer arrangement ############################## 

All_pairs_list = [] # list that contains all possible pairs for each oligomer without repetition
Total_pairs_number = 0
line_counter = 0
fout = open("pairs.txt","w")

for Oligo_list in Oligomer_list:
    List_len = len(Oligo_list)
    Pair_num = sum(list(range(1,List_len)))
    Total_pairs_number+= Pair_num
    #print("list length : ",list_len," number of pairs ", pair_num)
    List_current = []
    for i in list(range(List_len)):
        for j in list(range(i,List_len)):
            if i == j:
                continue
            else:
                List_current.append([Oligo_list[i],Oligo_list[j]])
                fout.write(Oligo_list[i]+","+Oligo_list[j]+"\n" )
    All_pairs_list = All_pairs_list+List_current
fout.close()

