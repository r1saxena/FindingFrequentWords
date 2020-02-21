#!/usr/bin/python3

# Finds the most frequent words with k mismatches in a string

def HammingDistance(p, q): 
    '''Compute hamming distance between two dna strings
    
    Args:
        p,q: dna strings

    Returns:
        integer representing hamming distance
    '''
    d = 0 
    for i in range(len(p)):
        if p[i] != q[i]:
            d += 1
    return d

def Neighbors(Pattern, d): 
    ''' Find all neighbors of a pattern

    Find all kmers that all 

    Args:
        Pattern: dna string
        d: hamming distance allowed in pattern

    Returns:
        list of k-mers  
    '''
    if d == 0:
        return [Pattern]
    if len(Pattern) == 1:
        return ['A', 'C', 'G', 'T']
    neighbors = []
    suffixNeighbors = Neighbors(Pattern[1:], d)
    for text in suffixNeighbors:
        if HammingDistance(Pattern[1:], text) < d:
            for x in ['A', 'C', 'G', 'T']:
                neighbors.append(x+text)
        else:
            neighbors.append(Pattern[0]+text)
    return neighbors

def NumberToSymbol(index):
    '''Return nucleotide based on number representation'''
    symArray = ['A', 'C', 'G', 'T']
    return symArray[index]

def NumberToPattern(index, k): 
    '''Convert an integer to its DNA string 

    Args:
        index: integer representing dna string
        k: length of kmer

    Returns: 
        dna string
    '''
    if k == 1:
        return NumberToSymbol(index)
    prefixIndex = index // 4
    r = index % 4 
    symbol = NumberToSymbol(r)
    prefixPattern = NumberToPattern(prefixIndex, k - 1)
    return prefixPattern + symbol

def SymbolToNumber(symbol):
    '''Return number representation of nucleotides'''
    symArray = ['A', 'C', 'G', 'T']
    return symArray.index(symbol)

def PatternToNumber(Pattern):
    '''Convert dna string to number representation

    Args:
        Pattern: dna string

    Returns: 
        integer representation of dna string
    '''
    if len(Pattern) == 0:
        return 0
    symbol = Pattern[-1]
    prefix = Pattern[:-1]
    return 4 * PatternToNumber(prefix) + SymbolToNumber(symbol)

def ApproximatePatternCount(Text, Pattern, d):
    '''Find all approximate occurrences of a pattern in a string

    Args:
        Text: string to search 
        Pattern: string to find
        d: number of mismatches allowed in pattern

    Return: 
        starting positions of pattern in text with at most d mismatches

    '''
    count = 0
    for i in range(len(Text) - len(Pattern) + 1):
        pat = Text[i:i+len(Pattern)]
        if HammingDistance(Pattern, pat) <= d:
            count += 1
    return count

def FrequentWordsWithMismatches(Text, k, d):
    '''Find most frequent kmers with mismatches in a string

    Search a given string Text to find the most frequent substring of
    length k that can have up to d mismatches. 

    Args:
        Text: string to search
        k: length of kmer to search
        d: 

    Return: 
        all most frequent kmers with up to d mismatches in Text
    '''

    FrequentPatterns = []
    close = [0] * (4**k)
    FreqArray = [0] * (4**k) 
    for i in range(len(Text) - k + 1):
        neighborhood = Neighbors(Text[i:i+k], d)
        for pattern in neighborhood:
            index = PatternToNumber(pattern)
            close[index] = 1
    for i in range(4**k):
        if close[i] == 1:
            pattern = NumberToPattern(i, k) 
            FreqArray[i] = ApproximatePatternCount(Text, pattern, d)
    maxCount = max(FreqArray)
    for i in range(4**k):
        if FreqArray[i] == maxCount:
            pattern = NumberToPattern(i, k)
            FrequentPatterns.append(pattern)
    return FrequentPatterns


def PrintOutput(string):
    '''Return formatted output string'''
    return ' '.join(str(i) for i in string)

if __name__=='__main__':
   
    # Test case 1 
    # Expected Output: ATGC ATGT GATG
    Text_1 = "ACGTTGCATGTCGCATGATGCATGAGAGCT"

    k_1 = 4
    d_1 = 1

    # Test case 2
    # Expected Output: GCACACAGAC GCGCACACAC
    Text_2 = "CACAGTAGGCGCCGGCACACACAGCCCCGGGCCCCGGGCCGCCCCGGGCCGGCGGCCGCCGGCGCCGGCACACCGGCACAGCCGTACCGGCACAGTAGTACCGGCCGGCCGGCACACCGGCACACCGGGTACACACCGGGGCGCACACACAGGCGGGCGCCGGGCCCCGGGCCGTACCGGGCCGCCGGCGGCCCACAGGCGCCGGCACAGTACCGGCACACACAGTAGCCCACACACAGGCGGGCGGTAGCCGGCGCACACACACACAGTAGGCGCACAGCCGCCCACACACACCGGCCGGCCGGCACAGGCGGGCGGGCGCACACACACCGGCACAGTAGTAGGCGGCCGGCGCACAGCC"
    k_2 = 10
    d_2 = 2

    patterns_1 = FrequentWordsWithMismatches(Text_1, k_1, d_1)
    print(PrintOutput(patterns_1))

    patterns_2 = FrequentWordsWithMismatches(Text_2, k_2, d_2)
    print(PrintOutput(patterns_2))


