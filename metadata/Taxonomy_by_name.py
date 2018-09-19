#!/usr/bin/python2

__author__ = "Jean-David Grattepanche"
__version__ = "2, September 14, 2016"
__email__ = "jeandavid.grattepanche@gmail.com"



import sys
import os
import re
import urllib2
import time
import string
import os.path
from Bio import SeqIO
from Bio import Entrez
Entrez.email = 'jgrattepanche@smith.edu'
from sys import argv
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast import NCBIXML
from Bio.Blast import NCBIWWW


def Rename(inputfile):
	print("start Adding Name")
	out = open(inputfile.split('.')[0]+'taxonomy.txt','w+')
	IDlist = []; usedID= []; mindate = 1986/01/01 ;
	for record in open(inputfile,'r'): 
		sterm  = record.split('\n')[0]
#		category = record.split('\t')[0]
#		IDlist.append(name)
		searchTerm = '(' + sterm + '[Organism] OR '  + sterm +  '[Organism])'
		handle = Entrez.esearch(db="taxonomy", retmax=1, term= sterm)
		record1 = Entrez.read(handle)
#		print record1 #["Count"]
		ID = record1["IdList"]
#		print ID
		if not ID:
			sterm = record.split(' ')[0]
			searchTerm = '(' + sterm + '[Organism] OR '  + sterm +  '[Organism])'
			handle = Entrez.esearch(db="taxonomy", retmax=1, term= sterm)
			record1 = Entrez.read(handle)
			ID = record1["IdList"]
		if ID :
			handle2 = Entrez.efetch(db="taxonomy", id=ID)
			records2 = Entrez.read(handle2)
			for record2 in records2:
				print  sterm, record2["Lineage"]
				out.write(record.split('\n')[0]+'\t'+ record2["Lineage"] + '\n')
		else:
			print sterm, "no taxID"		
			out.write(record.split('\n')[0]+'\tno taxID\n')
def main():
	script,  NGSfile = argv
	Rename(NGSfile)
main()