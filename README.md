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




#################################################################
#                  Inter_chain_Predictor                 #
################################################################
Current Version of the file can predict the homodimer of upto 500 sequence length

Format Command:
python <program_name> <input_feature_file> <output_directory>

Sample Command:
python contact_predictor.py ./examples/expected_input_file/feat-1A0F.txt /home/rajroy/predict_map_test/

The program will provide 2 files one is in rr format and another in matrix LxL format, where L is the lenght of the sequence.

Furthermore, an example directory has been added, DeepComplex/inter_chain_contact_predictor/homo_dimer/examples/ in which the if the example.sh file is executed it will produce a directory predicted_output_file which will contain 2 output files as stated above: to cross-match the output files another directory is provided which also contains the output of the prediction by the name of expected_output_file. 






