
def parse(raw_string):
    table = raw_string.split()
    codons = table[::2]
    amino_acids = table[1::2]
    return dict(zip(codons, amino_acids))
