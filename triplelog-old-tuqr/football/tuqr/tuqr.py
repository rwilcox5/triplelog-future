import sqlite3
from triplelog import maketable
import urllib
urllib.urlretrieve("http://triplelog.com/triplelog/football/tuqr/nflqbgamelog.db", "nflqbgamelog.db")
#print time.time()
connection = sqlite3.connect("nflqbgamelog.db")
def calcnflqbrating(x):
	if x[1]>0:
		cp = x[0]*1./x[1]
		ypa = x[2]*1./x[1]
		tdpa = x[3]*1./x[1]
		intpa = x[4]*1./x[1]
		if cp > .30:
			if cp < .775:
				cppoints = (cp*100-30)*.05
			else:
				cppoints = 2.375
		else:
			cppoints = 0
		if ypa > 3:
			if ypa < 12.5:
				ypapoints = (ypa-3)*.25
			else:
				ypapoints = 2.375
		else:
			ypapoints = 0 
		if tdpa > .11875:
			tdpoints = 2.375
		else:
			tdpoints = tdpa*100*.2
		if intpa > .095:
			intpoints = 0
		else:
			intpoints = 2.375-.25*100*intpa
	else:
		cppoints = 0
		ypapoints = 0
		tdpoints = 0
		intpoints = 0
	return cppoints, ypapoints, tdpoints, intpoints, (cppoints+ ypapoints+ tdpoints+ intpoints)*100./6
def calcncaaqbrating(x):
	if x[1]>0:
		cppoints = x[0]*1./x[1]*100
		ypapoints = x[2]*1./x[1]
		tdpoints = x[3]*1./x[1]*100
		intpoints = x[4]*1./x[1]*100
	else:
		cppoints = 0
		ypapoints = 0
		tdpoints = 0
		intpoints = 0
	return cppoints, ypapoints, tdpoints, intpoints, cppoints+ 8.4*ypapoints+ 3.3*tdpoints-2*intpoints
def calctuqr(x,cw,yw,tw,iw):
	if x[1]>0:
		cppoints = (x[0]*1./x[1]*100-60)*x[1]
		ypapoints = (x[2]*1./x[1]-7)*x[1]
		tdpoints = (x[3]*1./x[1]*100-4)*x[1]
		intpoints = (x[4]*1./x[1]*100-2)*x[1]
	else:
		cppoints = 0
		ypapoints = 0
		tdpoints = 0
		intpoints = 0
	return cppoints, ypapoints, tdpoints, intpoints, cw*cppoints+ yw*8.4*ypapoints+ tw*3.3*tdpoints-iw*2*intpoints
def calcmynflqbrating(x,cw,yw,tw,iw):
	if x[1]>0:
		cp = x[0]*1./x[1]
		ypa = x[2]*1./x[1]
		tdpa = x[3]*1./x[1]
		intpa = x[4]*1./x[1]
		if cp > .30:
			if cp < .775:
				cppoints = (cp*100-30)*.05
			else:
				cppoints = 2.375
		else:
			cppoints = 0
		if ypa > 3:
			if ypa < 12.5:
				ypapoints = (ypa-3)*.25
			else:
				ypapoints = 2.375
		else:
			ypapoints = 0 
		if tdpa > .11875:
			tdpoints = 2.375
		else:
			tdpoints = tdpa*100*.2
		if intpa > .095:
			intpoints = 0
		else:
			intpoints = 2.375-.25*100*intpa
	else:
		cppoints = 0
		ypapoints = 0
		tdpoints = 0
		intpoints = 0
	return cppoints, ypapoints, tdpoints, intpoints, (cw*cppoints+ yw*ypapoints+ tw*tdpoints+ iw*intpoints)*100./6
result = connection.execute("select comp,attempts,yards,tds,interceptions,qbrating, scored, pid,name from games")
x =result.fetchall()
players = []
games = x
seasons = []
careers = []
careerspg = []
playerseasons = []
for i in range(0,len(x)):
	if x[i][7] in players:
		dont = 0
	else:
		players.append(x[i][7])
		careers.append([0,0,0,0,0,0,0,x[i][7],x[i][8],0])
		careerspg.append([0,0,0,0,0,0,0,x[i][7],x[i][8],0])
for i in range(0,len(players)):
	for ii in range(0,len(x)):
		if x[ii][7]==players[i]:
			for iii in range(0,len(careers[i])-4):
				careers[i][iii]=careers[i][iii]+x[ii][iii]
			careers[i][9]=careers[i][9]+1
for i in range(0,len(players)):
	if careers[i][9]>0:
		for ii in range(0,len(careers[i])-4):
			careerspg[i][ii]=careers[i][ii]/careers[i][9]
for i in range(0,len(x)):
	if str(x[i][7])+str(2014) in playerseasons:
		dont = 0
	else:
		playerseasons.append(str(x[i][7])+str(2014))
		seasons.append([0,0,0,0,0,0,0,x[i][7],x[i][8],0,2014])
for i in range(0,len(seasons)):
	for ii in range(0,len(x)):
		if str(x[ii][7])+str(2014)==playerseasons[i]:
			for iii in range(0,len(seasons[i])-5):
				seasons[i][iii]=seasons[i][iii]+x[ii][iii]
			seasons[i][9]=seasons[i][9]+1
sliderarr = []
for i in range(101):
    sliderarr.append(round(i*1./100,2))
@interact
def _(Comps=slider(sliderarr,default=1),Yards=slider(sliderarr,default=1),TDs=slider(sliderarr,default=1),INTs=slider(sliderarr,default=1),minatt=slider(0,250,1,default=1,label="Min. Atts"),gacar=selector(['Game','Season','Career','PerGame'],label='',buttons=True)):
	ratings = [[],[],[]]
	cpgratings = [[],[],[]]
	names = []
	gratings = [[],[],[]]
	gnames = []
	gyear = []
	sratings = [[],[],[]]
	snames = []
	syear = []
	for i in range(0,len(careers)):
		if careers[i][1]>=minatt:
			ratings[0].append(calcnflqbrating(careers[i])[4])
			ratings[1].append(calcncaaqbrating(careers[i])[4])
			ratings[2].append(calctuqr(careers[i],Comps,Yards,TDs,INTs)[4])
			cpgratings[0].append(calcnflqbrating(careerspg[i])[4])
			cpgratings[1].append(calcncaaqbrating(careerspg[i])[4])
			cpgratings[2].append(calctuqr(careerspg[i],Comps,Yards,TDs,INTs)[4])
			names.append(careers[i][8])
	for i in range(0,len(games)):
		if games[i][1]>=minatt:
			gratings[0].append(calcnflqbrating(games[i])[4])
			gratings[1].append(calcncaaqbrating(games[i])[4])
			gratings[2].append(calctuqr(games[i],Comps,Yards,TDs,INTs)[4])
			gnames.append(games[i][8])
			gyear.append(2014)
	for i in range(0,len(seasons)):
		if seasons[i][1]>=minatt:
			sratings[0].append(calcnflqbrating(seasons[i])[4])
			sratings[1].append(calcncaaqbrating(seasons[i])[4])
			sratings[2].append(calctuqr(seasons[i],Comps,Yards,TDs,INTs)[4])
			snames.append(seasons[i][8])
			syear.append(seasons[i][10])
	allplayers = []
	if gacar == 'Game':
		for i in range(0,len(gratings[0])):
			allplayers.append([gnames[i],gyear[i],round(gratings[0][i],2),round(gratings[1][i],2),round(gratings[2][i]/100,2)])
		sortteams = sorted(allplayers, key=lambda allplayers_entry: allplayers_entry[4],reverse=True)
		header = ['Player','Year','NFL','NCAA','TUQR']
	elif gacar == 'Season':
		for i in range(0,len(sratings[0])):
			allplayers.append([snames[i],syear[i],round(sratings[0][i],2),round(sratings[1][i],2),round(sratings[2][i]/100,2)])
		sortteams = sorted(allplayers, key=lambda allplayers_entry: allplayers_entry[4],reverse=True)
		header = ['Player','Year','NFL','NCAA','TUQR']
	elif gacar == 'Career':
		for i in range(0,len(ratings[0])):
			allplayers.append([names[i],round(ratings[0][i],2),round(ratings[1][i],2),round(ratings[2][i]/100,2)])		
		sortteams = sorted(allplayers, key=lambda allplayers_entry: allplayers_entry[3],reverse=True)
		header = ['Player','NFL','NCAA','TUQR']
	else:
		for i in range(0,len(ratings[0])):
			allplayers.append([names[i],round(cpgratings[0][i],2),round(cpgratings[1][i],2),round(cpgratings[2][i]/100,2)])		
		sortteams = sorted(allplayers, key=lambda allplayers_entry: allplayers_entry[3],reverse=True)
		header = ['Player','NFL','NCAA','TUQR']
	print maketable(header,sortteams,'Python',10,[[],[]])
	

