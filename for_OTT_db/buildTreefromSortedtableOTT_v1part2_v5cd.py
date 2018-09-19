import sys
import os
import re
import time
import string
import os.path
from sys import argv
splist = []
taxo5dict = {}; taxo4dict= {};taxo3dict= {}; taxo2dict={};taxo1dict= {};taxodict={}
iklist=[];phlist=[];cllist=[];
treedict1 = {}
tree = ""; tree2= ""
def builttree(infile):
	for line in open(infile,'r'):
		kingdom = "";infrakingdom="";phylum="";classe="";order="";family="";species=""
		kingdom = "k_"+line.split('\t')[0]
		if line.split('\t')[1] != "":
			infrakingdom = "ik_"+line.split('\t')[1]
		else:
			infrakingdom = "ik_unnamed"
		if line.split('\t')[2] != '':
			phylum = "ph_"+line.split('\t')[2]
		else:
			phylum="ph_unamed_"+line.split('\t')[1]
		if line.split('\t')[3] != '':
			Class = "cl_"+line.split('\t')[3]
		else:
			Class = "cl_unamed_"+line.split('\t')[2]+"_"+line.split('\t')[1]
		if line.split('\t')[4] != '':
			order = "or_"+line.split('\t')[4]
		else:
			order = 'or_unamed_'+line.split('\t')[3]+"_"+line.split('\t')[2]+"_"+line.split('\t')[1]
		if line.split('\t')[5] != '':
			family = "fa_"+line.split('\t')[5]
		else:
			family = 'fa_unamed_'+line.split('\t')[4]+"_"+line.split('\t')[3]+"_"+line.split('\t')[2]+"_"+line.split('\t')[1]
		species = "sp_"+line.split('\t')[6].split('\n')[0].replace(':','-').replace('(','').replace(')','').replace('/','')
		splist.append(species)
#		print(species, family, order, Class, phylum, infrakingdom, kingdom)
		if family != "fa_":
			if species != "sp_":
				taxo5dict.setdefault(family, [])
				taxo5dict[family].append(species)
			else:
				print("error", family, species)
		if order != "or_":	
			if family != "fa_":
				taxo4dict.setdefault(order, [])
				taxo4dict[order].append(family)
			else:
				if species != "sp_":
#					print("no family", order, family)
					taxo4dict.setdefault(order, [])
					taxo4dict[order].append(species)
				else:
					print("error", order, species)
		if Class != "cl_":
			if order != "or_":	
				taxo3dict.setdefault(Class, [])
				taxo3dict[Class].append(order)
			else:
				if family != "fa_":
					taxo3dict.setdefault(Class, [])
					taxo3dict[Class].append(family)
				else:
					if species != "sp_":
						taxo3dict.setdefault(Class, [])
						taxo3dict[Class].append(species)
					else:
						print("error", Class, species)
		if phylum != "ph_":
			if Class != "cl_":
				taxo2dict.setdefault(phylum, [])
				taxo2dict[phylum].append(Class)
			else:
				if order != "or_":	
					taxo2dict.setdefault(phylum, [])
					taxo2dict[phylum].append(order)
				else:
					if family != "fa_":
						taxo2dict.setdefault(phylum, [])
						taxo2dict[phylum].append(family)
					else:
						if species != "sp_":
							taxo2dict.setdefault(phylum, [])
							taxo2dict[phylum].append(species)
						else:
							print("error", phylum, species)
		if infrakingdom != "ik_":
			if phylum != "ph_":
				taxo1dict.setdefault(infrakingdom, [])
				taxo1dict[infrakingdom].append(phylum)
			else:
				if Class != "cl_":
					taxo1dict.setdefault(infrakingdom, [])
					taxo1dict[infrakingdom].append(Class)
				else:
					if order != "or_":	
						taxo1dict.setdefault(infrakingdom, [])
						taxo1dict[infrakingdom].append(order)
					else:
						if family != "fa_":
							taxo1dict.setdefault(infrakingdom, [])
							taxo1dict[infrakingdom].append(family)
						else:
							if species != "sp_":
								taxo1dict.setdefault(infrakingdom, [])
								taxo1dict[infrakingdom].append(species)
							else:
								print("error", infrakingdom, species)
		if kingdom != "k_":
			if infrakingdom != "ik_":
				taxodict.setdefault(kingdom, [])
				taxodict[kingdom].append(infrakingdom)
			else:
				if phylum != "ph_":
					taxodict.setdefault(kingdom, [])
					taxodict[kingdom].append(phylum)
				else:
					if Class != "cl_":
						taxodict.setdefault(kingdom, [])
						taxodict[kingdom].append(Class)
					else:
						if order != "or_":	
							taxodict.setdefault(kingdom, [])
							taxodict[kingdom].append(order)
						else:
							if family != "fa_":
								taxodict.setdefault(kingdom, [])
								taxodict[kingdom].append(family)
							else:
								if species != "sp_":
									taxodict.setdefault(kingdom, [])
									taxodict[kingdom].append(species)
								else:
									print("error", kingdom, species)

	ordtree = {};falist=[]
	for ord1, fam in taxo4dict.items():
		tree = ""
		number=0;ordernumber=0
		for fa in fam:
			if fa not in falist:
				falist.append(fa)
				number=int(str(taxo5dict[fa]).count(','))+1
				if tree == "":
					try: 
						tree = "("+str(taxo5dict[fa]).split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+":0)"+'{'+str(int(str(taxo5dict[fa]).count(','))+1)+'}'
					except:
						tree =fa.split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+':0'
				else:
					try: 
						tree = tree+",("+str(taxo5dict[fa]).split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+":0)"+'{'+str(int(str(taxo5dict[fa]).count(','))+1)+'}'
					except:
						tree = tree+',' + fa.split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+':0'
				ordernumber=ordernumber + number
		tree1 = '('+ tree + '){'+str(ordernumber)+'}' #+ ord1
#		print(tree1)
		ordtree[ord1] = tree1
		if tree1 == "":
			print(ord1)


	cltree= {}
	tree2 = "";ordlist=[]
	for Cl1, ord in taxo3dict.items():
		tree1 = "empty"
		number=0;clnumber=0
		for orde in ord:
			if orde not in ordlist:
				ordlist.append(orde)
#				print(Cl1, orde)
				if orde.split('_')[0] == "or":
					number=int(ordtree[orde].split('{')[-1].split('}')[0])
#					print(ordtree[orde], number)
					if tree1 == "empty":
						try: 
							tree1 = str(ordtree[orde])
						except:
							print('error order1')
#							tree = '(' + fa + ')' 
					else:
						try: 
							tree1 = tree1+","+str(ordtree[orde])
						except:
							print('error order2')
				elif orde.split('_')[0] == "fa":
					if orde not in falist:
						falist.append(orde)
						number=int(str(taxo5dict[orde]).count(','))+1
						if tree1 == "empty":
							try: 
								tree1 = "("+str(taxo5dict[orde]).split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+":0)"+'{'+str(int(str(taxo5dict[orde]).count(','))+1)+'}'
							except:
#								tree1 = '(' + orde + ')' 
								print('error fa1')
						else:
							try: 
								tree1 = tree1+",("+str(taxo5dict[orde]).split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+":0)"+'{'+str(int(str(taxo5dict[orde]).count(','))+1)+'}'
#								print(tree1)
							except:
#								tree1 = tree1+',(' + orde + ')' 
								print('error fa2')
					else:
						print(orde, "in Tree[ord]")
				elif orde.split('_')[0] == "sp":
					print(Cl1, "SP")
					if tree1 == "empty":
						tree1 = orde.split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+':0'
					else:
						tree1 = tree1 +','+orde.split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+':0'
				else:
					print(orde)
				clnumber=clnumber+number
#				print("clnumber:",clnumber)
		tree2= '(' + tree1 + '){'+str(clnumber)+'}' #+ Cl1
		if tree1=="empty":
			print(tree2)
		cltree[Cl1]=tree2

	phtree= {};cllist=[]
	for ph1, cl in taxo2dict.items():
		tree2 = ""
		tree1 = ""
		number=0;phnumber=0
		for cle in cl:
			if cle not in cllist:
				cllist.append(cle)
#				print(ph1, cle)
				if cle.split('_')[0] == "cl":
					number=int(cltree[cle].split('{')[-1].split('}')[0])
					if tree1 == "":
						try: 
							tree1 = str(cltree[cle])
#							print(cle, "=>",tree1)
						except:
							print('error cl1')
#							tree = '(' + fa + ')' 
					else:
						try: 
							tree1 = tree1+","+str(cltree[cle])
						except:
							print('error cl2')
				elif cle.split('_')[0] == "or":
					number=int(ordtree[cle].split('{')[-1].split('}')[0])
					if cle not in ordlist:
						ordlist.append(cle)
						if tree1 == "":
							try: 
								tree1 = "("+str(ordtree[cle])+")"#+cle
#								print(cle, '=>', tree1)
							except:
#								tree1 = '(' + orde + ')' 
								print('error clor1')
						else:
							try: 
								tree1 = tree1+",("+str(ordtree[cle])+")"#+cle
							except:
#								tree1 = tree1+',(' + orde + ')' 
								print('error clor2')
				elif cle.split('_')[0] == "fa":
					if cle not in falist:
						falist.append(cle)
						number=int(str(taxo5dict[cle]).count(','))+1
						if tree1 == "":
							try: 
								tree1 = "("+str(taxo5dict[cle]).split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+":0)"+'{'+str(int(str(taxo5dict[cle]).count(','))+1)+'}'
#								print(cle, '=>', tree1)
							except:
#								tree1 = '(' + orde + ')' 
								print('error clfa1')
						else:
							try: 
								tree1 = tree1+",("+str(taxo5dict[cle]).split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+":0)"+'{'+str(int(str(taxo5dict[cle]).count(','))+1)+'}'
							except:
#								tree1 = tree1+',(' + orde + ')' 
								print('error clfa2')
				else:
					print(ph1+"SP")
					if tree1 == "":
						tree1 =cle.split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+':0'
					else:
						tree1 = tree1 +','+cle.split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+':0'
				phnumber=phnumber+number
		tree2= '(' + tree1 + '){'+str(phnumber)+'}'# + ph1
#		print(tree2)
		phtree[ph1]=tree2
#		out1=open("testtree_sc.txt",'a')
#		out1.write(tree2)
#		out1.close()

	iktree= {}
	tree2 = "";phlist=[];i=0;tree1 = ""
	for ik1, ph in taxo1dict.items():
		tree2 = ""
		number=0;iknumber=0
		for phe in ph:
			if phe not in phlist:
				phlist.append(phe)
#				print(ik1, phe)
				if phe.split('_')[0] == "ph":
					number=int(phtree[phe].split('{')[-1].split('}')[0])
					if tree1 == "":
						print(ik1)
						try: 
							tree1 = str(phtree[phe])
						except:
							print('error ph1')
#							tree = '(' + fa + ')' 
					else:
						try: 
							tree1 = tree1+","+str(phtree[phe])
						except:
							print('error ph2')
				elif phe.split('_')[0] == "cl":
					number=int(cltree[phe].split('{')[-1].split('}')[0])
					if tree1 == "":
						print(ik1)
						try: 
							tree1 = str(cltree[phe])
						except:
							print('error phcl1')
#							tree = '(' + fa + ')' 
					else:
						try: 
							tree1 = tree1+","+str(cltree[phe])
						except:
							print('error phcl2')
				elif phe.split('_')[0] == "or":
					number=int(ordtree[phe].split('{')[-1].split('}')[0])
					if tree1 == "":
						print(ik1)
						try: 
							tree1 = str(ordtree[phe])
						except:
#							tree1 = '(' + orde + ')' 
							print('error phor1')
					else:
						try: 
							tree1 = tree1+","+str(ordtree[phe])
						except:
#							tree1 = tree1+',(' + orde + ')' 
							print('error phor2')
				elif phe.split('_')[0] == "fa":
					number=int(str(taxo5dict[phe]).count(','))+1
					if tree1 == "":
						print(ik1)
						try: 
							tree1 = "("+str(taxo5dict[phe]).split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+":0)"+'{'+str(int(str(taxo5dict[phe]).count(','))+1)+'}'
						except:
#							tree1 = '(' + orde + ')' 
							print('error phfa1')
					else:
						try: 
							tree1 = tree1+",("+str(taxo5dict[phe]).split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+":0)"+'{'+str(int(str(taxo5dict[phe]).count(','))+1)+'}'
						except:
#							tree1 = tree1+',(' + orde + ')' 
							print('error phfa2')
				else:
					print(ik1, "SP")
					if tree1 == "":
						print(ik1)
						tree1 = phe.split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+':0'
					else:
						tree1 = tree1 +','+phe.split(',')[0].replace("'","").replace('[','').replace(']','').replace('"',"").replace(',',':0,')+':0'
				iknumber=iknumber+number
		tree2= '(' + tree1 + '){'+str(iknumber)+'}' #+ ik1
		tree1=""
#		print(tree2)
#		out3=open("tree"+ik1,'w')
#		out3.write(tree2)
#		out3.close()
		iktree[ik1]=tree2
		if i > 0:
			out=open("taxotree.txt",'a')
			out.write(',((A'+str(i)+",B"+str(i)+",C"+str(i)+",D"+str(i)+",E"+str(i)+",F"+str(i)+",G"+str(i)+",H"+str(i)+'))0,'+ tree2.replace('{','').replace('}',''))
			out.close()
			tree2=''
			i = i+1
		if i == 0:
			out=open("taxotree.txt",'w')
			out.write('(((A'+str(i)+",B"+str(i)+",C"+str(i)+",D"+str(i)+",E"+str(i)+",F"+str(i)+",G"+str(i)+",H"+str(i)+'))0,'+tree2.replace('{','').replace('}',''))
			out.close()
			i = 1
			tree2=''
		
	out=open("taxotree.txt",'a')
	out.write(')')#Eukaryota')
	out.close()


		
def main():
	script, ottfile = argv
	builttree(ottfile)
main()