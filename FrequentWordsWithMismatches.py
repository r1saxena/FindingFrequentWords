def NumberToSymbol(index):
    symArray = ['A', 'C', 'G', 'T']
    return symArray[index]

def NumberToPattern(index, k): 
    if k == 1:
        return NumberToSymbol(index)
    prefixIndex = index // 4
    r = index % 4 
    symbol = NumberToSymbol(r)
    prefixPattern = NumberToPattern(prefixIndex, k - 1)
    return prefixPattern + symbol

def HammingDistance(p, q): 
    d = 0 
    for i in range(len(p)):
        if p[i] != q[i]:
            d += 1
    return d

def Neighbors(Pattern, d): 
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

def FrequentWordsWithMismatches(Text, k, d):
    FreqArray = {}
    words = []
    for i in range(len(Text)-k+1):
        neighborhood = Neighbors(Text[i:i+k], d)
        for pattern in neighborhood:
            if pattern not in FreqArray:
                FreqArray[pattern] = 0
            FreqArray[pattern] += 1
    maxCount = max(FreqArray.values())
    for i in range(4**k):
        if FreqArray[i] == maxCount:
            pat = NumberToPattern(i, k)
            words.append(pat)
    return words    
            

Text = "ACGTTGCATGTCGCATGATGCATGAGAGCT"
k = 4
d = 1

words = FrequentWordsWithMismatches(Text, k, d)
print(words)


