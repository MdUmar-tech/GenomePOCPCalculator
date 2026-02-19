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
    -o pocp_matrix.tsv \
    -t 8
```
📊 Parameters
query_genome → Path to the query genome protein sequence file (FASTA format)

subject_genome → Path to the subject genome protein sequence file (FASTA format)

--output → Output file for BLASTP results (default: blastp_output.txt)

--evalue → E-value threshold for BLASTP (default: 1e-5)

--identity → Minimum sequence identity percentage (default: 40)

--coverage → Minimum alignable region coverage percentage (default: 50)

--num_threads → Number of CPU threads for BLASTP (default: 1)

📂 Example
```bash
python GenomePOCPCalculator.py genome1.faa genome2.faa \
    --output results.txt \
    --identity 40 \
    --coverage 50 \
    --num_threads 4
```
📜 Output
BLASTP output file with detailed results (blastp_output.txt)

Printed POCP value in console, e.g.:

POCP between genome1.faa and genome2.faa: 62.45%
📐 Algorithm
Run BLASTP between query and subject protein sequences

Identify conserved proteins based on identity and coverage thresholds

Calculate POCP using the formula:

📖 Formula & Reference

The Python code implements the calculation of Percentage of Conserved Proteins (POCP), as proposed by Qin, Xie et al., 2014:
POCP = (conserved_proteins_query + conserved_proteins_subject) / 
       (total_proteins_query + total_proteins_subject) * 100

Author
Md Umar

Contact: arc.umar@cusat.ac.in, arc.umar@gmail.com

