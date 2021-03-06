import string
import re
import sys
import os
from sys import argv

def main():
	script, dbfile, listgb = argv
	i=0;namelist = []; gbdict= {}; sourcedict = {}; GPSudict = {} ; titledict = {}; countrydict = {}; GPSdict = {}; valuelist = []; gbtokeep= []; countrylist=[]
	out = open(dbfile.split('.txt')[0]+ "_locationv2.txt",'w+'); 
	out2 = open('issue_location.txt','w+')
#	out.write('rank1\trank2\trank3\trank4\tname\t#records\t#title\t#GPS\t#uniqueGPS\tgbnumber\tlat_lon\tcountry\n')
	for gb in open(listgb, 'r'):
		if gb.split('\n')[0] not in gbtokeep:
			gbtokeep.append(gb.split('\n')[0])
			
	for line in open(dbfile,'r'):
		if line[0] == '>':
			if line.split('\t')[1] in gbtokeep:
				i = i+1
				rank1 = line.split('\t')[0].split('_')[0].replace('>','')
				name=rank1 #+'\t'+rank2+'\t'+rank3+'\t'+rank4+'\t'+genusname + '_'+spname
				if name not in namelist:
					print(i, name)
					gb = line.split('\t')[1]
					GPS = line.split('\t')[4]
					try:
						country =line.split('\t')[5].split(':')[0]
					except:
						country =line.split('\t')[5]
					if country not in countrylist:
						countrylist.append(country)
						out2.write(country+'\n')
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
					countrydict.setdefault(name, [])
					countrydict[name].append(country)
					for row in open(dbfile,'r'):
						if row[0] == '>':
							try:
								srank1 = row.split('\t')[0].split('_')[0].replace('>','')
								name2=srank1 #+'\t'+srank2+'\t'+srank3+'\t'+srank4+'\t'+genusname2+'_'+spname2
							except:
								print('error:',row.split('\t')[0])
								break
							gb2 = row.split('\t')[1]
							if name == name2 and gb2 != gb:
#								print(name)
								gbdict[name].append(gb2)
								GPS2 = row.split('\t')[4]
								title2 = row.split('\t')[12]
								try:
									country2 = row.split('\t')[5].split(':')[0]
								except:
									country2 = row.split('\t')[5]
								if country2 not in countrylist:
									countrylist.append(country2)
									out2.write(country2+'\n')
								if GPS2 != '':
									GPSdict[name].append(GPS2)
									if GPS2 not in GPSudict[name]:
										GPSudict[name].append(GPS2)
#								if country2 not in countrydict[name]:
								countrydict[name].append(country2)
								if title2 not in titledict[name]:
									titledict[name].append(title2)
		else:
			print(line)
	out.write('\t\t\t' + str(countrylist).replace('[','').replace(']','').replace("'","").replace(',','\t') + '\n')
	for species in namelist:
		Freq = []
		for C in countrylist:
			frequence = countrydict[species].count(C)
			Freq.append(frequence)
		out.write(species + '\t' + str(len(gbdict[species]))+'\t'+ str(len(titledict[species]))+'\t'+ str(Freq).replace('[','').replace(']','').replace("'","").replace(',','\t')+ '\n')
#	out.close()
	out2.close()

main()