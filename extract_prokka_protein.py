import os
import shutil
import re

# Input and output directories
input_dir = "../prokka_results"
output_dir = "prokka_protein"

# Make sure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Walk through input_dir and find all .faa files
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".faa"):
            # Full path of original file
            file_path = os.path.join(root, file)

            # Replace spaces (one or more) with underscore
            clean_name = re.sub(r"\s+", "_", file)

            # Destination path
            dest_path = os.path.join(output_dir, clean_name)

            # Copy file
            shutil.copy(file_path, dest_path)
            print(f"Copied: {file_path} -> {dest_path}")

print("✅ All .faa files copied to", output_dir)
