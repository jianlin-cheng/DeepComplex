# DeepComplex
Deep learning prediction of inter-chain contacts of protein complexes

This software has two tools:

(1) Inter-chain Contact Predictor which is used to predict the inter-chain contact map (currently for homodimeric proteins only), and

(2) Complex Structure Reconstructor which is used to construct the final structure of the protein complex from the inter-chain contacts.



###                  Downloading             

Just type the following command to download the software.


`git clone https://github.com/jianlin-cheng/DeepComplex`

You can also use wget to download the software using the following commands:

```
mkdir DeepComplex
cd DeepComplex
wget https://github.com/jianlin-cheng/DeepComplex
```

Once the download is complete, follow the steps in the installation section to install and run the software.


###                  Installation             

This software was developed and tested using python, perl and other dependent software. Please make sure the following softwares versions are installed:

+  (1) Python 3.6

* (2) Perl

  (3) CNS_solve 1.3 (Crystallography and NMR Systems)


The following python dependencies (packages) are needed for the code to execute:

  (1) Tensorflow 1.7.0

  (2) Numpy 1.16.2

  (3) Keras 2.1.6

  (4) H5py 2.9.0

  (5) Scikit-learn 0.20.3


Besides the python packages, In order to generate features for the deep learning predictor, the following software tools are necessary:

  (1) HH-suite-3.0

  (2) JackHMMER/HMMER-3.1

  (3) Latest HH-suite searchable protein database like UniRef30_2020_06: available at http://gwdu111.gwdg.de/~compbiol/uniclust/2020_06/

  (4) Latest JackHMMER searchable protein database like UniRef90: available at [ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz]

  (5) MetaPSICOV avilable at: https://github.com/psipred/metapsicov

  (6) SCRATCH-1D_1.1 available at: https://github.com/SBRG/ssbio/blob/master/docs/instructions/scratch.rst or http://download.igb.uci.edu/#sspro

  (7) ncbi-blast-2.2.25+ available at: https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.25/

  (8) Blast NR database: https://ftp.ncbi.nlm.nih.gov/blast/db/


IMPORTANT: After installing the above tools, please add the paths of the above tools into the "paths.txt" keeping the format of the file same.

Now run the following command to install the feature generation tool:

`$ sh install_dncon2_feature_generator.sh`


Installation is now complete. Now you are ready to use DeepComplex. Examples of how to use the two tools are described bellow.


###                  Complex_Structure_Reconstructor             

To use it go and edit the config file and change the directory of the CNS-1.3 and also may change the number of models that you want to generate

Format Command:
python <program_name> <target_id> <pdb_list_file> <restrain_list_file> <output_file>
Sample Command:
python structure_predictor_n-mer.py test /home/rajroy/multi-mer_test_1/pdb.txt /home/rajroy/multi-mer_test_1/res.txt /home/rajroy/test/

The chain name should be separated by an underscore and should be at the last char of the base name
e.g: /home/rajroy/multi-mer_test/provided_files/4OJ5_ABC_X_1.pdb  , here "1" is the name of the chain

The interaction chain name should be separated by an underscore and should be at the last 2 char of the base name
e.g /home/rajroy/multi-mer_test/provided_files/4OJ5_ABC_AB.rr, here this file would be restains between chain "A and B" respectively


###                  Inter_chain_Predictor                 

Current Version of the file can predict the homodimer of upto 500 sequence length

Format Command:
python <program_name> <input_feature_file> <output_directory>

Sample Command:
python contact_predictor.py ./examples/expected_input_file/feat-1A0F.txt /home/rajroy/predict_map_test/

The program will provide 2 files one is in rr format and another in matrix LxL format, where L is the lenght of the sequence.

Furthermore, an example directory has been added, DeepComplex/inter_chain_contact_predictor/homo_dimer/examples/ in which the if the example.sh file is executed it will produce a directory predicted_output_file which will contain 2 output files as stated above: to cross-match the output files another directory is provided which also contains the output of the prediction by the name of expected_output_file. 






