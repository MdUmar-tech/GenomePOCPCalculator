import os
import glob
import subprocess
import shutil

# Input and output directories
input_dir = 'genome/unzipped_genomes'
prokka_out_dir = 'prokka_results'
gff_out_dir = 'prokka_gff'

# Create necessary output directories
os.makedirs(prokka_out_dir, exist_ok=True)
os.makedirs(gff_out_dir, exist_ok=True)

# Get all .fna files in the input directory
fna_files = glob.glob(os.path.join(input_dir, '*.fna'))

# Run Prokka for each .fna file
for fna_file in fna_files:
    base_name = os.path.splitext(os.path.basename(fna_file))[0]
    out_dir = os.path.join(prokka_out_dir, base_name)

    print(f"Running Prokka on: {base_name}")
    
    # Run Prokka
    subprocess.run([
        'prokka',
        '--outdir', out_dir,
        '--prefix', base_name,
        fna_file
    ], check=True)

    # Move the generated GFF file to gff_out_dir
    gff_file = os.path.join(out_dir, f'{base_name}.gff')
    if os.path.exists(gff_file):
        shutil.copy(gff_file, os.path.join(gff_out_dir, f'{base_name}.gff'))
        print(f"Copied: {gff_file} to {gff_out_dir}")
    else:
        print(f"GFF file not found for {base_name}")

print("Prokka annotation completed.")
