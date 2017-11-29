import urllib
import sys
import zipfile
import csv
import math
import random
import numpy

def arrofstr(count):
	index = count.find(',')
	return int(count[1:index]),int(count[index+1:-1])
def readcsv(filen,rowtype):
	alldata = []
	with open(filen, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			if row[0]==rowtype or rowtype=='all':
				alldata.append(row)
	return alldata

allgames = readcsv('2016/allgames.csv','all')
pitchersB = readcsv('2016/Bpitcher.csv','all')
battersB = readcsv('2016/Bbatter.csv','all')

allpitcherelo = []
for pitcher in pitchersB:
	parr = []
	for i in battersB:
		parr.append(pitcher[2:])
	allpitcherelo.append(parr)

allpitcherelo1 = []
for pitcher in pitchersB:
	parr = []
	for i in battersB:
		parr.append(pitcher[2:])
	allpitcherelo1.append(parr)

for i in allgames:
	if random.random()<.5:
		countthing = arrofstr(i[2])[0]+arrofstr(i[2])[1]*4
		for iidx,ii in enumerate(pitchersB):
			if ii[0]==i[0]:
				pid = iidx
				break
		for iidx,ii in enumerate(battersB):
			if ii[0]==i[1]:
				bid = iidx
				break
		pelo = float(allpitcherelo[pid][bid][countthing])
		belo = float(battersB[bid][countthing+2])
		k = 20.
		if i[3]=='B':
			nbchance = 1./(1.+10**((pelo-belo)/400.))
			pelo = pelo+k*nbchance
		else:
			nbchance = 1./(1.+10**((pelo-belo)/400.))
			pelo = pelo-k*nbchance
		allpitcherelo[pid][bid][countthing]=pelo
	else:
		countthing = arrofstr(i[2])[0]+arrofstr(i[2])[1]*4
		for iidx,ii in enumerate(pitchersB):
			if ii[0]==i[0]:
				pid = iidx
				break
		for iidx,ii in enumerate(battersB):
			if ii[0]==i[1]:
				bid = iidx
				break
		pelo = float(allpitcherelo1[pid][bid][countthing])
		belo = float(battersB[bid][countthing+2])
		k = 20.
		if i[3]=='B':
			nbchance = 1./(1.+10**((pelo-belo)/400.))
			pelo = pelo+k*nbchance
		else:
			nbchance = 1./(1.+10**((pelo-belo)/400.))
			pelo = pelo-k*nbchance
		allpitcherelo1[pid][bid][countthing]=pelo

ocorrx = []
ocorry = []
print len(pitchersB)
goodids = []
for pid1,i1 in enumerate(pitchersB):
	ndiff = 0
	for bid in range(0,len(battersB)):
		if allpitcherelo[pid1][bid][0]!=pitchersB[pid1][2]:
			ndiff+=1
	if ndiff > 100:
		goodids.append(pid1)
print len(goodids)

for pid1,i1 in enumerate(pitchersB):
	if pid1%50==20:
		print pid1, numpy.corrcoef(ocorrx,ocorry)[0][1], len(ocorrx)
	if pid1 in goodids:
		
		for pid2,i2 in enumerate(pitchersB[pid1+1:]):
			if pid2 in goodids:
				if pid2!=pid1:
					
					ncc = 0
					ncc1 = 0
					tlength = 0
					for countthing in range(0,12):
						x1 = []
						y1 = []
						x = []
						y = []
						
						for bid in range(0,len(battersB)):
							if abs(float(allpitcherelo[pid1][bid][countthing])-float(pitchersB[pid1][countthing+2]))>12 and abs(float(allpitcherelo[pid2][bid][countthing])-float(pitchersB[pid2][countthing+2]))>12:
								x.append(allpitcherelo[pid1][bid][countthing]-float(pitchersB[pid1][countthing+2]))
								y.append(allpitcherelo[pid2][bid][countthing]-float(pitchersB[pid2][countthing+2]))
						
						for bid in range(0,len(battersB)):
							if abs(float(allpitcherelo1[pid1][bid][countthing])-float(pitchersB[pid1][countthing+2]))>12 and abs(float(allpitcherelo1[pid2][bid][countthing])-float(pitchersB[pid2][countthing+2]))>12:
								x1.append(allpitcherelo1[pid1][bid][countthing]-float(pitchersB[pid1][countthing+2]))
								y1.append(allpitcherelo1[pid2][bid][countthing]-float(pitchersB[pid2][countthing+2]))
						if x != y and x1 != y1:
							ncc += numpy.corrcoef(x,y)[0][1]
							ncc1 += numpy.corrcoef(x1,y1)[0][1]
							tlength+= len(x)+len(x1)

					if tlength>80:
						
						ocorrx.append(ncc)
						ocorry.append(ncc1)
						if ncc>.2:
							print i1[0],i2[0],ncc,ncc1
						if ncc1>.2:
							print i1[0],i2[0],ncc,ncc1
print numpy.corrcoef(ocorrx,ocorry)[0][1], len(ocorrx)


