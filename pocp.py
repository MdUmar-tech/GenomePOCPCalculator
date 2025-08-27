import os
import subprocess
import argparse

def run_blastp(query, subject, output, evalue=1e-5, identity=40, coverage=50, num_threads=1):
    """
    Run BLASTP between query and subject genomes.

    Parameters:
    - query: Path to the query protein sequence file (FASTA format).
    - subject: Path to the subject protein sequence file (FASTA format).
    - output: Output file for BLASTP results.
    - evalue: E-value threshold (default: 1e-5).
    - identity: Minimum sequence identity percentage (default: 40).
    - coverage: Minimum alignable region coverage percentage (default: 50).
    - num_threads: Number of threads for BLASTP (default: 1).
    """
    cmd = [
        'blastp',
        '-query', query,
        '-subject', subject,
        '-out', output,
        '-evalue', str(evalue),
        '-outfmt', '6 std qlen',
        '-max_target_seqs', '1',
        '-num_threads', str(num_threads)
    ]
    subprocess.run(cmd)

def count_conserved_proteins(blast_output, identity_threshold=40, coverage_threshold=50):
    """
    Count the number of conserved proteins based on BLASTP results.

    Parameters:
    - blast_output: Path to the BLASTP output file.
    - identity_threshold: Minimum sequence identity percentage (default: 40).
    - coverage_threshold: Minimum alignable region coverage percentage (default: 50).

    Returns:
    - Number of conserved proteins.
    """
    conserved_proteins = 0
    query_proteins = set()

    with open(blast_output, 'r') as f:
        for line in f:
            _, _, _, identity, qcov, _ = line.split()
            if float(identity) >= identity_threshold and float(qcov) >= coverage_threshold:
                conserved_proteins += 1
                query_proteins.add(line.split()[0])

    return conserved_proteins, query_proteins

def calculate_pocp(conserved_proteins_1, total_proteins_1, conserved_proteins_2, total_proteins_2):
    """
    Calculate the Percentage of Conserved Proteins (POCP).

    Parameters:
    - conserved_proteins_1: Number of conserved proteins in genome 1.
    - total_proteins_1: Total number of proteins in genome 1.
    - conserved_proteins_2: Number of conserved proteins in genome 2.
    - total_proteins_2: Total number of proteins in genome 2.

    Returns:
    - POCP value.
    """
    pocp = ((conserved_proteins_1 + conserved_proteins_2) / (total_proteins_1 + total_proteins_2)) * 100
    return pocp

def main():
    parser = argparse.ArgumentParser(description='Calculate POCP between two genomes based on BLASTP results.')
    parser.add_argument('query_genome', help='Path to the query genome protein sequence file (FASTA format).')
    parser.add_argument('subject_genome', help='Path to the subject genome protein sequence file (FASTA format).')
    parser.add_argument('--output', default='blastp_output.txt', help='Output file for BLASTP results.')
    parser.add_argument('--evalue', type=float, default=1e-5, help='E-value threshold for BLASTP (default: 1e-5).')
    parser.add_argument('--identity', type=float, default=40, help='Minimum sequence identity percentage (default: 40).')
    parser.add_argument('--coverage', type=float, default=50, help='Minimum alignable region coverage percentage (default: 50).')
    parser.add_argument('--num_threads', type=int, default=1, help='Number of threads for BLASTP (default: 1).')

    args = parser.parse_args()

    # Run BLASTP
    run_blastp(args.query_genome, args.subject_genome, args.output,
               evalue=args.evalue, identity=args.identity, coverage=args.coverage, num_threads=args.num_threads)

    # Count conserved proteins for both genomes
    conserved_proteins_1, query_proteins_1 = count_conserved_proteins(args.output,
                                                                     identity_threshold=args.identity,
                                                                     coverage_threshold=args.coverage)
    conserved_proteins_2, _ = count_conserved_proteins(args.output,
                                                       identity_threshold=args.identity,
                                                       coverage_threshold=args.coverage)

    # Calculate POCP
    pocp = calculate_pocp(conserved_proteins_1, len(query_proteins_1),
                          conserved_proteins_2, num_proteins(args.subject_genome))

    print(f'POCP between {args.query_genome} and {args.subject_genome}: {pocp:.2f}%')

if __name__ == '__main__':
    main()

#python script_name.py query_genome.fasta subject_genome.fasta --output blastp_output.txt --evalue 1e-5 --identity 40 --coverage 50 --num_threads 4

