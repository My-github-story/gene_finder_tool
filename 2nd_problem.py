
import argparse

def read_fasta(file_path):
    """Read a FASTA file and return the sequence."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    sequence = ''.join(line.strip() for line in lines if not line.startswith('>'))
    return sequence

def reversecomplement(dna_string):
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    reverse_complement = ""

    for nucleotide in reversed(dna_string):
        if nucleotide in complement:
            reverse_complement += complement[nucleotide]
        else:
            # If the nucleotide is not A, T, G, or C, skip it
            reverse_complement += 'N'  # 'N' represents any unknown nucleotide

    return reverse_complement

def find_genes(sequence):
    start_codon = "ATG"
    stop_codons = ["TAA", "TAG", "TGA"]
    genes = []

    # Search in three reading frames
    for frame in range(3):
        for i in range(frame, len(sequence) - 2):
            if sequence[i:i+3] == start_codon:  # Check for start codon
                for j in range(i, len(sequence) - 2, 3):
                    if sequence[j:j+3] in stop_codons:  # Check for stop codons
                        genes.append(sequence[i:j+3])  # Capture the gene
                        break

    return genes

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Gene Finder Tool')
    parser.add_argument('input_file', help='Path to the input FASTA (.fna) file')
    args = parser.parse_args()

    # Read the FASTA file
    original_sequence = read_fasta(args.input_file)

    # Find genes in the original sequence
    genes = find_genes(original_sequence)

    # Find genes in the reverse complement
    reverse_sequence = reversecomplement(original_sequence)
    reverse_genes = find_genes(reverse_sequence)

    # Combine results
    all_genes = genes + reverse_genes

    # Output found genes
    for gene in all_genes:
        print(gene)

if __name__ == "__main__":
    main()
