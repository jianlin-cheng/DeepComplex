

length_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/same/all_training_protein_length.txt"
train_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/same/train_list.txt"
val_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/same/validation_list.txt"
test_list_file="/data/farhan/SoftwareTools/HomopolymerProject/DeepComplex/training/dncon2_model/training_lists/same/test_list.txt"
range_gap=100
range_gap_list=[]
all_dict={}
train_dict={}
test_dict={}
val_dict={}

with open (length_list_file,"r") as f:
    for line in f:
        all_dict[line.strip().split()[0]]=int(line.strip().split()[1])

with open (train_list_file,"r") as f:
    for line in f:
        train_dict[line.strip()]=all_dict[line.strip()]

with open (test_list_file,"r") as f:
    for line in f:
        test_dict[line.strip()]=all_dict[line.strip()]

with open (val_list_file,"r") as f:
    for line in f:
        val_dict[line.strip()]=all_dict[line.strip()]



key_list=list(all_dict.keys())

