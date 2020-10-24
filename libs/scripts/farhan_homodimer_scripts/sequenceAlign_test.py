#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 17:14:25 2020

@author: farhan
"""

#sequence align

from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import sys

def getMaxConsecutiveGaps(sequence):
    num_of_gap_sequence=0
    if ("-" in sequence):
        gap_found=False
        i=-1
        while i < len(sequence)-1:
            i+=1
            if (sequence[i]=="-"):
                gap_found=True
                for j in range(i,len(sequence)):
                    
                    if (sequence[j]!="-"):
                        num_of_gap_sequence+=1
                        i=j-1
                        break
        #pass
    else:
        return 0
            
    return num_of_gap_sequence   

def selectBestAlignment(alignment):
    best=getMaxConsecutiveGaps(alignment[0][0])+getMaxConsecutiveGaps(alignment[0][1])
    best_aln=alignment[0]
    for i in range(1,len(alignment)):
        score_a1=getMaxConsecutiveGaps(alignment[i][0])
        score_a2=getMaxConsecutiveGaps(alignment[i][1])
        #print (score_a1,score_a2)
        if (score_a1+score_a2<=best):
            best=score_a1+score_a2
            best_aln=alignment[i]
        
    return best_aln

def readFastaDict(fasta_dict_file):
    fasta_dict={}
    with open (fasta_dict_file,"r") as f:
        for line in f:
            fasta_dict[line.strip().split(":")[0].strip()]=line.strip().split(":")[1].strip()
    return fasta_dict

pdb_name="1T62"#"2EHP"#"2HXR"#"4I24"#"1BFT"#"1UZY"#"5IZV"#"11AS"#"4I24"
#x=sys.argv[1]
#y=sys.argv[2]


fasta_dict=readFastaDict("fasta_dictionary.txt") #reads the fasta_dictionary.txt file as a dictionary
key_list=fasta_dict.keys() #get the keys of the dictionary
this_key_list=[] #stores the list of keys for pdb_name
for key in key_list:
    if pdb_name in key:
        this_key_list.append(key)

x=fasta_dict[this_key_list[0]]
y=fasta_dict[this_key_list[1]]

#x="VVKFTKSEALHKEALEHIVGGVNSPSRSFKAVGGGAPIAERGKGAYFWDVDGNKYIDYLAAYGPIITGHAHPHITKAITTAAENGVLYGTPTALEVKFAKLKEAPALDKVRFVNSGTEAVTTIRVARAYTGRTKIKFAGCYHGHSDLVLVA-------LGTPDSAGVPQSIAQEVITVPFNNVETLKEALDKWGHEVAAILVEPIVGNFGIVEPKPGFLEKVNELVHEAGALVIYDEVITAFRFYGGAQDLLGVTPDLTALGVIGGGLPIGAYGGKKEIEQVAPLGPAYQAGTAGNPASASGIACLEVLQQEGLYEKLDELGATLEKGILEQAAKHNIDITLNRLKGALTVYFTTNTIEDYDAAQDTDGEFGKFFKLLQEGVNLAPSKYEAWFLTTEHTKEDIEYTIEAVGRAFAALADNN-"
#x="VVKFTKSEALHKEALEHIVGGVNSPSRSFKAVGGGAPIAERGKGAYFWDVDGNKYIDYLAAYGPIITGHAHPHITKAITTAAENGVLYGTPTALEVKFAKLKEAPALDKVRFVNSGTEAVTTIRVARAYTGRTKIKFAGCYHGHSDLVLVALGTPDSAGVPQSIAQEVITVPFNNVETLKEALDKWGHEVAAILVEPIVGNFGIVEPKPGFLEKVNELVHEAGALVIYDEVITAFRFYGGAQDLLGVTPDLTALGVIGGGLPIGAYGGKKEIEQVAPLGPAYQAGTAGNPASASGIACLEVLQQEGLYEKLDELGATLEKGILEQAAKHNIDITLNRLKGALTVYFTTNTIEDYDAAQDTDGEFGKFFKLLQEGVNLAPSKYEAWFLTTEHTKEDIEYTIEAVGRAFAALADN"
#y="VVKFTKSEALHKEALEHIVGGVNSPSRSFKAVGGGAPIAERGKGAYFWDVDGNKYIDYLAAYGPIITGHAHPHITKAITTAAENGVLYGTPTALEVKFAKLKEAPALDKVRFVNSGTEAVTTIRVARAYTGRTKIKFAGCYHGHSDLVLVAAGSGPSTLGTPDSAGVPQSIAQEVITVPFNNVETLKEALDKWGHEVAAILVEPIVGNFGIVEPKPGFLEKVNELVHEAGALVIYDEVITAFRFYGGAQDLLGVTPDLTALGVIGGGLPIGAYGGKKEIEQVAPLGPAYQAGTAGNPASASGIACLEVLQQEGLYEKLDELGATLEKGILEQAAKHNIDITLNRLKGALTVYFTTNTIEDYDAAQDTDGEFGKFFKLLQEGVNLAPSKYEAWFLTTEHTKEDIEYTIEAVGRAFAALADNK"
#x="NQALLRILKETEFKKIKVLGSGAFGTVYKGLWIPEGEKVKIPVAIKELANKEILDEAYVMASVDNPHVCRLLGICLTSTVQLIMQLMPFGCLLDYVREHKDNIGSQYLLNWCVQIAKGMNYLEDRRLVHRDLAARNVLVKTPQHVKITDFGLAKLLVPIKWMALESILHRIYTHQSDVWSYGVTVWELMTFGSKPYDGIPASEISSILEKGERLPQPPICTIDVYMIMVKCWMIDADSRPKFRELIIEFSKMARDPQRYLVIQGDERMHLPSPTDSNFYRALMDEEDMDDVVDAD"
#y="NQALLRILKETEFKKIKVLGSGAFGTVYKGLWIPEGEKVKIPVAIKELREATSPKANKEILDEAYVMASVDNPHVCRLLGICLTSTVQLIMQLMPFGCLLDYVREHKDNIGSQYLLNWCVQIAKGMNYLEDRRLVHRDLAARNVLVKTPQHVKITDFGLAKLLGKVPIKWMALESILHRIYTHQSDVWSYGVTVWELMTFGSKPYDGIPASEISSILEKGERLPQPPICTIDVYMIMVKCWMIDADSRPKFRELIIEFSKMARDPQRYLVIQGDERMHLPSPTDSNFYRALMDEEDMDDVVDAD"
#alignments = pairwise2.align.globalxx(x, y)
alignments = pairwise2.align.globalms(x, y,5,-4,-1,-0.1)
#print (len(x),len(y))
# Use format_alignment method to format the alignments in the list

for a in alignments:
    #print(format_alignment(*a))
    print (a[0])
    print(a[1])
    #break

print (len(alignments))
#best_aln=selectBestAlignment(alignments)
#print (alignments[3][0])
#print (alignments[3][1])
#print(best_aln[0])
#print(best_aln[1])
#print(alignments[0][0]==alignments[1][0])
#print (alignments[0][0])
#print (alignments[1][0])
