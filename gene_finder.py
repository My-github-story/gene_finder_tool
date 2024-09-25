import argparse

def read_fasta(file_path):
    """Read a FASTA file and return the sequence."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Join lines and remove the FASTA header (first line)
    sequence = ''.join(line.strip() for line in lines if not line.startswith('>'))
    
    return sequence

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Gene Finder Tool')
    parser.add_argument('input_file', help='Path to the input FASTA (.fna) file')
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Read the FASTA file
    sequence = read_fasta(args.input_file)
    
    # (You can add additional code here to process the sequence)
    print(sequence)  # For now, just print the sequence

if __name__ == '__main__':
    main()
