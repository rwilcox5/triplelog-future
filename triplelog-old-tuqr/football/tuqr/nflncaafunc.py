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
def calcmyncaaqbrating(x,cx,yx,tx,ix):
	if x[1]>0:
		cppoints = cx(x[0]*1./x[1]*100)
		ypapoints = yx(x[2]*1./x[1])
		tdpoints = tx(x[3]*1./x[1]*100)
		intpoints = ix(x[4]*1./x[1]*100)
	else:
		cppoints = 0
		ypapoints = 0
		tdpoints = 0
		intpoints = 0
	return cppoints, ypapoints, tdpoints, intpoints, cppoints+ypapoints+tdpoints+intpoints
def calcmynflqbrating(x,cx,yx,tx,ix,cmin,cmax,ymin,ymax,tmin,tmax,imin,imax):
	if x[1]>0:
		cp = x[0]*1./x[1]*100
		ypa = x[2]*1./x[1]
		tdpa = x[3]*1./x[1]*100
		intpa = x[4]*1./x[1]*100
		if cp > cmin:
			if cp < cmax:
				cppoints = cx(cp)
			else:
				cppoints = cx(cmax)
		else:
			cppoints = cx(cmin)
		if ypa > ymin:
			if ypa < ymax:
				ypapoints = yx(ypa)
			else:
				ypapoints = yx(ymax)
		else:
			ypapoints = yx(ymin)
		if tdpa > tmin:
			if tdpa < tmax:
				tdpoints = tx(tdpa)
			else:
				tdpoints = tx(tmax)
		else:
			tdpoints = tx(tmin)
		if intpa > imin:
			if intpa < imax:
				intpoints = ix(intpa)
			else:
				intpoints = ix(imax)
		else:
			intpoints = ix(imin)
	else:
		cppoints = cx(cmin)
		ypapoints = yx(ymin)
		tdpoints = tx(tmin)
		intpoints = ix(imin)
	return cppoints, ypapoints, tdpoints, intpoints, cppoints+ypapoints+tdpoints+intpoints
	
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
sliderarr = []
for i in range(0,10001):
    sliderarr.append(round(i*1./100,2))
@interact
def _(Comps=input_box('sqrt(x)',type=str, label='Function for Completions'),Yards=input_box('sqrt(x)*10',type=str, label='Function for Yards'),tds=input_box('sqrt(x)',type=str, label='Function for Touchdowns'),ints=input_box('-sqrt(x)',type=str, label='Function for Interceptions'),CompCap=range_slider(sliderarr),YardsCap=range_slider(sliderarr),TDCap=range_slider(sliderarr),INTCap=range_slider(sliderarr),minatt=slider(0,250,1,default=50)):
	xc1 = []
	xc2 = []
	xc3 = []
	xc4 = []
	yc = []
	rc = []
	cmin = CompCap[0]
	cmax = CompCap[1]
	ymin = YardsCap[0]
	ymax = YardsCap[1]
	tmin = TDCap[0]
	tmax = TDCap[1]
	imin = INTCap[0]
	imax = INTCap[1]
	cx = lambda x: eval(Comps)
	yx = lambda x: eval(Yards)
	tx = lambda x: eval(tds)
	ix = lambda x: eval(ints)
	for i in range(0,len(sx)):
		if sx[i][1]>=minatt:
			xc1.append(calcnflqbrating(sx[i])[4])
			xc2.append(calcncaaqbrating(sx[i])[4])
			xc3.append(calcmynflqbrating(sx[i],cx,yx,tx,ix,cmin,cmax,ymin,ymax,tmin,tmax,imin,imax)[4])
			xc4.append(calcmyncaaqbrating(sx[i],cx,yx,tx,ix)[4])
			if sx[i][9]>0:
				yc.append(sx[i][6]*1./sx[i][9])
			else:
				yc.append(0)
			rc.append(sx[i][8])
	allplayers = []
	for i in range(0,len(xc1)):
		allplayers.append([rc[i],round(xc1[i],2),round(xc2[i],2),round(xc3[i],2),round(xc4[i],2)])
	sortteams = sorted(allplayers, key=lambda allplayers_entry: allplayers_entry[1],reverse=True)
	corrtable = [['Correlations: ',round(numpy.corrcoef(xc1,yc)[0,1],3),round(numpy.corrcoef(xc2,yc)[0,1],3),round(numpy.corrcoef(xc3,yc)[0,1],3),round(numpy.corrcoef(xc4,yc)[0,1],3)]]
	for i in range(0,len(sortteams)):
		corrtable.append(sortteams[i])
	print table(corrtable[0:10],header_row=['Player','NFL','NCAA','MyNFL','MyNCAA'])

#print x[0]
#print calcqbrating(x[0])
