#!/usr/bin/env python3

import os
import glob
import subprocess
import shutil
import argparse
import sys

# --------------------------------------------------
# Argument Parser
# --------------------------------------------------
parser = argparse.ArgumentParser(
    description="Run Prokka on multiple genomes and extract GFF and FAA files."
)

parser.add_argument(
    "-i", "--input",
    required=True,
    help="Input directory containing FASTA genome files (.fna, .fasta, .fa, .fas)"
)

parser.add_argument(
    "-o", "--outdir",
    default="prokka_results",
    help="Output directory for Prokka results (default: prokka_results)"
)

parser.add_argument(
    "-t", "--threads",
    type=int,
    default=6,
    help="Number of CPU threads for Prokka (default: 6)"
)

args = parser.parse_args()

# --------------------------------------------------
# Directory Setup
# --------------------------------------------------
input_dir = args.input
prokka_out_dir = args.outdir
threads = args.threads

gff_out_dir = os.path.join(prokka_out_dir, "prokka_gff")
protein_out_dir = os.path.join(prokka_out_dir, "proteins")

os.makedirs(prokka_out_dir, exist_ok=True)
os.makedirs(gff_out_dir, exist_ok=True)
os.makedirs(protein_out_dir, exist_ok=True)

# --------------------------------------------------
# Get all FASTA files
# --------------------------------------------------
fna_files = sorted([
    f for f in glob.glob(os.path.join(input_dir, "*"))
    if f.endswith((".fna", ".fasta", ".fa", ".fas"))
])

if not fna_files:
    print("❌ No FASTA files (.fna/.fasta/.fa/.fas) found in input directory.")
    sys.exit(1)

print(f"📂 Found {len(fna_files)} genome files.")

# --------------------------------------------------
# Run Prokka
# --------------------------------------------------
for fna_file in fna_files:
    base_name = os.path.splitext(os.path.basename(fna_file))[0]
    out_dir = os.path.join(prokka_out_dir, base_name)

    print(f"\n🔬 Running Prokka on: {base_name}")

    # Skip if already processed
    if os.path.exists(out_dir):
        print(f"⚠ Skipping {base_name}, output already exists.")
        continue

    try:
        subprocess.run([
            "prokka",
            "--outdir", out_dir,
            "--prefix", base_name,
            "--cpus", str(threads),
            "--kingdom", "Bacteria",
            fna_file
        ], check=True)

    except subprocess.CalledProcessError:
        print(f"❌ Prokka failed for {base_name}")
        continue

    # --------------------------------------------------
    # Copy GFF
    # --------------------------------------------------
    gff_file = os.path.join(out_dir, f"{base_name}.gff")
    if os.path.exists(gff_file):
        shutil.copy(gff_file, os.path.join(gff_out_dir, f"{base_name}.gff"))
        print(f"✔ Copied GFF: {base_name}.gff")
    else:
        print(f"⚠ GFF not found for {base_name}")

    # --------------------------------------------------
    # Copy FAA (proteins)
    # --------------------------------------------------
    faa_file = os.path.join(out_dir, f"{base_name}.faa")
    if os.path.exists(faa_file):
        shutil.copy(faa_file, os.path.join(protein_out_dir, f"{base_name}.faa"))
        print(f"✔ Copied Protein: {base_name}.faa")
    else:
        print(f"⚠ FAA not found for {base_name}")

print("\n✅ Prokka annotation completed successfully.")
