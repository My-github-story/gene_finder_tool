import sys
import argparse

def read_orfs_from_file(filename):
    """Read ORFs from a text file."""
    with open(filename, 'r') as file:
        orfs = file.read().strip().splitlines()
    return orfs

def contains_rbs(orf, rbs_sequences, upstream_length):
    """Check if the ORF contains any RBS within the upstream length."""
    start_codon_index = orf.find('ATG')  # Finding the start codon
    if start_codon_index != -1:
        # Check the sequence upstream of the start codon
        upstream_sequence = orf[max(0, start_codon_index - upstream_length):start_codon_index]
        print(f"Checking ORF: '{orf}'")  # Print the full ORF for debugging
        print(f"Checking upstream sequence: '{upstream_sequence}' for RBS sequences: {rbs_sequences}")
        return any(rbs in upstream_sequence for rbs in rbs_sequences)
    return False

def filter_orfs_with_rbs(orfs, rbs_sequences, upstream_length):
    """Filter ORFs that contain any of the RBS sequences."""
    filtered_orfs = []
    found_rbs_count = 0
    
    for orf in orfs:
        if contains_rbs(orf, rbs_sequences, upstream_length):
            filtered_orfs.append(orf)
            found_rbs_count += 1

    return filtered_orfs, found_rbs_count

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Filter ORFs for Ribosome Binding Sites (RBS)')
    parser.add_argument('input_file', help='Input file containing ORFs')
    parser.add_argument('--output_file', help='Output file to save filtered ORFs', default='output_6.txt')
    parser.add_argument('--rbs_sequences', nargs='+', help='Ribosome Binding Site sequences', 
                        default=['AGGAGG', 'GGAGG', 'GAGG', 'AGG'])  # Add other common RBS sequences here
    parser.add_argument('--upstream_length', type=int, help='Length to scan upstream for RBS', default=20)
    
    args = parser.parse_args()

    # Read ORFs from the input file
    orfs = read_orfs_from_file(args.input_file)
    print(f"Total ORFs read: {len(orfs)}")

    # Filter ORFs for RBS
    filtered_orfs, found_rbs_count = filter_orfs_with_rbs(orfs, args.rbs_sequences, args.upstream_length)

    # Write filtered ORFs to output file
    with open(args.output_file, 'w') as outfile:
        for orf in filtered_orfs:
            outfile.write(orf + '\n')

    print(f"Filtered ORFs saved to {args.output_file}. Found {found_rbs_count} ORFs with RBS.")

if __name__ == '__main__':
    main()
