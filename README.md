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

    (1) Python 3.6

    (2) Perl

    (3) CNS_solve 1.3 (Crystallography and NMR Systems)


The following python dependencies (packages) are needed for the code to execute:

    (1) Tensorflow 1.7.0

    (2) Numpy 1.16.2

    (3) Keras 2.1.6

    (4) H5py 2.9.0

    (5) Scikit-learn 0.20.3


Besides the python packages, In order to generate features for the deep learning predictor, the following software tools are necessary:

    (1) HH-suite-3.0 available at: https://github.com/soedinglab/hh-suite

    (2) JackHMMER/HMMER-3.1 available at: http://hmmer.org/download.html

    (3) Latest HH-suite searchable protein database like UniRef30_2020_06: available at: http://gwdu111.gwdg.de/~compbiol/uniclust/2020_06/

    (4) Latest JackHMMER searchable protein database like UniRef90: available at: ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz

    (5) MetaPSICOV avilable at: https://github.com/psipred/metapsicov

    (6) SCRATCH-1D_1.1 available at: https://github.com/SBRG/ssbio/blob/master/docs/instructions/scratch.rst or http://download.igb.uci.edu/#sspro

    (7) ncbi-blast-2.2.25+ available at: https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.25/

    (8) Blast NR database available at: https://ftp.ncbi.nlm.nih.gov/blast/db/


IMPORTANT: After installing the above tools, please add the paths of the above tools into the "paths.txt" keeping the format of the file same.

Now run the following command to install the feature generation tool:

`$ sh install_dncon2_feature_generator.sh`


Installation is now complete. Now you are ready to use DeepComplex. Examples of how to use the two tools are described bellow.




##                  Inter Chain Contact Predictor                 

Current version of the inter chain contact predictor can predict the homodimer of upto 500 sequence length

### Usage
For performing a inter-chain contact prediction, run the contact_predictor with the following command:

```
#Usage
python contact_predictor.py <input_fasta> <input_feature_file> <output_directory>

#Example:
python contact_predictor_homodimer.py ./examples/expected_input_file/11AS.fasta ./examples/expected_input_file/feat-11AS.txt /home/rajroy/output/ 11AS
 
```
The program will provide 2 files one is in rr format and another in matrix format of LxL , where L is the length of fasta sequence.
### Testing the inter-chain contact prediction
The program can be tested using the following script:
```
(1) cd /inter_chain_contact_predictor/homo_dimer/examples
(2) sh example.sh


Output examples:
/examples/predict_map_test/predicted_output_file//feat-1A0F_predicted.rr
/examples/predict_map_test/predicted_output_file//feat-1A0F_predicted.rr_matrix.txt
```





##                 Complex_Structure_Reconstructor             

### Setup

Edit the config file at /complex_sturcture_reconstructor/config.py
```
Change the directory of the varaible 'CNS_DIRECTORY' to the directory where it is installed

e.g CNS_DIRECTORY = '/home/rajroy/cns/cns_solve_1.3/'

```

###                        Usage

For performing a complex structure prediction, run structure predictor with the following command:
```
#Usage
python structure_predictor_n-mer.py <target_id> <pdb_list_file> <restrain_list_file> <output_file>

#Example
python structure_predictor_n-mer.py test /home/rajroy/multi-mer_test_1/pdb.txt /home/rajroy/multi-mer_test_1/res.txt /home/rajroy/test/

```

#### Instruction
The chain name should be separated by an underscore and should be at the last char of the base name
```
e.g: /home/rajroy/multi-mer_test/provided_files/4OJ5_ABC_X_1.pdb  , here "1" is the name of the chain
```
The interacting chain name should be separated by an underscore and should be at the last 2 char of the base name
```
e.g /home/rajroy/multi-mer_test/provided_files/4OJ5_ABC_AB.rr, here this file would be restains between chain "A and B" respectively
```

# DeepComplex webserver

### Dependencies

Please install the following dependency software:

    (1) Python 3.6, and 2.7 for DNCON2

    (2) Perl

    (3) PyRosetta [http://www.pyrosetta.org/dow/pyrosetta4-download]

    (4) DNCON2 and all its dependencies from [https://github.com/multicom-toolbox/DNCON2]

    (5) Tensorflow 1.7.0

    (6) Numpy 1.16.2

    (7) Keras 2.1.6

    (8) H5py 2.9.0

    (9) Scikit-learn 0.20.3

Make sure all the software paths are updates in the file: [https://github.com/jianlin-cheng/DeepComplex/tree/master/webserver/predictor_code/scripts/feature_gen_hetero_v2/paths.txt]

It is best to install the tools/dependencies in the folder [https://github.com/jianlin-cheng/DeepComplex/tree/master/webserver/predictor_code/tools/]

Change any hard paths that if necessary. 

### Source Code

The webserver source code can be found in [https://github.com/jianlin-cheng/DeepComplex/tree/master/webserver/html]

The Webserver predictor code is available in [https://github.com/jianlin-cheng/DeepComplex/tree/master/webserver/predictor_code]. This contains codes for both the homodimer and heterodimers. 

```
For Homodimer prediction Run:
python contact_predictor_homodimer.py <full path of fasta_file > <full path of feature_path > <full path of  output_dir> <target_id>

For Heterodimer prediction Run:
python contact_predictor_heterodimer.py <full path of fasta_file A> <full path of fasta_file B> <full path of feature_path > <full path of  output_dir> <target_id>
```

The feature generation code for heterodimers is available in [https://github.com/jianlin-cheng/DeepComplex/tree/master/webserver/predictor_code/scripts]

The feature generation code for homodimers is available in [https://github.com/jianlin-cheng/DeepComplex/tree/master/webserver/predictor_code/tools/DNCON2/dncon2-v1.0.sh]

The Gradient-descent (BD) based optimizer code is available in [https://github.com/jianlin-cheng/DeepComplex/tree/master/webserver/optimizer_code] 

```
For GD-based optimizer Run:
source ~/tools/pyrosettta-env/bin/activate
weight_file = ~/optimizer_code/talaris2013.wts
python ~/optimizer/do_dock.py <first_pdb> <second_pdb> <restraint_file> <output_dir> <$weight_file>
```



 






