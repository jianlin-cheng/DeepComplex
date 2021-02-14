

from Bio import pairwise2



def getMaxConsecutiveGaps(sequence):
    num_of_gap_sequence = 0
    if ("-" in sequence):
        gap_found = False
        i = -1
        while i < len(sequence) - 1:
            i += 1
            if (sequence[i] == "-"):
                gap_found = True
                for j in range(i, len(sequence)):

                    if (sequence[j] != "-"):
                        num_of_gap_sequence += 1
                        i = j - 1
                        break
        # pass
    else:
        return 0

    return num_of_gap_sequence


def selectBestAlignment(alignment):
    best = getMaxConsecutiveGaps(alignment[0][0]) + getMaxConsecutiveGaps(alignment[0][1])
    best_aln = alignment[0]
    for i in range(1, len(alignment)):
        score_a1 = getMaxConsecutiveGaps(alignment[i][0])
        score_a2 = getMaxConsecutiveGaps(alignment[i][1])
        # print (score_a1,score_a2)
        if (score_a1 + score_a2 <= best):
            best = score_a1 + score_a2
            best_aln = alignment[i]

    return best_aln


import sys


def calculatePercentageSimilarity(seq1, seq2):
    l = len(seq1)
    match = 0
    for i in range(l):
        if (seq1[i] == seq2[i]):
            match += 1

    return match


def getInclusionFlag(seq1, seq2):
    similarity = calculatePercentageSimilarity(seq1, seq2)

    return similarity


def mapFunctionGenerator(seq1, seq2, unaligned_seq1,
                         unaligned_seq2):  # generates a mapping function old_fasta_sequence -> aligned_fasta_sequence
    l = len(seq1)
    seq1_dict = {}
    seq1_list = []
    seq2_dict = {}
    seq2_list = []
    for i in range(l):
        if (seq1[i] != "-"):
            seq1_dict[str(i + 1)] = seq1[i]
            seq1_list.append(str(i + 1) + " : " + seq1[i])
        if (seq2[i] != "-"):
            seq2_dict[str(i + 1)] = seq2[i]
            seq2_list.append(str(i + 1) + " : " + seq2[i])

    if (seqDict2Fasta(seq1_dict) != unaligned_seq1): sys.exit("Unaligned sequences dont match!")
    if (seqDict2Fasta(seq2_dict) != unaligned_seq2): sys.exit("Unaligned sequences dont match!")

    map_seq1_list = []
    for i in range(len(unaligned_seq1)):
        map_seq1_list.append(str(i + 1) + " : " + seq1_list[i])
    map_seq2_list = []
    for i in range(len(unaligned_seq2)):
        map_seq2_list.append(str(i + 1) + " : " + seq2_list[i])

    if (len(seq1_dict) == len(unaligned_seq1)): print("Yes")
    if (len(seq2_dict) == len(unaligned_seq2)): print("Yes")

    return map_seq1_list, map_seq2_list


def seqDict2Fasta(seq_dict):
    fasta = ""
    for key in seq_dict.keys():
        fasta += seq_dict[key]
    return fasta


def seq_aligner(key_x, key_y, x, y):
    threshold = 0.95
    # key_x = sys.argv[1]
    # x = sys.argv[2]
    # key_y = sys.argv[3]
    # y = sys.argv[4]
    # x="VVKFTKSEALHKEALEHIVGGVNSPSRSFKAVGGGAPIAERGKGAYFWDVDGNKYIDYLAAYGPIITGHAHPHITKAITTAAENGVLYGTPTALEVKFAKLKEAPALDKVRFVNSGTEAVTTIRVARAYTGRTKIKFAGCYHGHSDLVLVA-------LGTPDSAGVPQSIAQEVITVPFNNVETLKEALDKWGHEVAAILVEPIVGNFGIVEPKPGFLEKVNELVHEAGALVIYDEVITAFRFYGGAQDLLGVTPDLTALGVIGGGLPIGAYGGKKEIEQVAPLGPAYQAGTAGNPASASGIACLEVLQQEGLYEKLDELGATLEKGILEQAAKHNIDITLNRLKGALTVYFTTNTIEDYDAAQDTDGEFGKFFKLLQEGVNLAPSKYEAWFLTTEHTKEDIEYTIEAVGRAFAALADNN-"
    # x="VVKFTKSEALHKEALEHIVGGVNSPSRSFKAVGGGAPIAERGKGAYFWDVDGNKYIDYLAAYGPIITGHAHPHITKAITTAAENGVLYGTPTALEVKFAKLKEAPALDKVRFVNSGTEAVTTIRVARAYTGRTKIKFAGCYHGHSDLVLVALGTPDSAGVPQSIAQEVITVPFNNVETLKEALDKWGHEVAAILVEPIVGNFGIVEPKPGFLEKVNELVHEAGALVIYDEVITAFRFYGGAQDLLGVTPDLTALGVIGGGLPIGAYGGKKEIEQVAPLGPAYQAGTAGNPASASGIACLEVLQQEGLYEKLDELGATLEKGILEQAAKHNIDITLNRLKGALTVYFTTNTIEDYDAAQDTDGEFGKFFKLLQEGVNLAPSKYEAWFLTTEHTKEDIEYTIEAVGRAFAALADN"
    # y="VVKFTKSEALHKEALEHIVGGVNSPSRSFKAVGGGAPIAERGKGAYFWDVDGNKYIDYLAAYGPIITGHAHPHITKAITTAAENGVLYGTPTALEVKFAKLKEAPALDKVRFVNSGTEAVTTIRVARAYTGRTKIKFAGCYHGHSDLVLVAAGSGPSTLGTPDSAGVPQSIAQEVITVPFNNVETLKEALDKWGHEVAAILVEPIVGNFGIVEPKPGFLEKVNELVHEAGALVIYDEVITAFRFYGGAQDLLGVTPDLTALGVIGGGLPIGAYGGKKEIEQVAPLGPAYQAGTAGNPASASGIACLEVLQQEGLYEKLDELGATLEKGILEQAAKHNIDITLNRLKGALTVYFTTNTIEDYDAAQDTDGEFGKFFKLLQEGVNLAPSKYEAWFLTTEHTKEDIEYTIEAVGRAFAALADNK"
    # x="NQALLRILKETEFKKIKVLGSGAFGTVYKGLWIPEGEKVKIPVAIKELANKEILDEAYVMASVDNPHVCRLLGICLTSTVQLIMQLMPFGCLLDYVREHKDNIGSQYLLNWCVQIAKGMNYLEDRRLVHRDLAARNVLVKTPQHVKITDFGLAKLLVPIKWMALESILHRIYTHQSDVWSYGVTVWELMTFGSKPYDGIPASEISSILEKGERLPQPPICTIDVYMIMVKCWMIDADSRPKFRELIIEFSKMARDPQRYLVIQGDERMHLPSPTDSNFYRALMDEEDMDDVVDAD"
    # y="NQALLRILKETEFKKIKVLGSGAFGTVYKGLWIPEGEKVKIPVAIKELREATSPKANKEILDEAYVMASVDNPHVCRLLGICLTSTVQLIMQLMPFGCLLDYVREHKDNIGSQYLLNWCVQIAKGMNYLEDRRLVHRDLAARNVLVKTPQHVKITDFGLAKLLGKVPIKWMALESILHRIYTHQSDVWSYGVTVWELMTFGSKPYDGIPASEISSILEKGERLPQPPICTIDVYMIMVKCWMIDADSRPKFRELIIEFSKMARDPQRYLVIQGDERMHLPSPTDSNFYRALMDEEDMDDVVDAD"
    # alignments = pairwise2.align.globalxx(x, y, one_alignment_only=False)
    alignments = pairwise2.align.globalms(x, y, 5, -4, -1, -0.1)
    # print (len(x),len(y))
    # Use format_alignment method to format the alignments in the list
    """
    for a in alignments:
        print(format_alignment(*a))
        #print (a[0])
        #print(a[1])
        break
    """
    # print (len(alignments))
    best_aln = selectBestAlignment(alignments)
    # print (alignments[1][0])
    # print (alignments[1][1])
    aln_print = key_x + "_" + key_y + " : " + best_aln[0] + ',' + best_aln[1] + '\n'

    file_object = open('../../../../../../PycharmProjects/multiprocessing/seq_aln_dictionary.txt', 'a')
    file_object.write(aln_print)
    file_object.close()

    score = 0
    match = getInclusionFlag(best_aln[0], best_aln[1])
    score = 2 * int(match) / (len(x) + len(y))
    print(score)
    type = ''
    if score >= threshold:
        type = 'homodimer'
    else:
        type = 'heterodimer'
    score_string = key_x + ',' + key_y + ',' + str(score) + ',' + type + '\n'

    file_object = open('../../../../../../PycharmProjects/multiprocessing/dimer_classifier.txt', 'a')
    file_object.write(score_string)
    file_object.close()

    print(aln_print)
