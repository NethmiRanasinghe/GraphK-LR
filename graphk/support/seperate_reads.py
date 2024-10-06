import argparse
import os
from Bio import SeqIO

parser = argparse.ArgumentParser(description='Separate reads in to bins.')

parser.add_argument('--reads', '-r', type=str, required=True)
parser.add_argument('--bins', '-b', type=str, required=True)
parser.add_argument('--output', '-o' ,type=str, required=True)

args = parser.parse_args()

input_file = args.reads
bins_file = args.bins
output_dir = args.output

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read bin assignments
with open(bins_file, 'r') as bf:
    bins = [line.strip() for line in bf]

# Create a dictionary to hold the file handles for each bin
output_handles = {}

# Determine the input format
input_format = "fastq" if input_file.endswith(".fastq") else "fasta"

# Process the input FASTQ/FASTA file and write to corresponding bin files in FASTA format
for index, record in enumerate(SeqIO.parse(input_file, input_format)):
    bin_id = bins[index]
    if bin_id not in output_handles:
        output_file = os.path.join(output_dir, f"bin_{bin_id}.fasta")
        output_handles[bin_id] = open(output_file, 'w')
    
    SeqIO.write(record, output_handles[bin_id], "fasta")  # Always write in FASTA format

# Close all output files
for handle in output_handles.values():
    handle.close()

print("Splitting completed. FASTA files created for each bin.")




