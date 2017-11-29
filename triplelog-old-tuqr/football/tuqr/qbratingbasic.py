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
def calcmyncaaqbrating(x,cw,yw,tw,iw):
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
    
x =result.fetchall()
px = []
sx = []
for i in range(0,len(x)):
    if x[i][7] in px:
        dont = 0
    else:
        px.append(x[i][7])
        sx.append([0,0,0,0,0,0,0,x[i][7],x[i][8]])
for i in range(0,len(px)):
    for ii in range(0,len(x)):
        if x[ii][7]==px[i]:
            for iii in range(0,len(sx[i])-1):
                sx[i][iii]=sx[i][iii]+x[ii][iii]
sliderarr = []
for i in range(101):
    sliderarr.append(round(i*1./100,2))
@interact
def _(Comps=slider(sliderarr,default=1),Yards=slider(sliderarr,default=1),TDs=slider(sliderarr,default=1),INTs=slider(sliderarr,default=1),minatt=slider(0,250,1,default=50)):
    xc1 = []
    xc2 = []
    xc3 = []
    xc4 = []
    yc = []
    rc = []
    for i in range(0,len(sx)):
        if sx[i][1]>=minatt:
            xc1.append(calcnflqbrating(sx[i])[4])
            xc2.append(calcncaaqbrating(sx[i])[4])
            xc3.append(calcmynflqbrating(sx[i],cw,yw,tw,iw)[4])
            xc4.append(calcmyncaaqbrating(sx[i],cw,yw,tw,iw)[4])
            yc.append(sx[i][6])
            rc.append(sx[i][8])
    allplayers = []
    for i in range(0,len(xc1)):
		allplayers.append([rc[i],round(xc1[i],2),round(xc2[i],2),round(xc3[i],2),round(xc4[i],2)])
    sortteams = sorted(allplayers, key=lambda allplayers_entry: allplayers_entry[1],reverse=True)
    print table(sortteams[0:10])
    print 'Correlations: ',round(numpy.corrcoef(xc1,yc)[0,1],3),round(numpy.corrcoef(xc2,yc)[0,1],3),round(numpy.corrcoef(xc3,yc)[0,1],3),round(numpy.corrcoef(xc4,yc)[0,1],3)

#print x[0]
#print calcqbrating(x[0])
