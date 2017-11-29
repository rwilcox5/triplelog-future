import sqlite3
import csv
import time
import numpy
from triplelog import tohtmltable
from getlahman import sqldb as connection
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def sagetohtmltable(header,rows):
    numbercols = []
    for idx,i in enumerate(rows[0]):
        if is_number(i):
            numbercols.append(idx)
    mystr = '<table class="dyna" id="my-table"><thead><tr>'
    for idx, i in enumerate(header):
        if idx > len(header)-5:
            mystr=mystr+'<th>'+str(i)+'</th>'
        else:
            mystr=mystr+'<th>'+str(i)+'</th>'
    mystr=mystr+'</tr></thead><tbody>'
    for idx, i in enumerate(rows):
        mystr=mystr+'<tr>'
        for iidx, ii in enumerate(i):
            if iidx in numbercols:
                mystr=mystr+'<td align="right">'+str(ii)+'</td>'
            else:
                mystr=mystr+'<td>'+str(ii)+'</td>'
        mystr=mystr+'</tr>'
    if len(numbercols)==0:
        mystr=mystr+'</tbody></table>'
    else:
        mystr=mystr+'</tbody></table>|col='
        for idx, i in enumerate(numbercols):
            if is_number(str(header[i])[0]):
                mystr = mystr+str(header[i])
            else:
                mystr = mystr+header[i].lower()
            if idx < len(numbercols)-1:
                mystr=mystr+'|'
    return mystr
@interact
def _(numbpa=range_slider(srange(0,910,10),default=(600,900)),age=range_slider(srange(16,50,1),default=(20,25)),hr=range_slider(srange(0,75,1),default=(20,75)),sb=range_slider(srange(0,200,1),default=(20,200))):
    limit = 1000
    result = connection.execute("select * from batters where year-yob>="+str(age[0])+" and year-yob<="+str(age[1])+" and ab+bb+hbp+sh+sf>="+str(numbpa[0])+" and ab+bb+hbp+sh+sf<="+str(numbpa[1])+" and hr>="+str(hr[0])+" and hr<="+str(hr[1])+" and sb>="+str(sb[0])+" and sb<="+str(sb[1])+" order by year DESC limit "+str(limit))
    theresults = result.fetchall()
    myresults = []
    header = ['First','Last','Year','Team','Age','PA','AB','R','H','2B','3B','HR','RBI','SB','BB','K','AVG','OBP','SLG','OPS']
    for idx, i in enumerate(theresults):
        aresult = [str(i[23]),str(i[24]),i[1],str(i[3]),i[1]-i[22],i[6]+i[15]+i[18]+i[19]+i[20],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[15],i[16],round(i[8]*1./i[6],3),round((i[15]+i[8])*1./(i[6]+i[15]+i[18]+i[19]+i[20]),3),round((i[8]+i[9]+2*i[10]+3*i[11])*1./i[6],3),round((i[15]+i[8])*1./(i[6]+i[15]+i[18]+i[19]+i[20])+(i[8]+i[9]+2*i[10]+3*i[11])*1./i[6],3)]
        myresults.append(aresult)
    rows = myresults
    print html(tohtmltable(header,myresults,[[16,17,18,19],[3,3,3,3]]))