# -*- coding: utf-8 -*-
"""
YOUR HEADER COMMENT HERE

@author: Nicholas Sherman

"""

import random
from amino_acids import aa, codons, aa_table   # you may find these useful
from load import load_seq


def shuffle_string(s):
    """Shuffles the characters in the input string
        NOTE: this is a helper function, you do not
        have to modify this in any way """
    return ''.join(random.sample(s, len(s)))

# YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """
    if nucleotide == 'A':
        return 'T'
    elif nucleotide == 'C':
        return 'G'
    elif nucleotide == 'G':
        return 'C'
    else:
        return 'A'


def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence

        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    complementary = ''
    reversedna = dna[::-1]
    for base in reversedna:
        complementary = complementary + get_complement(base)
    return complementary


def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start
        codon and returns the sequence up to but not including the
        first in frame stop codon.  If there is no in frame stop codon,
        returns the whole string.

        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """
    #TAG, TAA, TGA are the stop codons
    for n in range(0, (len(dna)-len(dna)%3), 3):
        if dna[n] in ('T'):
            codon = dna[n: n + 3]
            if codon in ('TAG', 'TAA', 'TGA'):
                return dna[:n]
    return dna
    """
    while nostopcodon:
        if x+2 < len(dna):
            if dna[x:x+3] in ('TAG', 'TAA', 'TGA'):
                nostopcodon = False
                finalstring = dna[0:x]
        else:
            finalstring = dna

        if nostopcodon:
            x += 3
        elif x > 300:
            return finalstring
        else:
            return finalstring

    return finalstring
    """

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA
        sequence and returns them as a list.  This function should
        only find ORFs that are in the default frame of the sequence
        (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        start codon is ATG
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    """
    allORFs1 = []
    tempdna = dna
    locORFs = []
    count = 0
    y = 0
    for x in range(0, (len(dna)-len(dna)%3), 3):
        if tempdna[y:(y+3)] == ('ATG'):
            #locORFs.append(x)
            allORFs1.append(rest_of_ORF(tempdna[y:]))
            y = y + len(allORFs1[count])
            count+=1
        y += 3

    return allORFs1

    """
    Something broke in here. I don't know what and I gave up trying to fix it because I don't understand whatever it is I broke.
    allORFs = []
    stillgoing = True
    tempdna = dna
    checkertempdna = dna
    temp = 0
    x = 0
    checker = 0
    while stillgoing:
        print('line1')
        if tempdna[x:(x+3)] in ("ATG"):
            print(tempdna + '1')
            allORFs.append(rest_of_ORF(tempdna[x:]))
            temp = len(allORFs[-1])
            checkertempdna = tempdna[(temp+x+3):]
            print(checkertempdna)
            checker += 1
            temp = 0
        else:
            print('line3')
            x = x + 3
        print(checker)
        x = x + 3
        checker += 1
        if checker > 3:
            stillgoing = False
        tempdna = checkertempdna

    return allORFs
    """

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in
        all 3 possible frames and returns them as a list.  By non-nested we
        mean that if an ORF occurs entirely within another ORF and they are
        both in the same frame, it should not be included in the returned list
        of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    tempdna = dna
    allORFs2 = []
    frameORFs = []

    for frame in range(0, 3):
        frameORFs = (find_all_ORFs_oneframe(dna[frame:]))
        for x in frameORFs:
            allORFs2.append(x)
    return allORFs2


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    tempdna = dna
    reversetempdna = get_reverse_complement(dna)
    forward = (find_all_ORFs(tempdna))
    backward = (find_all_ORFs(reversetempdna))
    return (forward + backward)


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    allORFs = find_all_ORFs_both_strands(dna)
    index = 0
    maxlen = 0
    curlen = 0
    maxlenindex = 0
    for orf in allORFs:
        curlen = len(orf)
        if curlen > maxlen:
            maxlen = curlen
            maxlenindex = index
        index += 1
    return allORFs[maxlenindex]


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence

        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    #shuffle_string()
    maxlen = 0
    tempdna = shuffle_string(dna)
    for i in range(num_trials):
        if maxlen < len(longest_ORF(tempdna)):
            maxlen = len(longest_ORF(tempdna))
        tempdna = shuffle_string(dna)
    print(maxlen)
    return maxlen



def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).

        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    count = ''
    for x in range(0, len(dna)-(len(dna)%3), 3):
        count = count + aa_table[dna[x:x+3]]
    return count


def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna

        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    threshold = longest_ORF_noncoding(dna, 1500)
    allORFSfinal = []
    allORFSfinal = find_all_ORFs_both_strands(dna)
    AAcodes = []
    print(len(dna))
    for x in allORFSfinal:
        if len(x) > threshold:
            AAcodes.append(coding_strand_to_AA(x))
    print(len(allORFSfinal))
    return AAcodes


"""if __name__ == "__main__":
    import doctest
    #doctest.testmod()
    doctest.run_docstring_examples(coding_strand_to_AA, globals(), verbose=True)
"""
