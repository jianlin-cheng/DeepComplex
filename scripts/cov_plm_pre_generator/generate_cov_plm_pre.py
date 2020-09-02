#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 15:41:13 2020

@author: farhan
"""

import os, re, sys

if __name__ == '__main__':
    if len(sys.argv)!=3:
        print("generate_cov_plm_pre.py <alignment_file in .aln or psicov format> <outdir>")
        exit(1)

    aln_file= os.path.abspath(sys.argv[1])
    outdir = os.path.abspath(sys.argv[2])
    
    #script_path = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    print ("Script_path: "+script_path)
    target = os.path.basename(aln_file)
    target = re.sub("\.aln","",target)

    if not os.path.exists(aln_file):
        print("Alignment file:"+aln_file+" not found. Quitting!")
        sys.exit(1)
    dir_subsets=["/cov","/plm","/pre"]
    for dirs in dir_subsets:
        if not os.path.exists(outdir+dirs):
            os.makedirs(outdir+dirs)
            print("Output folder: "+outdir+dirs+" created.")

    #Generate covariance matrix
    if os.path.exists(outdir+"/cov/"+target+".cov") and os.path.getsize(outdir+"/cov/"+target+".cov") > 0:
        print("Covariance file already exists...skipping!")
        #Save it in file
        with open (script_path+"/CovarianceAlreadyPresent.txt","a+") as f:
            f.write(target+"\n")
    else:
        exit_code=os.system(script_path+"/cov21stats "+aln_file+" "+outdir+"/cov/"+target+".cov")
        if os.path.exists(outdir+"/cov/"+target+".cov") and os.path.getsize(outdir+"/cov/"+target+".cov") > 0 and exit_code==0:
            print("Covariance matrix generated successfully... Saved as "+outdir+"/cov/"+target+".cov")
        else:
            print("Covariance matrix generation failed...")
            #Save it in file
            with open (script_path+"/CovarianceFailed.txt","a+") as f:
                f.write(target+"\n")
            

    #Generate plm matrix
    if os.path.exists(outdir+"/plm/"+target+".plm") and os.path.getsize(outdir+"/plm/"+target+".plm") > 0:
        print("Plm file already exists... skipping!")
        with open (script_path+"/PlmAlreadyPresent.txt","a+") as f:
            f.write(target+"\n")
        #os.system("mv "+outdir+"/ccmpred/"+target+".plm "+outdir)
    #elif os.path.exists(outdir+"/"+target+".plm") and os.path.getsize(outdir+"/"+target+".plm") > 0:
    #    print("plm generated.....skip")
    else:
        if not os.path.isdir(outdir+"/ccmpred"): os.makedirs(outdir+"/ccmpred")
        exit_code=os.system(script_path+"/CCMpred_plm/bin/ccmpred -t 1 "+aln_file+" "+outdir+"/ccmpred/"+target+".ccmpred "+outdir+"/plm/"+target+".plm")
        if os.path.exists(outdir+"/plm/"+target+".plm") and os.path.getsize(outdir+"/plm/"+target+".plm") > 0 and exit_code==0:
            print("PLM matrix generated successfully... Saved as "+outdir+"/plm/"+target+".plm")
        else:
            print("PLM matrix generation failed...")
            #Save it in file
            with open (script_path+"/PlmFailed.txt","a+") as f:
                f.write(target+"\n")

    #step5: generate precision matrix
    if os.path.exists(outdir+"/pre/"+target+".pre") and os.path.getsize(outdir+"/pre/"+target+".pre") > 0:
        print("Precision matrix already exists..Skipping!")
        with open (script_path+"/PreAlreadyPresent.txt","a+") as f:
            f.write(target+"\n")
    else:
        exit_flag=True
        exit_code=os.system(script_path+"/calNf_ly "+aln_file+" 0.8 > "+outdir+"/pre/"+target+".weight")
        if exit_code==0: exit_flag=True
        exit_code=os.system("python -W ignore "+script_path+"/generate_pre.py "+aln_file+" "+outdir+"/pre/"+target)#+" >"+outdir+"/pre.log")
        if exit_code==0: exit_flag=True
        os.system("rm "+outdir+"/pre/"+target+".weight")
        if os.path.exists(outdir+"/pre/"+target+".pre") and os.path.getsize(outdir+"/pre/"+target+".pre") > 0 and exit_flag:
            print("Precision matrix generated successfully... Saved as "+outdir+"/pre/"+target+".pre")
        else:
            print("Pre matrix generation failed...")
            #Save it in file
            with open (script_path+"/PreFailed.txt","a+") as f:
                f.write(target+"\n")