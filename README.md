# DeepComplex
Deep learning prediction of inter-chain contacts of protein complex


#################################################################
#                  Complex_Structure_Predictor                 #
################################################################
To use it go and edit the config file and change the directory of the CNS-1.3 and also may change the number of models that you want to generate

Format Command:
python <program_name> <target_id> <pdb_list_file> <restrain_list_file> <output_file>
Sample Command:
python structure_predictor_n-mer.py test /home/rajroy/multi-mer_test_1/pdb.txt /home/rajroy/multi-mer_test_1/res.txt /home/rajroy/test/

The chain name should be separated by an underscore and should be at the last char of the base name
e.g: /home/rajroy/multi-mer_test/provided_files/4OJ5_ABC_X_1.pdb  , here "1" is the name of the chain

The interaction chain name should be separated by an underscore and should be at the last 2 char of the base name
e.g /home/rajroy/multi-mer_test/provided_files/4OJ5_ABC_AB.rr, here this file would be restains between chain "A and B" respectively

