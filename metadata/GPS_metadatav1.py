import string
import re
import sys
import os
from sys import argv

def main():
	script, dbfile, listgb = argv
	i=0;namelist = []; gbdict= {}; sourcedict = {}; GPSudict = {} ; titledict = {}; countrydict = {}; GPSdict = {}; valuelist = []; gbtokeep= []; countrylist=[]
	out = open(dbfile.split('.txt')[0]+ "_gpsv2.txt",'w+'); 
	out2 = open('issue_gps.txt','w+')
#	out.write('rank1\trank2\trank3\trank4\tname\t#records\t#title\t#GPS\t#uniqueGPS\tgbnumber\tlat_lon\tcountry\n')
	for gb in open(listgb, 'r'):
		if gb.split('\n')[0] not in gbtokeep:
			gbtokeep.append(gb.split('\n')[0])
			
	for line in open(dbfile,'r'):
		if line[0] == '>':
			if line.split('\t')[1] in gbtokeep:
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
					GPS = line.split('\t')[4].replace('"','').replace('deg','.')
					try:
						country =line.split('\t')[5].split(':')[0]
					except:
						country =line.split('\t')[5]
					title = line.split('\t')[12]
					namelist.append(name)
					titledict.setdefault(name, [])
					titledict[name].append(title)
					gbdict.setdefault(name, [])
					gbdict[name].append(gb)
					GPSudict.setdefault(name, [])
					GPSdict.setdefault(name, [])
					if GPS != '':
						GPSudict[name].append(GPS)
						GPSdict[name].append(GPS)
						if GPS not in countrylist:
							countrylist.append(GPS)
							out2.write(GPS+'\n')
					countrydict.setdefault(name, [])
					countrydict[name].append(country)
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
#								print(name)
								gbdict[name].append(gb2)
								GPS2 = row.split('\t')[4].replace('"','').replace('deg','.')
								title2 = row.split('\t')[12]
								try:
									country2 = row.split('\t')[5].split(':')[0]
								except:
									country2 = row.split('\t')[5]
								if GPS2 != '':
									GPSdict[name].append(GPS2)
									if GPS2 not in countrylist:
										countrylist.append(GPS2)
										out2.write(GPS2+'\n')
									if GPS2 not in GPSudict[name]:
										GPSudict[name].append(GPS2)
#								if country2 not in countrydict[name]:
								countrydict[name].append(country2)
								if title2 not in titledict[name]:
									titledict[name].append(title2)
		else:
			print(line)
	print(len(countrylist))
	out.write('\t\t\t' + str(countrylist).replace('[','').replace(']','').replace("'","").replace(',','\t') + '\n')
	for species in namelist:
		Freq = []
		for C in countrylist:
			frequence = GPSdict[species].count(C)
			Freq.append(frequence)
		print(len(Freq))
		out.write(species + '\t' + str(len(gbdict[species]))+'\t'+ str(len(titledict[species]))+'\t'+ str(Freq).replace('[','').replace(']','').replace("'","").replace(',','\t')+ '\n')
#	out.close()
	out2.close()

main()