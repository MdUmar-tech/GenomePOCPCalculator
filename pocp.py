#!/usr/bin/env python3

import os
import subprocess
import argparse
import itertools
import pandas as pd

# --------------------------------------------------
# Count total proteins in FASTA
# --------------------------------------------------
def count_proteins(fasta_file):
    count = 0
    with open(fasta_file) as f:
        for line in f:
            if line.startswith(">"):
                count += 1
    return count


# --------------------------------------------------
# Build BLAST database (store inside db folder)
# --------------------------------------------------
def build_blast_db(fasta_file, db_dir):
    basename = os.path.basename(fasta_file)
    db_path = os.path.join(db_dir, basename)

    if not os.path.exists(db_path + ".pin"):
        print(f"Building BLAST DB for {basename}")
        subprocess.run([
            "makeblastdb",
            "-in", fasta_file,
            "-dbtype", "prot",
            "-parse_seqids",
            "-out", db_path
        ], check=True)

    return db_path


# --------------------------------------------------
# Run BLASTP
# --------------------------------------------------
def run_blastp(query, db, output, threads):
    cmd = [
        "blastp",
        "-query", query,
        "-db", db,
        "-out", output,
        "-evalue", "1e-5",
        "-outfmt", "6 std qlen",
        "-max_target_seqs", "1",
        "-num_threads", str(threads)
    ]
    subprocess.run(cmd, check=True)


# --------------------------------------------------
# Count conserved proteins
# --------------------------------------------------
def count_conserved(blast_output, identity_threshold=40, coverage_threshold=50):
    conserved = set()

    with open(blast_output) as f:
        for line in f:
            cols = line.strip().split()
            qseqid = cols[0]
            pident = float(cols[2])
            length = float(cols[3])
            qlen = float(cols[12])

            coverage = (length / qlen) * 100

            if pident >= identity_threshold and coverage >= coverage_threshold:
                conserved.add(qseqid)

    return len(conserved)


# --------------------------------------------------
# Calculate POCP
# --------------------------------------------------
def calculate_pocp(C1, T1, C2, T2):
    return ((C1 + C2) / (T1 + T2)) * 100


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="All-vs-All POCP calculator (Improved)")
    parser.add_argument("-i", "--input", required=True, help="Folder containing protein FASTA files (.faa)")
    parser.add_argument("-o", "--output", required=True, help="Output folder")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of BLAST threads")
    parser.add_argument("--clean", action="store_true", help="Remove BLAST database and BLAST output files after completion")

    args = parser.parse_args()

    # -------------------------------
    # Create output structure
    # -------------------------------
    output_dir = args.output
    db_dir = os.path.join(output_dir, "db")
    blast_dir = os.path.join(output_dir, "blast")

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(db_dir, exist_ok=True)
    os.makedirs(blast_dir, exist_ok=True)

    stats_file = os.path.join(output_dir, "protein_stats.tsv")
    matrix_file = os.path.join(output_dir, "matrix.tsv")

    fasta_files = sorted([f for f in os.listdir(args.input) if f.endswith(".faa")])

    genomes = [os.path.join(args.input, f) for f in fasta_files]
    genome_names = [os.path.splitext(f)[0] for f in fasta_files]

    # --------------------------------------------------
    # Build BLAST databases
    # --------------------------------------------------
    print("\nBuilding BLAST databases...")
    db_paths = {}
    for name, path in zip(genome_names, genomes):
        db_paths[name] = build_blast_db(path, db_dir)

    # --------------------------------------------------
    # Count total proteins
    # --------------------------------------------------
    total_proteins = {}
    for name, path in zip(genome_names, genomes):
        total_proteins[name] = count_proteins(path)

    # --------------------------------------------------
    # Prepare POCP matrix
    # --------------------------------------------------
    matrix = pd.DataFrame(index=genome_names, columns=genome_names)

    # Write header if stats file doesn't exist
    if not os.path.exists(stats_file):
        with open(stats_file, "w") as sf:
            sf.write("Genome1\tGenome2\tTotal_Proteins_G1\tTotal_Proteins_G2\t"
                     "Conserved_G1\tConserved_G2\tPOCP\n")

    # --------------------------------------------------
    # All-vs-All comparisons
    # --------------------------------------------------
    for i, j in itertools.combinations(range(len(genomes)), 2):
        name1 = genome_names[i]
        name2 = genome_names[j]

        g1 = genomes[i]
        g2 = genomes[j]

        print(f"\nProcessing: {name1} vs {name2}")

        out1 = os.path.join(blast_dir, f"{name1}_vs_{name2}.tab")
        out2 = os.path.join(blast_dir, f"{name2}_vs_{name1}.tab")

        # Run BLAST both directions
        run_blastp(g1, db_paths[name2], out1, args.threads)
        run_blastp(g2, db_paths[name1], out2, args.threads)

        # Count conserved proteins
        C1 = count_conserved(out1)
        C2 = count_conserved(out2)

        T1 = total_proteins[name1]
        T2 = total_proteins[name2]

        pocp_value = calculate_pocp(C1, T1, C2, T2)

        matrix.loc[name1, name2] = round(pocp_value, 2)
        matrix.loc[name2, name1] = round(pocp_value, 2)

        # Append statistics
        with open(stats_file, "a") as sf:
            sf.write(f"{name1}\t{name2}\t{T1}\t{T2}\t{C1}\t{C2}\t{round(pocp_value,2)}\n")

    # Diagonal = 100
    for g in genome_names:
        matrix.loc[g, g] = 100.0

    matrix.to_csv(matrix_file, sep="\t")

    print(f"\nPOCP matrix saved to: {matrix_file}")
    print(f"Protein statistics saved to: {stats_file}")
    # --------------------------------------------------
    # Cleanup section
    # --------------------------------------------------
    if args.clean:
        print("\nCleaning BLAST intermediate files...")
    
        # Remove BLAST output files
        for file in os.listdir(blast_dir):
            os.remove(os.path.join(blast_dir, file))
    
        # Remove BLAST database files
        for file in os.listdir(db_dir):
            os.remove(os.path.join(db_dir, file))
    
        print("Cleanup complete.")
    
if __name__ == "__main__":
        main()
