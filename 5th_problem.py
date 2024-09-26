import argparse

# Codon table for translating RNA to proteins
codon_table = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'
}

# Function to reverse complement a DNA sequence
def reverse_complement(dna_sequence):
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(complement.get(base, 'N') for base in reversed(dna_sequence))  # Handles ambiguous nucleotides

# Function to translate a DNA sequence into a protein
def translate_dna_to_protein(dna_sequence):
    protein = []
    for i in range(0, len(dna_sequence) - 2, 3):
        codon = dna_sequence[i:i+3]
        if codon_table.get(codon, '') == '_':  # Stop codon
            break
        protein.append(codon_table.get(codon, ''))
    return ''.join(protein)

# Function to find all ORFs in a sequence
def find_orfs(dna_sequence, min_length):
    orfs = []
    seq_length = len(dna_sequence)
    for frame in range(3):  # Reading frames 0, 1, and 2
        for i in range(frame, seq_length - 2, 3):
            codon = dna_sequence[i:i+3]
            if codon == 'ATG':  # Start codon
                for j in range(i, seq_length - 2, 3):
                    stop_codon = dna_sequence[j:j+3]
                    if stop_codon in ['TAA', 'TAG', 'TGA']:  # Stop codon
                        orf = dna_sequence[i:j+3]
                        if len(orf) >= min_length * 3:  # Filtering by codon length
                            orfs.append(orf)
                        break
    return orfs

# Main function
def main():
    parser = argparse.ArgumentParser(description="Filter ORFs by length and discard short ORFs")
    parser.add_argument("input_file", help="Path to the input file with DNA sequence (output from previous question)")
    parser.add_argument("--min_length", type=int, default=100, help="Minimum number of codons for an ORF to be considered a gene")
    args = parser.parse_args()

    # Read DNA sequence from the plain text file (output from the 4th problem)
    with open(args.input_file, 'r') as file:
        dna_sequence = file.read()

    # Clean the DNA sequence (remove newlines and any header)
    dna_sequence = ''.join(line.strip() for line in dna_sequence.splitlines() if not line.startswith(">"))

    # Find ORFs in the original and reverse complement sequences
    original_orfs = find_orfs(dna_sequence, args.min_length)
    reverse_sequence = reverse_complement(dna_sequence)
    reverse_orfs = find_orfs(reverse_sequence, args.min_length)

    # Translate ORFs to protein strings and collect distinct proteins
    protein_strings = set()
    
    for orf in original_orfs:
        protein = translate_dna_to_protein(orf)
        if protein:
            protein_strings.add(protein)

    for orf in reverse_orfs:
        protein = translate_dna_to_protein(orf)
        if protein:
            protein_strings.add(protein)

    # Write filtered results to output file
    with open('output_5.txt', 'w') as output_file:
        for protein in protein_strings:
            output_file.write(f"{protein}\n")

if __name__ == "__main__":
    main()
