"""
This program will use a Genbank file downloaded from NCBI with
multiple records to extract accession number, length of sequence, collection date
if available ,first publication year, number of ambigious nucleotides  and write these to file
Sources of reference are:
http://www.ece.drexel.edu/gailr/EESI/tutorial_data.php
http://wilke.openwetware.org/Parsing_Genbank_files_with_Biopython.html
http://www2.warwick.ac.uk/fac/sci/moac/people/students/peter_cock/python/genbank/#indexing_features
"""
from Bio import SeqIO
import re
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-i','--input',help='Reading a  Genbank file')
parser.add_argument('-o','--output', help='Writing to a text file')
parser.add_argument('-l','--length', type=int, help='Supplying an appropriate threshold for a near complete genome')

args = parser.parse_args()

#Creating dictionaries for each piece of information required from Genbank file
dna_seq={}
lengthseq={}
pubdate={}
colldate_dict={}
term_cnt=0
gen_record_cnt=0
N_dict={}
#print "Looping through each Genbank record to get relevant information..."
#Opening the file and looping through each record to obtain the relevant information. "r" is for read only.
for gen_record in SeqIO.parse(open(args.input,"r"), "genbank"):
#Counts the number of ambigious nucleotides(N) found in the sequence and placing this in a dictionary	
	n_cnt=0
	for i in gen_record.seq:
		if i == 'N':
			n_cnt+=1
	N_dict[gen_record.id]=n_cnt	
  #Counter of how many records are being read for each sequence which will be printed out to logfile
  	gen_record_cnt+=1
	#Want to filter out the records which have the terms within the description shown below
	#using a simple regular expression.
	des_str=gen_record.description
	term =re.search (r'vector|Patent|clone|Chimeric|chimeric|VACCINE|Vaccines|vaccine|attenuated|Modified|adapted|fusion', des_str)
	#Using an if/else statment only the records which do not have the terms
	# within their description  will be processed further within the else part of the statement.
	if term:
		term_cnt+=1	
	else:		
	#Making a dictionary of the length of sequence with a key being the id
		lengthseq [gen_record.id]= len(gen_record.seq)
	#Making a dictionary of the sequences with a key being the id
		dna_seq[gen_record.id] = (gen_record.seq)

  	# Within the record is an 'annotations' dictionary which can be accessed 
	#with the key 'references' which is in a list.
		young_year=10000		
		for i in gen_record.annotations.keys():
			if i == 'references':
				for ref in gen_record.annotations["references"]:
					#Looping through the references for each gen_record and storing this in a variable
					journal_str=(ref.journal)
					# Reg expression search looking for years 4 digits and starting with
					# a format of 19 or 20 or dd-mm-yyyy
					year=re.search(r'\((19\d{2})\)|\((20\d{2})\)|\d{2}-\w{3}-\d{4}',journal_str)
					#Using the regular expression function to remove brackets and dd-mmm
					# from string
					if year:
						year_str=str(year.group(0))
						year_str=re.sub('[()]','', year_str)
						year_str=re.sub(r'(^\d{2})-(\w{3})-','',year_str)
					# Looping through the different years to find the earliest one
					# and making a new dictionary
						if int(year_str)<= int(young_year):
							young_year=year_str
							pubdate[gen_record.id]=young_year


						
		#Within each features list are types ('source', 'CDS') containing a nested list called qualifiers
		#with collection_date extracted with removal of square brackets, dd-mmm and mmm and making new dictionary
	
		for fea in gen_record.features:
			if fea.type=='source':
				source= gen_record.features[0]
				for qual in source.qualifiers:
					if qual=='collection_date':
						colldate=source.qualifiers['collection_date']
						colldate=str(colldate)
						m = re.match(r'.*(19\d{2}|20\d{2}).*', colldate)
						if m:
							colldate_dict[gen_record.id]=m.group(1)
						else:
							print colldate

#Making both fasta_file and tab delimited file(.tsv) with only ones being printed which are above the size_cuttoff.
#The fasta file contains accession number, Number of ambigious nucleotides, collection date if available (or publication) and DNA sequence.
#The tab delimited file contains all data and if collection date is absence is filled with na (not available).

#print "Printing relevant information to both a tab delimited file(.tsv) and a fasta format file(.fa)"
log_file=open("logfile.txt", "w")
log_file.write("E-utilities downloaded " + str(gen_record_cnt) + " sequences \n")
fasta_file=open(args.output + ".fa","w")
tsv_file=open(args.output + ".tsv", "w")
tsv_file.write("Accession_no\t Seq_length\t NumberofN\t Coll_Date\t Pub_Date\t \n")
align_cnt=0
for key, value in lengthseq.iteritems():
	#The user will need to supply a threshold which will be deemed acceptable for a 'near complete genome'
	#Only above this will the relevant information be stored
	if value > int (args.length):
		acc_no=key
		seqlength=value
		align_cnt+=1
		tsv_file.write(acc_no + "\t" + str(seqlength) + "\t" +str(N_dict[key])+ "\t")
		if key in colldate_dict:
			pcolldate= colldate_dict[key]			
			tsv_file.write("%s\t" % str(pcolldate))
			fasta_file.write(">%s_%s_N%s %s \n" % (acc_no,str(pcolldate),str(N_dict[key]),'\n'+dna_seq[key]))
		else:
			tsv_file.write("na\t")
			if key in pubdate:
				ppubdate=pubdate[key]
				fasta_file.write(">%s_%s_N%s %s \n" % (acc_no,str(ppubdate),str(N_dict[key]),'\n'+ dna_seq[key]))
			else:
				log_file.write("This does not fufill the selection criteria " + acc_no + "\n")
		if key in pubdate:
			tsv_file.write("%s\t" % str(pubdate[key]))
		tsv_file.write("\n")
log_file.write("The number of sequences to be aligned are:" + str(align_cnt)+"\n")
			
tsv_file.close()
fasta_file.close()
log_file.close()


