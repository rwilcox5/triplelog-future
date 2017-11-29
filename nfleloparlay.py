import time
import random
import csv
import math
import threading
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
nteams = 130
this_week = 5

def writecsv(parr, filen):
        with open(filen, 'ab') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in range(0,len(parr)):
                        try:
                                spamwriter.writerow(parr[i])
                        except:
                                print parr[i], i


def readcsv(filen):
        allgamesa  =[]
        with open(filen, 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                        allgamesa.append(row)
        return allgamesa

allgames = readcsv('nfl16.csv')

print len(allgames)

teams = []
allelos = [1386.60661738187,1523.61839594805,1483.88120708739,1577.25173932155,1451.58424856129,1476.43131892176,1463.0081034697,1297.4840313748,1645.58794425166,1504.09669826344,1438.6571174855,1595.46410064528,1458.19106743891,1365.20428758862,1515.42579084463,1537.81266533677,1670.67562006733,1465.66647164366,1464.20068481427,1443.26379253801,1400.92674053396,1413.45250987923,1418.36940674607,1493.09912723611,1476.82828101692,1554.94879549516,1434.98431735436,1492.28569222856,1598.89740469865,1545.63720313099,1508.07362423011,1380.59003149679]

for i in range(0,256):
    allin = False
    for ii in range(0,len(teams)):
        if teams[ii][0]==allgames[i][0]:
            allin = True
    if not allin:
        all32 = []
        for ii in range(0,32):
            all32.append(0)
        teams.append([allgames[i][0],1500,allelos[len(teams)],all32])

fakegames = []
for i in range(0,256):
    ateam = allgames[i][0]
    hteam = allgames[i][1]
    for ii in range(0,len(teams)):
        if ateam==teams[ii][0]:
            ateamid= ii
        if hteam==teams[ii][0]:
            hteamid= ii  
    aeloact = teams[ateamid][2]
    heloact = teams[hteamid][2]
    aelo = teams[ateamid][1]
    helo = teams[hteamid][1]
    hteamwin = 1./(1.+10.**((aeloact-heloact)/400.))

    if random.random()<hteamwin:
        hwin = True
    else:
        hwin = False
    k = 25.
    kk = 1.
    if hwin:
        ateamprob = 1./(1.+10.**((helo-aelo)/400.))
        helo = helo+k*ateamprob
        aelo = aelo-k*ateamprob
        
        dAdHold = teams[ateamid][3][hteamid]
        dAdH= dAdHold+k*(1.+10.**((helo-aelo)/400.))**(-2.)*10.**((helo-aelo)/400.)*math.log(10,2.718)/400.*(1-dAdHold)
        dHdAold = teams[hteamid][3][ateamid]
        dHdA= dHdAold-k*(1.+10.**((helo-aelo)/400.))**(-2.)*10.**((helo-aelo)/400.)*math.log(10,2.718)/400.*(dHdAold-1)
        teams[ateamid][3][hteamid]=dAdH
        teams[hteamid][3][ateamid]=dHdA
        for ii in range(0,32):
            if ii!=ateamid and ii!=hteamid:
                dHdii=teams[hteamid][3][ii]+kk*(dHdA-dHdAold)*teams[ateamid][3][ii]
                dAdii=teams[ateamid][3][ii]+kk*(dAdH-dAdHold)*teams[hteamid][3][ii]
                teams[hteamid][3][ii]=dHdii
                teams[ateamid][3][ii]=dAdii
        for ii in range(0,32):
            if ii!=ateamid and ii!=hteamid:
                diidH=teams[ii][3][hteamid]+kk*(dAdH-dAdHold)*teams[ii][3][ateamid]
                diidA=teams[ii][3][ateamid]+kk*(dHdA-dHdAold)*teams[ii][3][hteamid]
                teams[ii][3][hteamid]=diidH
                teams[ii][3][ateamid]=diidA
                
        
    else:
        hteamprob = 1./(1.+10.**((aelo-helo)/400.))
        helo = helo-k*hteamprob
        aelo = aelo+k*hteamprob

        dAdHold = teams[ateamid][3][hteamid]
        dAdH= dAdHold-k*(1.+10.**((aelo-helo)/400.))**(-2.)*10.**((aelo-helo)/400.)*math.log(10,2.718)/400.*(dAdHold-1)
        dHdAold = teams[hteamid][3][ateamid]
        dHdA= dHdAold+k*(1.+10.**((aelo-helo)/400.))**(-2.)*10.**((aelo-helo)/400.)*math.log(10,2.718)/400.*(1-dHdAold)
        teams[ateamid][3][hteamid]=dAdH
        teams[hteamid][3][ateamid]=dHdA
        for ii in range(0,32):
            if ii!=ateamid and ii!=hteamid:
                dHdii=teams[hteamid][3][ii]+kk*(dHdA-dHdAold)*teams[ateamid][3][ii]
                dAdii=teams[ateamid][3][ii]+kk*(dAdH-dAdHold)*teams[hteamid][3][ii]
                teams[hteamid][3][ii]=dHdii
                teams[ateamid][3][ii]=dAdii
        for ii in range(0,32):
            if ii!=ateamid and ii!=hteamid:
                diidH=teams[ii][3][hteamid]+kk*(dAdH-dAdHold)*teams[ii][3][ateamid]
                diidA=teams[ii][3][ateamid]+kk*(dHdA-dHdAold)*teams[ii][3][hteamid]
                teams[ii][3][hteamid]=diidH
                teams[ii][3][ateamid]=diidA
                
        
    teams[ateamid][1] = aelo
    teams[hteamid][1] = helo


    

team1 = 'Denver Broncos'
team2 = 'Oakland Raiders'
team3 = 'Dallas Cowboys'
team4 = 'New York Giants'
for idx,i in enumerate(teams):
    if i[0]==team1:
        team1id = idx
    if i[0]==team2:
        team2id = idx
    if i[0]==team3:
        team3id = idx
    if i[0]==team4:
        team4id = idx

my_games = []
for iiiii in range(0,256):
    if allgames[iiiii][0]==team1 or allgames[iiiii][0]==team2 or allgames[iiiii][0]==team3 or allgames[iiiii][0]==team4 or allgames[iiiii][1]==team1 or allgames[iiiii][1]==team2 or allgames[iiiii][1]==team3 or allgames[iiiii][1]==team4:
        if allgames[iiiii][0]==team1:
            ateam = 't1'
        elif allgames[iiiii][0]==team2:
            ateam = 't2'
        elif allgames[iiiii][0]==team3:
            ateam = 't3'
        elif allgames[iiiii][0]==team4:
            ateam = 't4'
        else:
            for i in teams:
                if i[0]==allgames[iiiii][0]:
                    ateam = i[1] 
        if allgames[iiiii][1]==team1:
            hteam = 't1'
        elif allgames[iiiii][1]==team2:
            hteam = 't2'
        elif allgames[iiiii][1]==team3:
            hteam = 't3'
        elif allgames[iiiii][1]==team4:
            hteam = 't4'
        else:
            for i in teams:
                if i[0]==allgames[iiiii][1]:
                    hteam = i[1] 
        if allgames[iiiii][3]>allgames[iiiii][2]:
            my_games.append([ateam,hteam,'h'])
        else:
            my_games.append([ateam,hteam,'a'])
print len(my_games)
def probthis(game,t1elo,t2elo,t3elo,t4elo):
    ateam = game[0]
    hteam = game[1]
    if ateam=='t1':
        aelo = t1elo
    elif ateam=='t2':
        aelo = t2elo
    elif ateam=='t3':
        aelo = t3elo
    elif ateam=='t4':
        aelo = t4elo
    else:
        aelo = ateam
    if hteam=='t1':
        helo = t1elo
    elif hteam=='t2':
        helo = t2elo
    elif hteam=='t3':
        helo = t3elo
    elif hteam=='t4':
        helo = t4elo
    else:
        helo = hteam
    if game[2]=='h':
        return 1./(1.+10.**((aelo-helo)/400.))
    else:
        return 1./(1.+10.**((helo-aelo)/400.))

sumdiff = 0.
ngames = 0.
x = .05
for i in range(0,32):
    for ii in range(i+1,32):
        for iii in range(0,32):
            if iii!=i and iii!=ii:
                for iv in range(iii+1,32):
                    if iv!=i and iv!=ii:
                        if teams[i][3][iii]>teams[i][3][iv]+x and teams[ii][3][iv]>teams[ii][3][iii]+x:
                            parlay_odds1 = 1./(1.+10.**((teams[i][1]-teams[ii][1])/400.))*1./(1.+10.**((teams[iii][1]-teams[iv][1])/400.))
                            parlay_odds2 = 1./(1.+10.**((-teams[i][1]+teams[ii][1])/400.))*1./(1.+10.**((-teams[iii][1]+teams[iv][1])/400.))
                            actodds1 = 1./(1.+10.**((teams[i][2]-teams[ii][2])/400.))*1./(1.+10.**((teams[iii][2]-teams[iv][2])/400.))
                            actodds2 = 1./(1.+10.**((-teams[i][2]+teams[ii][2])/400.))*1./(1.+10.**((-teams[iii][2]+teams[iv][2])/400.))
                            sumdiff +=actodds1+actodds2-parlay_odds1-parlay_odds2
                            ngames += 1
                        if teams[i][3][iii]<teams[i][3][iv]-x and teams[ii][3][iv]<teams[ii][3][iii]-x:
                            parlay_odds1 = 1./(1.+10.**((teams[i][1]-teams[ii][1])/400.))*1./(1.+10.**((teams[iv][1]-teams[iii][1])/400.))
                            parlay_odds2 = 1./(1.+10.**((-teams[i][1]+teams[ii][1])/400.))*1./(1.+10.**((-teams[iv][1]+teams[iii][1])/400.))
                            actodds1 = 1./(1.+10.**((teams[i][2]-teams[ii][2])/400.))*1./(1.+10.**((teams[iv][2]-teams[iii][2])/400.))
                            actodds2 = 1./(1.+10.**((-teams[i][2]+teams[ii][2])/400.))*1./(1.+10.**((-teams[iv][2]+teams[iii][2])/400.))
                            sumdiff +=actodds1+actodds2-parlay_odds1-parlay_odds2
                            ngames += 1


print sumdiff, ngames, sumdiff/ngames
print soto
prob1b3 = 0.
totalprob = 0.
prob2b4 = 0.
prob12b34 = 0.
for i in range(0,30):
    print i
    team1elo = teams[team1id][1]+i*6.-90.
    for ii in range(0,30):
        team2elo = teams[team2id][1]+ii*6.-125.
        for iii in range(0,30):
            team3elo = teams[team3id][1]+iii*6.-125.
            for iiii in range(0,30):
                team4elo = teams[team4id][1]+iiii*6.-125.
                probhere = 1.
                for iiiii in my_games:
                    probhere = probhere*probthis(iiiii,team1elo,team2elo,team3elo,team4elo)
                prob1b3 += 1./(1.+10.**((team3elo-team1elo)/400.))*probhere
                prob2b4 += 1./(1.+10.**((team4elo-team2elo)/400.))*probhere
                prob12b34 += 1./(1.+10.**((team3elo-team1elo)/400.))*1./(1.+10.**((team4elo-team2elo)/400.))*probhere
                totalprob+=probhere
print prob1b3/totalprob,prob2b4/totalprob,prob12b34/totalprob,prob1b3/totalprob*prob2b4/totalprob




    
