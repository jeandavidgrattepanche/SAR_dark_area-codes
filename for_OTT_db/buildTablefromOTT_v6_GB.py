import sys
import os
import re
import time
import string
import os.path
from Bio import SeqIO
from sys import argv

parentdict = {}
childdict= {}
childdict2= {}
rankdict= {}
flagdict = {}
rename = {}
parentslist = []
splist = []

ranklist= ["kingdom", "infrakingdom","phylum","class", "order", "family", "genus", "species", "no rank - terminal"]
rename["304358"] = "Eukaryota"
rankdict["304358"] = "kingdom"
flagdict["304358"] = " "

def builttree(infile):
# translate OTT table in various dictionaries. 
	for line in open(infile,'r'):
		name = line.split("\t")[4].replace("_","-").replace(',','-')
		taxID = line.split("\t")[0]
		parent = line.split("\t")[2]
		rank = line.split("\t")[6]
		db = line.split("\t")[8]
		for db1 in db.split(','):
			if "ncbi" in db1:
				if not 'ncbi' in name:
					name = name+"_GBank"
#					print("GBank")
		
		flag = line.split("\t")[12]
		for flag1 in flag.split(','):
			if "extinct" in flag1:
				if not 'extinct' in name:
					name = name+"_extinct"
#					print("Extinct")
				
		rename[taxID] = name
		rankdict[taxID]=rank
		parentdict[taxID]=parent
		flagdict[taxID] = flag
		childdict.setdefault(parent, [])
		childdict[parent].append(taxID)
		if parent not in parentslist:
			parentslist.append(parent)
		if (line.split("\t")[6] == "species") or (line.split("\t")[6] == "no rank - terminal"):
			if taxID not in splist:
				splist.append(taxID)
	print("number of sp:",len(splist))
	print("number of extinct sp:",int(str(splist).count('-extinct-')))
	print("number of sp in GenBank:",int(str(splist).count('_GBank')))
# collapse ranks to 5 ranks removing no rank and other intermediate ranks.
	for ch2, pa2 in parentdict.items():
		if rankdict[ch2] in ranklist:
			while True:
				if rankdict[pa2] in ["kingdom", "infrakingdom","phylum","class", "order", "family","genus"]:
					try:
						if not ch2 in childdict2[pa2]:
							childdict2[pa2].append(ch2)
					except:
						childdict2.setdefault(pa2, []) # create a new dictionary with only the 6 ranks mentioned above! and therefore collapse intermediate ranks such as genus, suborder etc
						childdict2[pa2].append(ch2)
#					print("added:", rename[ch2], rankdict[ch2], rename[pa2], rankdict[pa2])
					break
				else:
#					print("change rank from:",rename[pa2])
					pa2=parentdict[pa2]
#					print("change rank to:",rename[pa2])
						
# create a table using the previous dictionary.
	rank0 = "Eukaryota" 
	for child1 in childdict2["304358"]:
		rank1="";rank2="";rank3="";rank4="";rank5="";rank6="";rank7="";rank8=""
#		print(childdict2["304358"])
#		print("rk1:", ranklist[1], rename[child1])
		rank7= ""
		rank1=rankdict[child1]+'_'+rename[child1] 
		try:
			child2list= childdict2[child1]
		except:
			if rankdict[child1] != "species":
				print("No child for:", rename[child1], rankdict[child1])
			else:
				outtable = open('OTT_Table_Sorted_Gbank.txt','a')
				outtable.write(str(rank0) + '\t'+ str(rank1)+'\t'+str(rank2) + '\t' +str(rank3) + '\t'+ str(rank4) + '\t'+str(rank5) + '\t' + str(rank6) +'\t'+str(rank7)+'\t'+str(rank8) + '\n')
				outtable.close()
			child2list = []
		for child2 in child2list:
			rank2="";rank3="";rank4="";rank5="";rank6="";rank7="";rank8=""
			rank2=rankdict[child2]+'_'+rename[child2] 
			try:
				child3list= childdict2[child2]
			except:
				if rankdict[child2] != "species":
					print("No child for:", rename[child2], rankdict[child2])
				else:
					outtable = open('OTT_Table_Sorted_Gbank.txt','a')
					outtable.write(str(rank0) + '\t'+ str(rank1)+'\t'+str(rank2) + '\t' +str(rank3) + '\t'+ str(rank4) + '\t'+str(rank5) + '\t' + str(rank6) +'\t'+str(rank7) +'\t'+str(rank8)+ '\n')
					outtable.close()
				child3list = []
			for child3 in child3list:
				rank3="";rank4="";rank5="";rank6="";rank7="";rank8=""
				rank3=rankdict[child3]+'_'+rename[child3] 
				try:
					child4list= childdict2[child3]
				except:
					if rankdict[child3] != "species":
						print("No child for:", rename[child3], rankdict[child3])
					else:
						outtable = open('OTT_Table_Sorted_Gbank.txt','a')
						outtable.write(str(rank0) + '\t'+ str(rank1)+'\t'+str(rank2) + '\t' +str(rank3) + '\t'+ str(rank4) + '\t'+str(rank5) + '\t' + str(rank6) +'\t'+str(rank7) +'\t'+str(rank8)+ '\n')
						outtable.close()
					child4list = []
				for child4 in child4list:
					rank4="";rank5="";rank6="";rank7="";rank8=""
					rank4=rankdict[child4]+'_'+rename[child4]
					try:
						child5list= childdict2[child4]
					except:
						if rankdict[child4] != "species":
							print("No child for:", rename[child4], rankdict[child4])
						else:
							outtable = open('OTT_Table_Sorted_Gbank.txt','a')
							outtable.write(str(rank0) + '\t'+ str(rank1)+'\t'+str(rank2) + '\t' +str(rank3) + '\t'+ str(rank4) + '\t'+str(rank5) + '\t' + str(rank6) +'\t'+str(rank7) +'\t'+str(rank8)+ '\n')
							outtable.close()
						child5list = []
					for child5 in child5list:
						rank5="";rank6="";rank7="";rank8=""
						rank5=rankdict[child5]+'_'+rename[child5]
						try:
							child6list= childdict2[child5]
						except:
							if rankdict[child5] != "species":
								print("No Child for:",rankdict[child5], rename[child5])
							else:
								outtable = open('OTT_Table_Sorted_Gbank.txt','a')
								outtable.write(str(rank0) + '\t'+ str(rank1)+'\t'+str(rank2) + '\t' +str(rank3) + '\t'+ str(rank4) + '\t'+str(rank5) + '\t' + str(rank6) +'\t'+str(rank7) +'\t'+str(rank8)+ '\n')
								outtable.close()
							child6list= []
						for child6 in child6list:
							rank6="";rank7="";rank8=""
							rank6=rankdict[child6]+'_'+rename[child6]
							try:
								child7list= childdict2[child6]
							except:
								if rankdict[child6] != "species":
									print("No child for:", rename[child6], rankdict[child6])
								else:
									outtable = open('OTT_Table_Sorted_Gbank.txt','a')
									outtable.write(str(rank0) + '\t'+ str(rank1)+'\t'+str(rank2) + '\t' +str(rank3) + '\t'+ str(rank4) + '\t'+str(rank5) + '\t' + str(rank6) +'\t'+str(rank7)+'\t'+str(rank8) + '\n')
									outtable.close()
								child7list = []
							for child7 in child7list:
								rank7="";rank8=""
								rank7=rankdict[child7]+'_'+rename[child7]
								try:
									child8list= childdict2[child7]
								except:
									if rankdict[child7] != "species":
										print("No child for:", rename[child7], rankdict[child7])
									else:
										outtable = open('OTT_Table_Sorted_Gbank.txt','a')
										outtable.write(str(rank0) + '\t'+ str(rank1)+'\t'+str(rank2) + '\t' +str(rank3) + '\t'+ str(rank4) + '\t'+str(rank5) + '\t' + str(rank6) +'\t'+str(rank7)+'\t'+str(rank8) + '\n')
										outtable.close()
									child8list = []
								for child8 in child8list:
									rank8=""
									rank8=rankdict[child8]+'_'+rename[child8]
									if rankdict[child8] != "species":
										print("No child for:", rename[child7], rankdict[child7])
									else:
										outtable = open('OTT_Table_Sorted_Gbank.txt','a')
										outtable.write(str(rank0) + '\t'+ str(rank1)+'\t'+str(rank2) + '\t' +str(rank3) + '\t'+ str(rank4) + '\t'+str(rank5) + '\t' + str(rank6) +'\t'+str(rank7)+'\t'+str(rank8) + '\n')
										outtable.close()

def main():
	script, ottfile = argv
	builttree(ottfile)
main()