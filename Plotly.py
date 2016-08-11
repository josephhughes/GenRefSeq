
"""
This program takes the combined file generated from Combo.py and using the graphics program Plotly generates a scatterplot of tip-root divergence vs. time.Functionality includes zooming into areas of interest and hovering over points where further information is provided such as accession number.
"""

from plotly.offline import plot
from  plotly.graph_objs import *
import csv
import plotly
import argparse


#Argument construct which will parse input argument to the script below
parser=argparse.ArgumentParser()
parser.add_argument('-i','--input',help='Combination file(.tsv) is supplied')
args = parser.parse_args()

#Four empty lists
dists=[]
clusters=[]
accs=[]
years=[]
#Color list using decimal rgb code for 63 colors (http://godsnotwheregodsnot.blogspot.co.uk/2012/09/color-distribution-methodology.html)
cList=['rgb(1,0,103)','rgb(213,255,0)','rgb(255,0,86)','rgb(158,0,142)','rgb(14,76,161)','rgb(255,229,2)',\
'rgb(0,95,57)', 'rgb(0,255,0)', 'rgb(149,0,58)', 'rgb(255,147,126)','rgb(164,36,0)','rgb(0,21,68)','rgb(145,208,203)',\
'rgb(98,14,0)','rgb(107,104,130)', 'rgb(0,0,255)', 'rgb(0,125,181)','rgb(106,130,108)', 'rgb(0,174,126)', 'rgb(194,140,159)',\
'rgb(190,153,112)', 'rgb(0,143,156)','rgb(95,173,78)', 'rgb(255,0,0)', 'rgb(255, 0, 246)', 'rgb(255,2,157)','rgb(104,61,59)',\
'rgb(255,116,163)', 'rgb(150,138,232)', 'rgb(152,255,82)', 'rgb(167,87,64)','rgb(1,255,254)', 'rgb(255,238,232)','rgb(254,137,0)',\
'rgb(189,198,255)','rgb(1,208,255)','rgb(187,136,0)','rgb(117,68,177)','rgb(165,255,210)','rgb(255,166,254)','rgb(119,77,0)',\
'rgb(122,71,130)','rgb(38,52,0)','rgb(0,71,84)','rgb(67,0,44)','rgb(181,0,255)','rgb(255,177,103)','rgb(255,219,102)',\
'rgb(144,251,146)','rgb(126,45,210)','rgb(189,211,147)','rgb(229,111,254)','rgb(222,255,116)','rgb(0,255,120)','rgb(0,155,255)',\
'rgb(0,100,1)','rgb(0,118,255)','rgb(133,169,0)','rgb(0,185,23)','rgb(120,130,49)','rgb(0,255,198)','rgb(255,110,65)','rgb(0,0,0)']

clust_no=0
#Opens the file from the input argument
with open(args.input,'r') as txtin:
        next(txtin) # skip headings
        txtin = csv.reader(txtin, delimiter='\t')
#Splits each column into variables anf then appends each to their corresponding list
	for acc,year,dist,cluster,NofN in txtin:
                years.append(year)
                dists.append(dist)	
		accs.append(acc)
		# Conversion to int is required
		cluster=int(cluster)
		#Associates cluster number with a specific rgb code from cList
		if cList[cluster]:
			clusters.append(cList[cluster])		
		else:
			print cluster + " doesn't exist in cList"
		#Looking for the highest cluster number 
		if cluster >=int(clust_no):
			clust_no=cluster

if clust_no <= 64:
#Format needed to allow offline plotting (https://plot.ly/python/getting-started/)
	plotly.offline.plot({"data":[Scatter(x=years, y=dists, mode="markers", marker=dict(color=clusters,size=6),text=accs)], \
	"layout":Layout(hovermode="closest", \
	xaxis=dict(title="Time(years)"), yaxis=dict(title="root-to-tip divergence"))},auto_open=False)
else:
	print "Unfortunately the scatterplot could not be generated as the cluster count exceeded 64"
