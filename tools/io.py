
def read_fasta(fd):
    label = fd.readline().strip()

    while label and label.startswith('>'):
        label = label[1:]

        sequences = []
        for line in map(str.strip, fd):
            if not line.startswith('>'):
                sequences.append(line)
            else:
                break

        yield label, sequences
        label = line
