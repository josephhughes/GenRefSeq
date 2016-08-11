"""
This program takes the output of the Combo.py script and generates a filtered output based on a year cutoff decided by the user,
for which they would like to obtain sequences.

"""
import argparse 

parser=argparse.ArgumentParser()
parser.add_argument('-i','--input',help='Combination file(.tsv) should be  supplied')
parser.add_argument('-o','--output',help='A file (.tsv) of accession numbers and associated data is generated for a specified time period')
parser.add_argument('-y','--year',help='A year(four digit format) is chosen by which the data will be filtered')
args = parser.parse_args()

fil_year_file=open(args.output,"w")
fil_year_file.write("Accession_no\t Year\t Distance\t ClusterNo\t NumberofN\t \n")
with open(args.input, "r") as combined_file:
	next(combined_file)
	for line in combined_file:
		year=line.split('\t')[1]
		if int(year) >= int(args.year):
			 fil_year_file.write(line)
fil_year_file.close()	
