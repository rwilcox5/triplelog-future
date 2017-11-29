import sqlite3
from getlahman import connection
@interact
def _(age=range_slider(srange(16,50,1),default=(20,25))):
    limit = 25
    result = connection.execute("select first, last, year, yob, ab, runs, hits, hr, rbi, sb, bb, so, hbp, sf, sh  from batters where year-yob>="+str(age[0])+" and year-yob<="+str(age[1])+"  order by hr DESC limit "+str(limit))
    theresults = result.fetchall()
    myresults = []
    header = ['First','Last','Year','Age','PA','R','H','HR','RBI','SB','BB','K']
    for idx, i in enumerate(theresults):
        aresult = [str(i[0]),str(i[1]),i[2],i[2]-i[3],i[4]+i[10]+i[11]+i[12]+i[13],i[5],i[6],i[7],i[8],i[9],i[10],i[11]]
        myresults.append(aresult)
    rows = myresults
    print table(rows,header_row=header)