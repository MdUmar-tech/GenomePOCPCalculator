# POCP Calculator

A Python tool for calculating the **Percentage of Conserved Proteins (POCP)** between two genomes using BLASTP.  
The method follows the definition proposed by **Qin, Xie et al., 2014**.

---

## 📖 Description
This tool calculates the **POCP** between two genomic datasets by performing BLASTP searches and identifying conserved proteins based on sequence identity and coverage thresholds.

---

## ✨ Features
- BLASTP comparison between two protein sequence files  
- Customizable thresholds for sequence identity and coverage  
- Multi-threading support for faster processing  
- Simple command-line interface  

---

## ⚙️ Requirements
- Python 3.6+  
- [BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) installed in your system `$PATH`  

---

## 🔧 Installation

### On Ubuntu/Debian
```bash
sudo apt-get install ncbi-blast+
On macOS with Homebrew
```
```bash
brew install blast
Then clone or download this repository.
```
🚀 Usage
1. Annotate genomes with Prokka
```bash
python run_prokka.py --input genome_folder --output prokka_results
```
2. Extract protein sequences
``` bash
python extract_prokka_protein.py --input prokka_results --output proteins/
```
3. Run POCP calculation
```bash
python GenomePOCPCalculator.py \                                       
    -i proteins \
    -o pocp_results \
    -t 8
```
📊 Parameters
Parameter	Description
-i, --input	Folder containing protein FASTA files (.faa)
-o, --output	Output directory where results will be stored
-t, --threads	Number of CPU threads for BLASTP (default: 4)
--clean	Remove intermediate BLAST database and BLAST output files after completion

📂 Output Structure

After execution, the output directory will contain:

pocp_results/
├── db/                  # BLAST databases
├── blast/               # BLAST pairwise results
├── matrix.tsv           # All-vs-all POCP matrix
└── protein_stats.tsv    # Detailed statistics for each genome pair

📊 Output Files
1️⃣ matrix.tsv

All-vs-all POCP percentage matrix.

Example:

        Genome1   Genome2   Genome3
Genome1   100      62.45     58.33
Genome2   62.45    100       60.12
Genome3   58.33    60.12     100

2️⃣ protein_stats.tsv

Detailed statistics for each genome pair:

Genome1	Genome2	Total_Proteins_G1	Total_Proteins_G2	Conserved_G1	Conserved_G2	POCP
🧬 Algorithm Overview

Build BLAST protein databases for each genome.

Perform bidirectional BLASTP comparisons.

Identify conserved proteins based on:

Minimum identity ≥ 40%

Minimum coverage ≥ 50%

Count conserved proteins in both directions.

Calculate POCP using the formula below.

📐 POCP Formula
POCP = ((C1 + C2) / (T1 + T2)) × 100

Where:

C1 = Conserved proteins from Genome 1 against Genome 2

C2 = Conserved proteins from Genome 2 against Genome 1

T1 = Total proteins in Genome 1

T2 = Total proteins in Genome 2

📖 Reference

Qin, Q.-L., Xie, B.-B., Zhang, X.-Y., et al. (2014).
A proposed genus boundary for the prokaryotes based on genomic insights. Journal of Bacteriology, 196(12), 2210–2215. https://doi.org/10.1128/JB.01688-14

🌐 Running on Remote Server (E2E Mode) 
For complete end-to-end (E2E) server setup instructions — including: SSH access Miniconda installation Prokka environment setup Screen session usage Large genome optimization See the full server deployment guide in [E2E.md](E2E.md) so this will link directly to .txt and webpage open if i uplaod txt in github

Future Improvements
Integration of high-speed protein search engines (e.g., DIAMOND, MMseqs2) for large-scale genome comparisons.
Automated visualization of POCP similarity matrices.
Enhanced parallel computing support for high-throughput analyses.

Author
Md Umar

Contact: arc.umar@cusat.ac.in, arc.umar@gmail.com

