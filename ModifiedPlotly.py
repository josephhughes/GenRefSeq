"""
This program takes the combined file generated from Combo.py and using the graphics program Plotly generates a scatterplot of tip-root divergence vs. time.
Functionality includes zooming into areas of interest and hovering over points where further information is provided such as accession number.

"""

from plotly.offline import download_plotlyjs, init_notebook_mode, plot
from plotly.graph_objs import *
import csv
import plotly
import argparse


#Argument construct which will parse input argument to the script below
parser=argparse.ArgumentParser()
parser.add_argument('-i','--input',help='Combination file(.tsv) is supplied')
args = parser.parse_args()

#Three empty lists
dists=[]
accs=[]
years=[]

#Opens the file from the input argument
with open(args.input,'r') as txtin:
        next(txtin) # skip headings
        txtin = csv.reader(txtin, delimiter='\t')
#Splits each column into variables anf then appends each to their corresponding list
	for acc,year,dist,cluster, NofN in txtin:
                years.append(year)
                dists.append(dist)	
	              accs.append(acc)
		
#Format needed to allow offline plotting (https://plot.ly/python/getting-started/)
	plotly.offline.plot({"data":[Scatter(x=years, y=dists, mode="markers", marker=dict(size=6),text=accs)], \
	"layout":Layout(hovermode="closest", \
	xaxis=dict(title="Time(years)"), yaxis=dict(title="root-to-tip divergence"))})
