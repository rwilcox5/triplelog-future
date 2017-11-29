import sqlite3
import csv
import time
import numpy
from sage.plot.scatter_plot import ScatterPlot
import urllib
urllib.urlretrieve("http://triplelog.com/triplelog/football/tuqr/nflqbgamelog.db", "nflqbgamelog.db")
#print time.time()
connection = sqlite3.connect("nflqbgamelog.db")
result = connection.execute("select comp,attempts,yards,tds,interceptions,qbrating, scored, pid,name from games")
	
x =result.fetchall()
px = []
sx = []
for i in range(0,len(x)):
	if x[i][7] in px:
		dont = 0
	else:
		px.append(x[i][7])
		sx.append([0,0,0,0,0,0,0,x[i][7],x[i][8],0])
for i in range(0,len(px)):
	for ii in range(0,len(x)):
		if x[ii][7]==px[i]:
			if ii%2 ==1:
				for iii in range(0,len(sx[i])-4):
					sx[i][iii]=sx[i][iii]+x[ii][iii]
			if ii%2 ==0:
				sx[i][6]=sx[i][6]+x[ii][6]
				sx[i][9]=sx[i][9]+1
@interact
def _(minatt=slider(0,250,1,default=50),mystat=['CP','YPA','TDPA','INTPA']):
	if mystat == 'CP':
		compperc = []
		for i in range(0,len(sx)):
			if sx[i][1]>=minatt:
				compperc.append([sx[i][0]*1./sx[i][1], sx[i][1]])
		sortteams = sorted(compperc, key=lambda compperc_entry: compperc_entry[0],reverse=True)
		print table(sortteams[0:50],header_row=['CP','Att'])
	if mystat == 'YPA':
		compperc = []
		for i in range(0,len(sx)):
			if sx[i][1]>=minatt:
				compperc.append([sx[i][2]*1./sx[i][1], sx[i][1]])
		sortteams = sorted(compperc, key=lambda compperc_entry: compperc_entry[0],reverse=True)
		print table(sortteams[0:50],header_row=['YPA','Att'])
	if mystat == 'TDPA':
		compperc = []
		for i in range(0,len(sx)):
			if sx[i][1]>=minatt:
				compperc.append([sx[i][3]*1./sx[i][1], sx[i][1]])
		sortteams = sorted(compperc, key=lambda compperc_entry: compperc_entry[0],reverse=True)
		print table(sortteams[0:50],header_row=['TDPA','Att'])
	if mystat == 'INTPA':
		compperc = []
		for i in range(0,len(sx)):
			if sx[i][1]>=minatt:
				compperc.append([sx[i][4]*1./sx[i][1], sx[i][1]])
		sortteams = sorted(compperc, key=lambda compperc_entry: compperc_entry[0],reverse=True)
		print table(sortteams[0:50],header_row=['INTPA','Att'])
#print x[0]
#print calcqbrating(x[0])
