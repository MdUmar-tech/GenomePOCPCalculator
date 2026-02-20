🖥️ End-to-End (E2E) Server Setup Guide
Running POCP Pipeline on a Remote Linux Server

## This guide explains how to:

1. Connect to a remote server via SSH
2. Install Miniconda
3. Configure Conda environment
4. Install Prokka
5. Upload scripts and genomes
6. Run the POCP workflow using screen
7. Download results
8. Clean up the server

## 🔐 1️⃣ Connect to the Remote Server

From your local machine, connect using your private key:

`ssh -i id_rsa root@164.52.215.50`
If using a .pem key:

`ssh -i mykey.pem root@164.52.215.50`
Enter your password if prompted.

# 📦 2️⃣ Install Miniconda (If Not Already Installed)

Download Miniconda:

`wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
Install:
`bash Miniconda3-latest-Linux-x86_64.sh`
Follow installation prompts and press Enter to accept defaults.
Activate conda:
`source ~/.bashrc`
Verify installation:
`conda --version`
⚙️ 3️⃣ Configure Conda Channels (Important for Bioinformatics)
`conda config --remove-key channels
conda config --add channels conda-forge
conda config --add channels bioconda
conda config --add channels defaults
conda config --set channel_priority strict`

This ensures correct package priority and avoids dependency conflicts.

## 🧬 4️⃣ Create Prokka Environment

Create a dedicated environment:
`conda create -n prokka_env prokka=1.15.6 -y`

Activate environment:
`conda activate prokka_env`
Verify installation:
`prokka --version`
Expected output:
`prokka 1.15.6`
📤 5️⃣ Upload Scripts and Genomes to Server
From your local system terminal:

Upload scripts:
`scp -i mykey.pem run_prokka.py root@164.52.215.50:/root/
scp -i mykey.pem extract_prokka_protein.py root@164.52.215.50:/root/
scp -i mykey.pem GenomePOCPCalculator.py root@164.52.215.50:/root/`

Upload genomes folder:
`scp -i mykey.pem -r genomes root@164.52.215.50:/root/`
🖥️ 6️⃣ Use screen for Long Jobs (Highly Recommended)

Create a new screen session:
`screen -S pocp`

This allows jobs to continue running even if SSH disconnects.

🔹 To Detach (Keep Running in Background)

Press:

Ctrl + A, then D
🔹 To Reattach Later
screen -r pocp

If already attached elsewhere:

screen -d -r pocp
🚀 7️⃣ Run POCP Workflow

Inside screen session:

Step 1: Run Prokka
`python run_prokka.py`

Check results:

`ls prokka_results/`
Step 2: Extract Proteins
`python extract_prokka_protein.py`
Step 3: Run POCP Calculation
`python GenomePOCPCalculator.py \
    -i proteins \
    -o pocp_results \
    -t 18`

Adjust threads (-t) based on server CPU capacity.

## 📥 8️⃣ Download Results to Local Machine

First exit from server:
`exit`

Navigate to desired local directory:
`cd /path/to/your/local/folder`

Download specific files:

`scp -i id_rsa root@164.52.214.201:/root/spades_output/contigs.fasta .`
`scp -i id_rsa root@164.52.214.201:/root/spades_output/scaffolds.fasta .`

Download full POCP results:

`scp -i mykey.pem -r root@164.52.215.50:/root/pocp_results .`
🧹 9️⃣ Clean Up Server (⚠ Use Carefully)

To remove all files inside /root/:
`rm -rf /root/*`

⚠ WARNING:
This permanently deletes all files in /root/.
Use only if you are absolutely sure.

🔚 1️⃣0️⃣ Exit Server
exit
✅ Best Practices

✔ Always use screen or tmux
✔ Activate correct conda environment before running scripts
✔ Use appropriate thread count
✔ Monitor resources with htop
✔ Download results before cleanup
✔ Avoid running heavy jobs directly without screen
