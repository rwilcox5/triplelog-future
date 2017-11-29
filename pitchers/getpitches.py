import urllib
import sys
import zipfile
import csv
import math
import random

theyear = sys.argv[1]
if sys.argv[2]==True:
	urllib.urlretrieve("http://www.retrosheet.org/events/"+str(theyear)+"eve.zip", "2016/events"+str(theyear)+".zip")
	zip_ref = zipfile.ZipFile("2016/events"+str(theyear)+".zip", 'r')
	zip_ref.extractall("2016/")
	zip_ref.close()

def toelo(pct):
	return -200.*math.log(1./pct-1.)/math.log(10.)+1500.
def topct(alleloarrays,idx,bidx,countthing):
	return [1./(1.+10**((alleloarrays[0][1][bidx][1][countthing]-alleloarrays[0][0][idx][1][countthing])/400.)),1./(1.+10**((alleloarrays[1][1][bidx][1][countthing]-alleloarrays[1][0][idx][1][countthing])/400.)),1./(1.+10**((alleloarrays[2][1][bidx][1][countthing]-alleloarrays[2][0][idx][1][countthing])/400.)),1./(1.+10**((alleloarrays[3][1][bidx][1][countthing]-alleloarrays[3][0][idx][1][countthing])/400.)),1./(1.+10**((alleloarrays[4][1][bidx][1][countthing]-alleloarrays[4][0][idx][1][countthing])/400.))]
def writecsv(parr, filen):
		with open(filen, 'wb') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				for i in range(0,len(parr)):
						spamwriter.writerow(parr[i])
def readcsv(filen,rowtype):
	alldata = []
	with open(filen, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			if row[0]==rowtype or rowtype=='all':
				alldata.append(row)
	return alldata

allrows = []
for alteam in ['ANA','BAL','BOS','CHA','CLE','DET','HOU','KCA','MIN','NYA','OAK','SEA','TBA','TEX','TOR']:
	allrows = allrows+readcsv("2016/2016"+alteam+".EVA",'all')
for nlteam in ['ARI','ATL','CHN','CIN','COL','LAN','MIA','MIL','NYN','PHI','PIT','SDN','SFN','SLN','WAS']:
	allrows = allrows+readcsv("2016/2016"+nlteam+".EVN",'all')
allgames = []
allpas0 = []
allpas1 = []
for i in range(0,len(allrows)):
	if allrows[i][0]=='id':
		game = []
		for ii in range(i+1,len(allrows)):

			if allrows[ii][0]=='id':
				break
			elif allrows[ii][0]=='play':
				if random.random()<1:
					if allrows[ii][2]==str(0):
						count = [0,0]
						allpas0.append([hpitcher,allrows[ii][6]])
						for iii in range(0,len(allrows[ii][5])):
							cc = [count[0],count[1]]
							if allrows[ii][5][iii]=='X':
								game.append([hpitcher,allrows[ii][3],cc,allrows[ii][5][iii],allrows[ii][6]])
							else:
								game.append([hpitcher,allrows[ii][3],cc,allrows[ii][5][iii],''])
							if allrows[ii][5][iii] in ['B','I','P']:
								count[0]+=1
							elif allrows[ii][5][iii] in ['C','S','F','L','M','Q','R','K'] and count[1]<2:
								count[1]+=1
					if allrows[ii][2]==str(1):
						count = [0,0]
						allpas0.append([vpitcher,allrows[ii][6]])
						for iii in range(0,len(allrows[ii][5])):
							cc = [count[0],count[1]]
							if allrows[ii][5][iii]=='X':
								game.append([vpitcher,allrows[ii][3],cc,allrows[ii][5][iii],allrows[ii][6]])

							elif allrows[ii][5][iii] in ['C','S','F','L','M','Q','R','K','B','I','P']:
								game.append([vpitcher,allrows[ii][3],cc,allrows[ii][5][iii],''])

							if allrows[ii][5][iii] in ['B','I','P']:
								count[0]+=1
							elif allrows[ii][5][iii] in ['C','S','F','L','M','Q','R','K'] and count[1]<2:
								count[1]+=1
				else:
					if allrows[ii][2]==str(0):
						allpas1.append([hpitcher,allrows[ii][3],allrows[ii][6]])
					if allrows[ii][2]==str(1):
						allpas1.append([vpitcher,allrows[ii][3],allrows[ii][6]])

			elif allrows[ii][0]=='start':
				if allrows[ii][5]==str(1):
					if allrows[ii][3]==str(0):
						vpitcher = allrows[ii][1]
					else:
						hpitcher = allrows[ii][1]
			elif allrows[ii][0]=='sub':
				if allrows[ii][5]==str(1):
					if allrows[ii][3]==str(0):
						vpitcher = allrows[ii][1]
					else:
						hpitcher = allrows[ii][1]
		allgames.append(game)

print len(allgames)


def getallelos(allgames,pitchtype,pitchers,batters):
	thispitch = [0,0,0,0,0,0,0,0,0,0,0,0,0]
	allpitches = [0,0,0,0,0,0,0,0,0,0,0,0,0]
	for i in allgames:
		for ii in i:
			try:
				allpitches[0]+=1
				allpitches[ii[2][0]+ii[2][1]*4+1]+=1
				if ii[3]==pitchtype:
					thispitch[0]+=1
					thispitch[ii[2][0]+ii[2][1]*4+1]+=1
			except:
				print ii[2], ii,pitchtype

	thispitchelos = []
	for i in range(0,13):
		ballpct = thispitch[i]*1./allpitches[i]
		getelo = toelo(ballpct)
		thispitchelos.append(getelo)

	

	pitcher_array = []
	for i in pitchers:
		pitcher_elos = []
		my_elo = thispitchelos[0]
		for ii in i[1:]:
			thepitch = allgames[ii[0]][ii[1]]
			if thepitch[3]==pitchtype:
				nbchance = 1./(1.+10.**((my_elo-1500.)/200.))
				k = 10.
				my_elo = my_elo +k*nbchance
			else:
				nbchance = 1./(1.+10.**((1500.-my_elo)/200.))
				k = 10.
				my_elo = my_elo-k*nbchance
		pitcher_elos.append(my_elo)
		for iiii in range(1,13):
			count_elo = thispitchelos[iiii]+(my_elo-thispitchelos[0])/12.
			for ii in i[1:]:
				thepitch = allgames[ii[0]][ii[1]]
				if thepitch[2]==[(iiii-1)%4,(iiii-1)/4]:
					if thepitch[3]==pitchtype:
						nbchance = 1./(1.+10.**((count_elo-1500.)/200.))
						k = 10.
						count_elo = count_elo +k*nbchance
					else:
						nbchance = 1./(1.+10.**((1500.-count_elo)/200.))
						k = 10.
						count_elo = count_elo-k*nbchance
			pitcher_elos.append(count_elo)
		pitcher_array.append([i[0],pitcher_elos])
	batter_array = []
	for i in batters:
		batter_elos = []
		my_elo = 3000.-thispitchelos[0]
		for ii in i[1:]:
			thepitch = allgames[ii[0]][ii[1]]
			if thepitch[3]!=pitchtype:
				nbchance = 1./(1.+10.**((my_elo-1500.)/200.))
				k = 10.
				my_elo = my_elo +k*nbchance
			else:
				nbchance = 1./(1.+10.**((1500.-my_elo)/200.))
				k = 10.
				my_elo = my_elo-k*nbchance
		batter_elos.append(my_elo)
		for iiii in range(1,13):
			count_elo = 3000.-thispitchelos[iiii]+(my_elo-(3000.-thispitchelos[0]))/12.
			for ii in i[1:]:
				thepitch = allgames[ii[0]][ii[1]]
				if thepitch[2]==[(iiii-1)%4,(iiii-1)/4]:
					if thepitch[3]!=pitchtype:
						nbchance = 1./(1.+10.**((count_elo-1500.)/200.))
						k = 10.
						count_elo = count_elo +k*nbchance
					else:
						nbchance = 1./(1.+10.**((1500.-count_elo)/200.))
						k = 10.
						count_elo = count_elo-k*nbchance
			batter_elos.append(count_elo)
		batter_array.append([i[0],batter_elos])

	for i in allgames:
		for ii in i:
			for iiidx,iii in enumerate(pitchers):
				if ii[0]==iii[0]:
					pid = iiidx
					break
			for iiidx,iii in enumerate(batters):
				if ii[1]==iii[0]:
					bid = iiidx
					break
			countthing = ii[2][0]+ii[2][1]*4+1
			pelo = pitcher_array[pid][1][countthing]
			belo = batter_array[bid][1][countthing]
			if ii[3]==pitchtype:
				nbchance = 1./(1.+10**((pelo-belo)/400.))
				k = 5.
				pelo = pelo+k*nbchance
				belo = belo-k*nbchance
			else:
				nbchance = 1./(1.+10**((belo-pelo)/400.))
				k = 5.
				pelo = pelo-k*nbchance
				belo = belo+k*nbchance
			pitcher_array[pid][1][countthing] = pelo
			batter_array[bid][1][countthing] = belo

	return pitcher_array, batter_array, thispitchelos


pitchers = []
for idx,i in enumerate(allgames):
	for iidx,ii in enumerate(i):
		yesin = False
		for iiidx,iii in enumerate(pitchers):
			if iii[0]==ii[0]:
				yesin = True
				pid = iiidx
		if not yesin:
			pitchers.append([ii[0],[idx,iidx]])
		else:
			pitchers[pid].append([idx,iidx])

batters = []
for idx,i in enumerate(allgames):
	for iidx,ii in enumerate(i):
		yesin = False
		for iiidx,iii in enumerate(batters):
			if iii[0]==ii[1]:
				yesin = True
				pid = iiidx
		if not yesin:
			batters.append([ii[1],[idx,iidx]])
		else:
			batters[pid].append([idx,iidx])

allptypes = ['B','S','C','F','X']
alleloarrays = []
alleloarrays.append(getallelos(allgames,'B',pitchers,batters))
alleloarrays.append(getallelos(allgames,'S',pitchers,batters))
alleloarrays.append(getallelos(allgames,'C',pitchers,batters))
alleloarrays.append(getallelos(allgames,'F',pitchers,batters))
alleloarrays.append(getallelos(allgames,'X',pitchers,batters))
def createcsv(iii,ptype,porb):
	tocsv = []
	if porb=='P':
		for i in alleloarrays[iii][0]:
			toarr = [i[0]]
			for ii in i[1]:
				toarr.append(ii)
			tocsv.append(toarr)
		writecsv(tocsv,'2016/'+ptype+'pitcher.csv')
	else:
		for i in alleloarrays[iii][1]:
			toarr = [i[0]]
			for ii in i[1]:
				toarr.append(ii)
			tocsv.append(toarr)
		writecsv(tocsv,'2016/'+ptype+'batter.csv')

for i in range(0,5):
	createcsv(i,allptypes[i],'P')
	createcsv(i,allptypes[i],'B')
writecsv(pitchers,'2016/pitchers.csv')
writecsv(batters,'2016/batters.csv')
tocsv = []
for i in allgames:
	for ii in i:
		tocsv.append(ii)
writecsv(tocsv,'2016/allgames.csv')
print soto
totalwalks = 0
totalk = 0
totalab = 0
acttotpa=0
acttotw = 0
acttotk = 0
for idx,pitcher in enumerate(pitchers):
	walkpct = 0
	kpct = 0
	pitcherpa = 0
	for i in allpas1:
		if i[0]==pitcher[0]:
			for iidx, ii in enumerate(batters):
				if ii[0]==i[1]:
					bidx=iidx
					break
			for irun in range(0,20):
				
				count = [0,0]
				pitchres = ''
				while pitchres != 'X':
					randx = random.random()
					countthing = count[0]+count[1]*4+1
					pitchpcts = topct(alleloarrays,idx,bidx,countthing)
					sumpct =0
					for ipct in pitchpcts:
						sumpct+=ipct
					for ipct in range(0,len(pitchpcts)):
						pitchpcts[ipct]=pitchpcts[ipct]/sumpct

					if randx < pitchpcts[0]:
						pitchres = 'B'
						count[0]+=1
						if count[0]==4:
							pitchres='X'
							abres = 'BB'
					elif randx < pitchpcts[0]+pitchpcts[1]:
						pitchres = 'S'
						count[1]+=1
						if count[1]==3:
							pitchres='X'
							abres = 'K'
					elif randx < pitchpcts[0]+pitchpcts[1]+pitchpcts[2]:
						pitchres = 'C'
						count[1]+=1
						if count[1]==3:
							pitchres='X'
							abres = 'K'
					elif randx < pitchpcts[0]+pitchpcts[1]+pitchpcts[2]+pitchpcts[3]:
						pitchres = 'F'
						count[1]+=1
						if count[1]==3:
							count[1]=2
					elif randx < pitchpcts[0]+pitchpcts[1]+pitchpcts[2]+pitchpcts[3]+pitchpcts[4]:
						pitchres = 'X'
						abres = 'P'
				if abres == 'BB':
					walkpct+=1
					totalwalks +=1
				if abres == 'K':
					kpct +=1
					totalk += 1
				pitcherpa+=1
				totalab +=1
	actpas = 0
	actwp = 0
	actkp = 0
	for i in allpas0:
		if i[0]==pitcher[0]:
			if i[1][0]=='W':
				actwp+=1
			elif i[1][0]=='K':
				actkp+=1
			actpas+=1
	actpas1 = 0
	actwp1 = 0
	actkp1 = 0
	for i in allpas1:
		if i[0]==pitcher[0]:
			if i[2][0]=='W':
				actwp1+=1
			elif i[2][0]=='K':
				actkp1+=1
			actpas1+=1
	acttotw+=actwp
	acttotk+=actkp
	acttotpa+=actpas
	if actpas > 100:
		print pitcher[0], walkpct*1./pitcherpa, kpct*1./pitcherpa, actwp*1./actpas, actkp*1./actpas, actwp1*1./actpas1, actkp1*1./actpas1#, totalwalks*1./totalab, totalk*1./totalab, acttotw*1./acttotpa, acttotk*1./acttotpa
