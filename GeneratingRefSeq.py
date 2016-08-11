
import subprocess
import csv
import argparse

parser=argparse.ArgumentParser(description='This pipeline generates a near complete genome reference database for a given virus species or genus',epilog='A taxonomic ID, near complete genome threshold and year cut-off needs to be supplied to the Virus.txt file. Further assistance can be obtained from the user manual if required.')

args = parser.parse_args()

with open('Virus.txt','r') as virus_det:
	taxid=""
 	ncompg=""
	year_cutoff=""
	next(virus_det) # skip headings
 	virus_det = csv.reader(virus_det, delimiter='\t')
	print "The first taxid with associated near complete genome threshold and year cut off is being processed.."
	for taxid, ncompg, year_cutoff in virus_det:
		print "Running E-utilities for Genbank files..."
		eutil_str="esearch -db nucleotide -query txid" + taxid + "[Organism]| efetch -format gb >" + taxid +".gb" 	
		subprocess.call(eutil_str, shell=True)
		print "Running E-utilities for FASTA files..."
		fasta_str="esearch -db nucleotide -query txid" + taxid + "[Organism]| efetch -format fasta >"+ taxid +".fasta"
		subprocess.call(fasta_str, shell=True)
		print "Python script to get relevant information and writing these to a tab delimited and fasta file format..."
		backup_str = "python NCompleteGenomes.py -i " + taxid + ".gb -o " + taxid + " -l " + ncompg
		subprocess.call(backup_str, shell=True)
		print "Running MAFFT..."
		mafft_str="mafft --auto " + taxid + ".fa > mafft" + taxid + ".fa"
		subprocess.call(mafft_str, shell=True)
		print  "Running FastTree..."
		fast_str="FastTree -nt mafft" + taxid +".fa > " + taxid + ".tree"
		subprocess.call(fast_str, shell=True)
		print "Running CDHIT..."
		cdhit_str="cd-hit-v4.6.5-2016-0304/cd-hit-est -i "+ taxid + ".fa -o cdhit"+taxid +" -c 0.9 -n 8"
		subprocess.call(cdhit_str, shell=True)
		print "Combining relevant information from CDHIT & FastTree..."
		combo_str="python Combo.py -i cdhit" + taxid + ".clstr -i2 " + taxid + ".tree -o Combo"+ taxid
		subprocess.call(combo_str, shell=True)
		print "Producing a scatterplot..." 
		scatterplot_str = "python Plotly.py -i Combo" + taxid +".tsv"
		subprocess.call(scatterplot_str, shell=True) 
		print "Making a filtered file(.tsv) dependent on cut-off year chosen.."
		filtered_str="python FilteredSeq.py -i Combo" + taxid + ".tsv -o Filtered" + taxid + ".tsv -y " + year_cutoff
		subprocess.call(filtered_str, shell=True)
		print "Getting unique references from each cluster..."
		ref_str="python GetRefseq.py -i Filtered" + taxid +".tsv -i2 " + taxid + ".fasta -o refseq" + taxid + ".txt"
		subprocess.call(ref_str, shell=True)
		#Move all generated files to an appropriately named folder
		subprocess.call(['mkdir',taxid])
		mv_str="mv *" +taxid+ ".* "+ taxid
		subprocess.call (mv_str, shell=True)
		plot_str="mv temp-plot.html " + taxid
		subprocess.call(plot_str, shell=True)
		cdhit_str="mv cdhit" + taxid+ " " + taxid
		subprocess.call(cdhit_str, shell=True)
		mvlog="mv logfile.txt " + taxid
		subprocess.call(mvlog, shell=True)
