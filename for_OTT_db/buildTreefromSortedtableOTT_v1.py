import sys
import os
import re
import time
import string
import os.path
from Bio import SeqIO
from sys import argv

uniqueline=[]
splist = []
def builttree(infile):
	out = open("OTT_5ranks_sorted_Gbank.txt",'w')
	out.write('kingdom'+'\t'+'infrakingdom' +'\t'+ 'phylum'+'\t'+ 'class'+'\t'+ 'order'+'\t'+ 'family'+'\t'+ 'species' +'\t'+'genus'+ '\n')
	out.close()
	taxoun = "";species=""
	i=0 
	for line in open(infile,'r'):
		kingdom = "";infrakingdom="";phylum="";classe="";order="";family="";genus="";taxo=""
		if line.split('\n')[0] not in uniqueline:
			uniqueline.append(line.split('\n')[0])
			kingdom = line.split("\t")[0]
			if "species" in line.split("\n")[0]:
				for element in line.split("\n")[0].split("\t"):
					if element.split('_')[0] == "infrakingdom":
						if infrakingdom != "":
							print("2 infraki ??", infrakindgom, element)
						else:	
							infrakingdom=element.split('_')[1]
					if element.split('_')[0] == "phylum":
						if phylum != "":
							print("2 phylum ??", phylum, element)
						else:
							phylum=element.split('_')[1]
					if element.split('_')[0] == "class":
						if classe != "":
							print('2 classes ??', classe, element)
						else:
							classe=element.split('_')[1]
					if element.split('_')[0] == "order":
						if str(order) != "[]" and str(order) != "":
							print('2 order ??', order, element)
						else:
							order=element.split('_')[1]
					if element.split('_')[0] == "family":
						if family != "":
							print('2 families ??', family, element)
						else:
							family=element.split('_')[1]
					if element.split('_')[0] == "genus":
						if genus != "":
							print('2 genus ??', genus, element)
						else:
							genus=element.split('_')[1]
					if element.split('_')[0] == "species":
						taxo=kingdom+"_"+infrakingdom+"_"+phylum+"_"+classe+"_"+order+"_"+family+"_"+genus+'.'
						if taxoun == taxo:
							try:
								species=species+','+element.split('_')[1]+'-'+element.split('_')[2]
#								print("same taxo", taxoun, taxo, species)
								out = open("OTT_5ranks_sorted_Gbank.txt",'a')
								out.write(','+element.split('_')[1]+'-'+element.split('_')[2])
								out.close()
							except:
								species=species+','+element.split('_')[1]
#								print("same taxo", taxoun, taxo, species)
								out = open("OTT_5ranks_sorted_Gbank.txt",'a')
								out.write(','+element.split('_')[1])
								out.close()
								
						else:
							species=""
							try:
								species=element.split('_')[1]+'-'+element.split('_')[2]
							except:
								species=element.split('_')[1]
#							species1=species
#							print(kingdom,infrakingdom, phylum, classe, order, family, species)
							taxoun = taxo
							out = open("OTT_5ranks_sorted_Gbank.txt",'a')
							out.write('\n'+ kingdom+'\t'+infrakingdom +'\t'+ phylum+'\t'+ classe+'\t'+ order+'\t'+ family+'\t'+genus+ '\t'+species)
							out.close()
				if species not in splist:
					splist.append(species)
			else:
				print("No Species:", line.split('\n')[0])
	print("number of species:", len(splist))#, str(splist))
				
def main():
	script, ottfile = argv
	builttree(ottfile)
main()