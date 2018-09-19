import string
import re
import sys
import os
from sys import argv

def main():
	script, dbfile, worddict = argv
	i=0;namelist = []; gbdict= {}; sourcedict = {}; GPSudict = {} ; titledict = {}; countrydict = {}; hostdict={}; envdict = {}; GPSdict = {}; valuelist = []
	for wordlist in open(worddict ,'r'):
		if wordlist[0] == '>':
			category = wordlist.split('\n')[0].replace('>','')
#			print(category)
			envdict.setdefault(category, [])
		else:
			for word in wordlist.split('\n')[0].split(', '):
#				print(word)
				envdict[category].append(word)
			
	out = open(dbfile.split('.txt')[0]+ "_compiled_genusb.txt",'w+'); out2 = open(worddict.split('.')[0]+'_usage.txt','w+')
	out.write('rank1\trank2\trank3\trank4\tname\t#records\t#title\t#GPS\t#uniqueGPS\tgbnumber\tPa\tPp\tPn\tFwTitle\tMwTitle\tWaterTitle\tSedimentTitle\tnoneTitle\tFw\tMw\tWater\tSediment\tnone\tisolation_source\tlat_lon\tcountry\thost\ttitle\n')
	for line in open(dbfile,'r'):
		if line[0] == '>':
			i = i+1
			rank1 = line.split('\t')[0].split('_')[0].replace('>','')
			rank2 = line.split('\t')[0].split('_')[1]
			rank3 = line.split('\t')[0].split('_')[2]
			rank4 = line.split('\t')[0].split('_')[3]
			genusname = line.split('\t')[0].split('_')[4] 
			spname= line.split('\t')[0].split('_')[5]
			if spname == "cf.":
				spname = "cf_"+line.split('\t')[0].split('_')[6]
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
							if spname == "cf.":
								spname2 = "cf_"+row.split('\t')[0].split('_')[6]
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
							if host2 not in hostdict[name]:
								hostdict[name].append(host2)
		else:
			print(line)
	for species in namelist:
		f=0;m=0;w=0;s=0; pa= 0; pp =0; pn=0; nonet=0; noneo=0;envlist = []; envtitlelist= []; envctitlelist= []; envclist= []; hostclist = []; 
		if 'environmental' in species:
			print('removed:', species)
		elif 'uncultured' in species:
			print('removed:', species)
		else:
			for key, values in envdict.items():
#				print(values)
				for value in values:
					for title1 in titledict[species]:
						if value in title1:
							valuelist.append(value)
#							print(key, species, titledict[species])
							envtitlelist.append(key)
							if key not in envtitlelist:
								envctitlelist.append(species)
					for source1 in sourcedict[species]:
						if value in source1:
							valuelist.append(value)
#							print(key, species, sourcedict[species])
							envlist.append(key)
							if key not in envlist:
								envclist.append(species)
					for country1 in countrydict[species]:
						if value in country1:
							valuelist.append(value)
#							print(key, species, sourcedict[species])
							envlist.append(key)
							if key not in envlist:
								envclist.append(species)
					if str(hostdict[species]) != "['']":
						for host1 in sourcedict[species]:
							if key == 'animal_parasite' and value in host1:
#								print('parasite:',key)
								pa = pa + 1
								hostclist.append(species)
							elif key == 'plant_parasite' and value in host1:
#								print('parasite:',key)
								pp = pp + 1
								hostclist.append(species)
			if str(hostdict[species]) != "['']":
				if species not in hostclist:
					pn = pn + 1
		
			if species not in envctitlelist:
				nonet = nonet + 1
			if species not in envclist:
				noneo = noneo + 1
			
			f = envlist.count('Freshwater')
			m = envlist.count('Marine')
			w = envlist.count('Aquatic')
			s = envlist.count('Sediment')
			ft = envtitlelist.count('Freshwater')
			mt = envtitlelist.count('Marine')
			wt = envtitlelist.count('Aquatic')
			st = envtitlelist.count('Sediment')
#			print(species, 'F=', f , "M=", m , "W=", w, "S=", s)
			out.write(species + '\t' + str(len(gbdict[species]))+'\t'+ str(len(titledict[species]))+'\t'+ str(len(GPSdict[species]))+'\t'+ str(len(GPSudict[species]))+'\t' + str(gbdict[species]) +'\t' + str(pa)+ '\t' + str(pp)+'\t' + str(pn)+  '\t' + str(ft) + '\t' + str(mt) + '\t' + str(wt) + '\t'+ str(st)+ '\t'+ str(nonet)+ '\t' + str(f) + '\t' + str(m) + '\t' + str(w) + '\t'+ str(s) +'\t'+ str(noneo)+ '\t' + str(sourcedict[species]) +'\t' + str(GPSudict[species]) + '\t' + str(countrydict[species]) + '\t' + str(hostdict[species]) + '\t' + str(titledict[species]) + '\n')
	out.close()
	for wordlist in open(worddict ,'r'):
		if wordlist[0] != '>':
			for word in wordlist.split('\n')[0].split(', '):
				
				out2.write(word + '\t' + str(valuelist.count(word)) + '\n')
	out2.close()

main()