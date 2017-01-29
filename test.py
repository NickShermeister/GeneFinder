def main():
    print("Hello")
    find_all_ORFs_oneframe('ATGCATGAATGTAGATAGATGTGCCC')

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
    finalstring = ''
    nostopcodon = True
    x = 0

    while nostopcodon:
        if x+2 < len(dna):
            if dna[x:x+3] in ('TAG', 'TAA', 'TGA'):
                nostopcodon = False
                finalstring = dna[0:x]
        else:
            finalstring = dna

        if nostopcodon:
            x += 3

        else:
            return finalstring

    return finalstring


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
    allORFs = []
    stillgoing = True
    tempdna = dna
    temp = 0
    x = 0
    checker = 0
    while stillgoing:
        if tempdna[x:x+3] in ('ATG'):
            print(tempdna + '1')
            allORFs.append(rest_of_ORF(tempdna[x:]))
            temp = len(allORFs[checker])
            tempdna = tempdna[(temp+x+3):]
            print(tempdna)
            checker += 1
            x = 0
            temp = 0
        else:
            x = x + 3
        print(x)
        if checker > 0:
            stillgoing = False
        if x > 10:
            stillgoing = False


    return allORFs
