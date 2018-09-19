import string
import re
import sys
import os
from sys import argv

def main():
	script, dbfile, ecolodict, parasitedict = argv
	i=0;namelist = []; gbdict= {}; sourcedict = {}; GPSudict = {} ; titledict = {}; countrydict = {}; hostdict={}; envdict = {}; GPSdict = {}; valuelist = []; padict = {};
	for paralist in open(parasitedict, 'r'):
		catpara = paralist.split('\t')[0]
		hostt = paralist.split('\t')[1].split('\n')[0]
		padict.setdefault(hostt, [])
		padict[hostt].append(catpara)
#		print(hostt, catpara)
	for ecololist in open(ecolodict ,'r'):
		if ecololist[0] == '>':
			category = ecololist.split('\n')[0].replace('>','')
#			print(category)
			envdict.setdefault(category, [])
		else:
			for word in ecololist.split('\n')[0].split(', '):
#				print(word)
				envdict[category].append(word)
			
	out = open(dbfile.split('.txt')[0]+ "_compiledv3.3.txt",'w+'); out2 = open('issue_count_v3.3.txt','w+')
	out.write('rank1\trank2\trank3\trank4\tname\t#records\t#title\t#GPS\t#uniqueGPS\tgbnumber\tVp\tVpS\tAp\tPp\tPpS\tOp\tPn\tFw\tMw\tWater\tSediment\tnone\tisolation_source\tlat_lon\tcountry\thost\ttitle\n')
	for line in open(dbfile,'r'):
		if line[0] == '>':
			i = i+1
			rank1 = line.split('\t')[0].split('_')[0].replace('>','')
			rank2 = line.split('\t')[0].split('_')[1]
			rank3 = line.split('\t')[0].split('_')[2]
			rank4 = line.split('\t')[0].split('_')[3]
			genusname = line.split('\t')[0].split('_')[4] 
			spname= line.split('\t')[0].split('_')[5]
			if spname == "cf." or spname == "cf":
				spname = "cf_"+line.split('\t')[0].split('_')[6]
			if spname == "aff.":
				spname = "aff_"+line.split('\t')[0].split('_')[6]
			if spname == "sp.":
				try:
					spname = "sp_"+line.split('\t')[0].split('_')[6]
				except:
					spname = spname
			name=rank1+'\t'+rank2+'\t'+rank3+'\t'+rank4+'\t'+genusname + '_'+spname
			if name not in namelist:
				print(i, name)
				gb = line.split('\t')[1]
				iso = line.split('\t')[2]
				iso_source = line.split('\t')[3]
				GPS = line.split('\t')[4]
				country =line.split('\t')[5]
				host = line.split('\t')[9]
				title = line.split('\t')[12]
				namelist.append(name)
				gbdict.setdefault(name, [])
				gbdict[name].append(gb)
				sourcedict.setdefault(name, [])
				sourcedict[name].append(iso_source)
				GPSudict.setdefault(name, [])
				GPSdict.setdefault(name, [])
				if GPS != '':
					GPSudict[name].append(GPS)
					GPSdict[name].append(GPS)
				titledict.setdefault(name, [])
				titledict[name].append(title)
				countrydict.setdefault(name, [])
				countrydict[name].append(country)
				hostdict.setdefault(name, [])
				if host :
					if host not in padict:
						print('h\t\t\t\t\t', host)
						out2.write(host +'\n')
#						break
					else:
						hostdict[name].append(host)
				for row in open(dbfile,'r'):
					if row[0] == '>':
						try:
							srank1 = row.split('\t')[0].split('_')[0].replace('>','')
							srank2 = row.split('\t')[0].split('_')[1]
							srank3 = row.split('\t')[0].split('_')[2]
							srank4 = row.split('\t')[0].split('_')[3]
							genusname2 = row.split('\t')[0].split('_')[4] 
							spname2= row.split('\t')[0].split('_')[5]
							if spname2 == "cf." or spname == "cf":
								spname2 = "cf_"+row.split('\t')[0].split('_')[6]
							if spname2 == "aff.":
								spname2 = "aff_"+row.split('\t')[0].split('_')[6]
							if spname2 == "sp.":
								try:
									spname2 = "sp_"+row.split('\t')[0].split('_')[6]
								except:
									spname2 = spname2
							name2=srank1+'\t'+srank2+'\t'+srank3+'\t'+srank4+'\t'+genusname2+'_'+spname2
						except:
							print('error:',row.split('\t')[0])
							break
						gb2 = row.split('\t')[1]
						if name == name2 and gb2 != gb:
#							print(name)
							gbdict[name].append(gb2)
							iso_source2 = row.split('\t')[3]
							GPS2 = row.split('\t')[4]
							country2 = row.split('\t')[5]
							title2 = row.split('\t')[12]
							host2 = row.split('\t')[9]
							if iso_source2 not in sourcedict[name]:
								sourcedict[name].append(iso_source2)
							if GPS2 != '':
								GPSdict[name].append(GPS2)
								if GPS2 not in GPSudict[name]:
									GPSudict[name].append(GPS2)
							if country2 not in countrydict[name]:
								countrydict[name].append(country2)
							if title2 not in titledict[name]:
								titledict[name].append(title2)
							if host2 :
								if host2 not in padict:
									print('h2\t\t\t\t\t\t\t\t\t', host2)
									out2.write(host2+'\n')
#									break
								else:
									if host2 not in hostdict[name]:
										hostdict[name].append(host2)
		else:
			print(line)
	for species in namelist:
		f=0;m=0;w=0;s=0; vp=0; pa=0; ap= 0; pp =0; pps=0; op=0; pn=0; nonet=0; noneo=0;envlist = []; envtitlelist= []; envctitlelist= []; envclist= []; hostclist = []; 
		if 'environmental' in species:
			print('removed:', species)
		elif 'uncultured' in species:
			print('removed:', species)
		else:
			for key, values in envdict.items():
				for value in values:
					for title1 in titledict[species]:
						if value in title1:
							valuelist.append(value)
							envlist.append(key)
							if species not in envclist:
								envclist.append(species)
					for source1 in sourcedict[species]:
						if value in source1:
							valuelist.append(value)
							envlist.append(key)
							if species not in envclist:
								envclist.append(species)
					for country1 in countrydict[species]:
						if value in country1:
							valuelist.append(value)
							envlist.append(key)
							if species not in envclist:
								envclist.append(species)
			if str(hostdict[species]) != "['']":
				for hosta in hostdict[species]:
					if 'vertebrate' in padict[hosta]:
						vp = vp +1
						hostclist.append(species)
						for host1 in sourcedict[species]:
							for key, values in envdict.items():
								for value in values:
									if key == 'animal_parasite' and value in host1:
										pa = pa + 1
					elif 'animal' in padict[hosta]:
						ap = ap +1
						hostclist.append(species)
					elif 'plant' in padict[hosta]:
						pp = pp +1
						hostclist.append(species)
						for host1 in sourcedict[species]:
							for key, values in envdict.items():
								for value in values:
									if key == 'plant_parasite' and value in host1:
										pps = pps + 1
					elif 'other' in padict[hosta]:
						op = op + 1
						hostclist.append(species)
					else:
						print(species, padict[hosta])
		if str(hostdict[species]) != "['']":
			if species not in hostclist:
				pn = pn + 1
		
		if species not in envclist:
			noneo = noneo + 1
			
		f = envlist.count('Freshwater')
		m = envlist.count('Marine')
		w = envlist.count('Aquatic')
		s = envlist.count('Sediment')
		out.write(species + '\t' + str(len(gbdict[species]))+'\t'+ str(len(titledict[species]))+'\t'+ str(len(GPSdict[species]))+'\t'+ str(len(GPSudict[species]))+'\t' + str(gbdict[species]) +'\t' + str(vp)+'\t' + str(pa)+ '\t'+ str(ap) + '\t' + str(pp) + '\t'+ str(pps)+ '\t' + str(op)+'\t' + str(pn)+ '\t' + str(f) + '\t' + str(m) + '\t' + str(w) + '\t'+ str(s) +'\t'+ str(noneo)+ '\t' + str(sourcedict[species]) +'\t' + str(GPSudict[species]) + '\t' + str(countrydict[species]) + '\t' + str(hostdict[species]) + '\t' + str(titledict[species]) + '\n')
	out.close()
	for ecololist in open(ecolodict ,'r'):
		if ecololist[0] != '>':
			for word in ecololist.split('\n')[0].split(', '):
				
				out2.write(word + '\t' + str(valuelist.count(word)) + '\n')
	out2.close()

main()