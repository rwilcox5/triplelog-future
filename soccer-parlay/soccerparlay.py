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

allconfed = readcsv('elo_blatter.csv')
allteams = []
for i in allconfed[1:]:
    allteams.append([i[0],i[3]])
allteams.append(['USA','CONCACAF'])

allrawpred = readcsv('wwc-matches-start.csv')
allrawresults = readcsv('wwc-matches-end.csv')
allpred = []
confedlist = []
confedteams = []
for idx,i in enumerate(allrawpred[1:]):
    found1 = False
    found2 = False
    for ii in allteams:
        if ii[0]==i[2]:
            confed1 = ii[1]
            found1 = True
        if ii[0]==i[3]:
            confed2 = ii[1]
            found2 = True
    if not found1:
        print i[2]
    if not found2:
        print i[3]
    allpred.append([i[2],i[3],i[4],i[5],confed1,confed2,allrawresults[idx+1][4],allrawresults[idx+1][5],i[6],allrawresults[idx+1][6]])
    if confed1 not in confedlist:
        confedlist.append(confed1)
        confedteams.append([i[2]])
    else:
        for iidx,ii in enumerate(confedlist):
            if ii==confed1:
                if i[2] not in confedteams[iidx]:
                    confedteams[iidx].append(i[2])
    if confed2 not in confedlist:
        confedlist.append(confed2)
        confedteams.append([i[3]])
    else:
        for iidx,ii in enumerate(confedlist):
            if ii==confed2:
                if i[3] not in confedteams[iidx]:
                    confedteams[iidx].append(i[3])
for i in range(0,len(confedteams)):
    print confedlist[i],confedteams[i]

for iiiiiiii in range(0,20):
    broll = 0.
    ngames = 0.
    for idx in range(0,0):
        x = random.random()
        if x<float(allpred[idx][2]):
            allpred[idx][6]=1
            allpred[idx][7]=0
        elif x<float(allpred[idx][2])+float(allpred[idx][3]):
            allpred[idx][7]=1
            allpred[idx][6]=0
        else:
            allpred[idx][7]=0
            allpred[idx][6]=0


    for i in allpred:
        for ii in allpred:
            for iii in allpred:
                allteams = [i[0],i[1],ii[0],ii[1],iii[0],iii[1]]
                allconfeds = [i[4],i[5],ii[4],ii[5],iii[4],iii[5]]
                diffteams = True
                for iiii in range(0,len(allteams)):
                    for iv in allteams[iiii+1:]:
                        if allteams[iiii]==iv:
                            diffteams = False
                diffconfeds = True
                if i[4]==i[5]:
                    diffconfeds = False
                if ii[4]==ii[5]:
                    diffconfeds = False
                if iii[4]==iii[5]:
                    diffconfeds = False

                nconfeds1 = 1
                nconfeds2 = 1
                
                confed1 = allconfeds[0]
                confed2 = allconfeds[1]
                for iiii in allconfeds[2:]:
                    if iiii==confed1:
                        nconfeds1+=1
                    if iiii==confed2:
                        nconfeds2+=1

                if diffteams and diffconfeds and max(nconfeds1,nconfeds2)>=2.5:
                    
                    win1 = float(i[2])*26./29
                    awin1 = float(i[6])
                    if ii[4]==confed1:
                        win1*=float(ii[2])*26./29
                        awin1*=float(ii[6])
                    elif ii[5]==confed1:
                        win1*=float(ii[3])*26./29
                        awin1*=float(ii[7])
                    else:
                        win1*=0
                        awin1*=0
                    if iii[4]==confed1:
                        win1*=float(iii[2])*26./29
                        awin1*=float(iii[6])
                    elif iii[5]==confed1:
                        win1*=float(iii[3])*26./29
                        awin1*=float(iii[7])
                    else:
                        win1*=0
                        awin1*=0

                    win2 = float(i[3])*26./29
                    awin2 = float(i[7])
                    if ii[4]==confed2:
                        win2*=float(ii[2])*26./29
                        awin2*=float(ii[6])
                    elif ii[5]==confed2:
                        win2*=float(ii[3])*26./29
                        awin2*=float(ii[7])
                    else:
                        win2*=0
                        awin2*=0
                    if iii[4]==confed2:
                        win2*=float(iii[2])*26./29
                        awin2*=float(iii[6])
                    elif iii[5]==confed2:
                        win2*=float(iii[3])*26./29
                        awin2*=float(iii[7])
                    else:
                        win2*=0
                        awin2*=0


                    broll -= win1
                    broll -= win2
                    broll += awin1
                    broll += awin2

                    ngames +=1

    print broll,ngames

print soto
broll = 0.
for i in allpred:
    for ii in allpred:
        if i[0] !=ii[0] and i[0] !=ii[1] and i[1]!=ii[0] and i[1]!=ii[1]:
            if i[4]==ii[4] and i[5]==ii[5] and i[4]!=i[5]:
                parlaywins = float(i[2])*float(ii[2])
                parlaylosses = float(i[3])*float(ii[3])
                if float(i[6])>.5 and float(ii[6])>.5:
                    broll +=1.
                elif float(i[7])>.5 and float(ii[7])>.5:
                    broll +=1.
                broll -= parlaywins
                broll -= parlaylosses
            if i[4]==ii[5] and i[5]==ii[4] and i[4]!=i[5]:
                parlaywins = float(i[2])*float(ii[3])
                parlaylosses = float(i[3])*float(ii[2])
                if float(i[6])>.5 and float(ii[7])>.5:
                    broll +=1.
                elif float(i[7])>.5 and float(ii[6])>.5:
                    broll +=1.
                broll -= parlaywins
                broll -= parlaylosses
                broll -= float(i[8])*float(ii[8])
                broll += float(i[9])*float(ii[9])
print broll

broll = 0.
ngames = 0.
for i in allpred:
    for ii in allpred:
        for iii in allpred:
            allteams = [i[0],i[1],ii[0],ii[1],iii[0],iii[1]]
            allconfeds = [i[4],i[5],ii[4],ii[5],iii[4],iii[5]]
            diffteams = True
            for iiii in range(0,len(allteams)):
                for iv in allteams[iiii+1:]:
                    if allteams[iiii]==iv:
                        diffteams = False
            diffconfeds = True
            if i[4]==i[5]:
                diffconfeds = False
            if ii[4]==ii[5]:
                diffconfeds = False
            if iii[4]==iii[5]:
                diffconfeds = False

            twoconfeds = True
            
            confed1 = allconfeds[0]
            confed2 = allconfeds[1]
            for iiii in allconfeds[2:]:
                if iiii!=confed1 and iiii!=confed2:
                    twoconfeds = False

            if diffteams and diffconfeds and twoconfeds:
                win1 = float(i[2])
                awin1 = float(i[6])
                if ii[4]==confed1:
                    win1*=float(ii[2])
                    awin1*=float(ii[6])
                else:
                    win1*=float(ii[3])
                    awin1*=float(ii[7])
                if iii[4]==confed1:
                    win1*=float(iii[2])
                    awin1*=float(iii[6])
                else:
                    win1*=float(iii[3])
                    awin1*=float(iii[7])

                win2 = float(i[3])
                awin2 = float(i[7])
                if ii[4]==confed2:
                    win2*=float(ii[2])
                    awin2*=float(ii[6])
                else:
                    win2*=float(ii[3])
                    awin2*=float(ii[7])
                if iii[4]==confed2:
                    win2*=float(iii[2])
                    awin2*=float(iii[6])
                else:
                    win2*=float(iii[3])
                    awin2*=float(iii[7])
                drawp = float(i[8])*float(ii[8])*float(iii[8])
                drawa = float(i[9])*float(ii[9])*float(iii[9])

                broll -= win1
                broll -= win2
                broll += awin1
                broll += awin2
                broll -= drawp
                broll += drawa
                ngames +=1

print broll,ngames

broll = 0.
ngames = 0.
for i in allpred:
    for ii in allpred:
        for iii in allpred:
            for iv in allpred:
                allteams = [i[0],i[1],ii[0],ii[1],iii[0],iii[1],iv[0],iv[1]]
                allconfeds = [i[4],i[5],ii[4],ii[5],iii[4],iii[5],iv[4],iv[5]]
                diffteams = True
                for iiii in range(0,len(allteams)):
                    for iiv in allteams[iiii+1:]:
                        if allteams[iiii]==iiv:
                            diffteams = False
                diffconfeds = True
                if i[4]==i[5]:
                    diffconfeds = False
                if ii[4]==ii[5]:
                    diffconfeds = False
                if iii[4]==iii[5]:
                    diffconfeds = False
                if iv[4]==iv[5]:
                    diffconfeds = False

                twoconfeds = True
                
                confed1 = allconfeds[0]
                confed2 = allconfeds[1]
                for iiii in allconfeds[2:]:
                    if iiii!=confed1 and iiii!=confed2:
                        twoconfeds = False

                if diffteams and diffconfeds and twoconfeds:
                    win1 = float(i[2])
                    awin1 = float(i[6])
                    if ii[4]==confed1:
                        win1*=float(ii[2])
                        awin1*=float(ii[6])
                    else:
                        win1*=float(ii[3])
                        awin1*=float(ii[7])
                    if iii[4]==confed1:
                        win1*=float(iii[2])
                        awin1*=float(iii[6])
                    else:
                        win1*=float(iii[3])
                        awin1*=float(iii[7])
                    if iv[4]==confed1:
                        win1*=float(iv[2])
                        awin1*=float(iv[6])
                    else:
                        win1*=float(iv[3])
                        awin1*=float(iv[7])

                    win2 = float(i[3])
                    awin2 = float(i[7])
                    if ii[4]==confed2:
                        win2*=float(ii[2])
                        awin2*=float(ii[6])
                    else:
                        win2*=float(ii[3])
                        awin2*=float(ii[7])
                    if iii[4]==confed2:
                        win2*=float(iii[2])
                        awin2*=float(iii[6])
                    else:
                        win2*=float(iii[3])
                        awin2*=float(iii[7])
                    if iv[4]==confed2:
                        win2*=float(iv[2])
                        awin2*=float(iv[6])
                    else:
                        win2*=float(iv[3])
                        awin2*=float(iv[7])
                    drawp = float(i[8])*float(ii[8])*float(iii[8])*float(iv[8])
                    drawa = float(i[9])*float(ii[9])*float(iii[9])*float(iv[9])

                    broll -= win1
                    broll -= win2
                    broll += awin1
                    broll += awin2
                    broll -= drawp
                    broll += drawa
                    ngames +=1

print broll,ngames



broll = 0.
ngames = 0.
for i in allpred:
    for ii in allpred:
        for iii in allpred:
            allteams = [i[0],i[1],ii[0],ii[1],iii[0],iii[1]]
            allconfeds = [i[4],i[5],ii[4],ii[5],iii[4],iii[5]]
            diffteams = True
            for iiii in range(0,len(allteams)):
                for iv in allteams[iiii+1:]:
                    if allteams[iiii]==iv:
                        diffteams = False
            diffconfeds = True
            if i[4]==i[5]:
                diffconfeds = False
            if ii[4]==ii[5]:
                diffconfeds = False
            if iii[4]==iii[5]:
                diffconfeds = False

            threeconfeds = True
            
            confed1 = allconfeds[0]
            confed2 = allconfeds[1]
            if allconfeds[2]!=confed1 and allconfeds[2]!= confed2:
                confed3 = allconfeds[2]
                for iiii in allconfeds[3:]:
                    if iiii!=confed1 and iiii!=confed2 and iiii!=confed3: 
                        threeconfeds = False
            else:
                if allconfeds[3]!=confed1 and allconfeds[3]!= confed2:
                    confed3 = allconfeds[3]
                    for iiii in allconfeds[4:]:
                        if iiii!=confed1 and iiii!=confed2 and iiii!=confed3: 
                            threeconfeds = False
            

            if diffteams and diffconfeds and threeconfeds:
                win1 = float(i[2])
                awin1 = float(i[6])
                if ii[4]==confed1:
                    win1*=float(ii[3])
                    awin1*=float(ii[7])
                elif ii[5]==confed1:
                    win1*=float(ii[2])
                    awin1*=float(ii[6])
                else:
                    if ii[4]==confed2:
                        win1*=float(ii[2])
                        awin1*=float(ii[6])
                    else:
                        win1*=float(ii[3])
                        awin1*=float(ii[7])

                if iii[4]==confed1:
                    win1*=float(iii[3])
                    awin1*=float(iii[7])
                elif iii[5]==confed1:
                    win1*=float(iii[2])
                    awin1*=float(iii[6])
                else:
                    if iii[4]==confed2:
                        win1*=float(iii[2])
                        awin1*=float(iii[6])
                    else:
                        win1*=float(iii[3])
                        awin1*=float(iii[7])

                win2 = float(i[3])
                awin2 = float(i[7])
                if ii[4]==confed2:
                    win2*=float(ii[3])
                    awin2*=float(ii[7])
                elif ii[5]==confed2:
                    win2*=float(ii[2])
                    awin2*=float(ii[6])
                else:
                    if ii[4]==confed1:
                        win2*=float(ii[2])
                        awin2*=float(ii[6])
                    else:
                        win2*=float(ii[3])
                        awin2*=float(ii[7])
                if iii[4]==confed2:
                    win2*=float(iii[3])
                    awin2*=float(iii[7])
                elif iii[5]==confed2:
                    win2*=float(iii[2])
                    awin2*=float(iii[6])
                else:
                    if iii[4]==confed1:
                        win2*=float(iii[2])
                        awin2*=float(iii[6])
                    else:
                        win2*=float(iii[3])
                        awin2*=float(iii[7])


                broll -= win1
                broll -= win2
                broll += awin1
                broll += awin2

                ngames +=1

print broll,ngames
print 'best:'


broll = 0.
ngames = 0.
for i in allpred:
    for ii in allpred:
        for iii in allpred:
            for iv in allpred:
                allteams = [i[0],i[1],ii[0],ii[1],iii[0],iii[1],iv[0],iv[1]]
                allconfeds = [i[4],i[5],ii[4],ii[5],iii[4],iii[5],iv[4],iv[5]]
                diffteams = True
                for iiii in range(0,len(allteams)):
                    for iiv in allteams[iiii+1:]:
                        if allteams[iiii]==iiv:
                            diffteams = False
                diffconfeds = True
                if i[4]==i[5]:
                    diffconfeds = False
                if ii[4]==ii[5]:
                    diffconfeds = False
                if iii[4]==iii[5]:
                    diffconfeds = False
                if iv[4]==iv[5]:
                    diffconfeds = False

                nconfeds1 = 1
                nconfeds2 = 1
                
                confed1 = allconfeds[0]
                confed2 = allconfeds[1]
                for iiii in allconfeds[2:]:
                    if iiii==confed1:
                        nconfeds1+=1
                    if iiii==confed2:
                        nconfeds2+=1

                if diffteams and diffconfeds and max(nconfeds1,nconfeds2)>=2.5 and min(nconfeds1,nconfeds2)>=2.5:
                    win1 = float(i[2])
                    awin1 = float(i[6])
                    if ii[4]==confed1:
                        win1*=float(ii[2])
                        awin1*=float(ii[6])
                    elif ii[5]==confed1:
                        win1*=float(ii[3])
                        awin1*=float(ii[7])
                    else:
                        win1*=1
                        awin1*=1
                    if iii[4]==confed1:
                        win1*=float(iii[2])
                        awin1*=float(iii[6])
                    elif iii[5]==confed1:
                        win1*=float(iii[3])
                        awin1*=float(iii[7])
                    else:
                        win1*=1
                        awin1*=1
                    if iv[4]==confed1:
                        win1*=float(iv[2])
                        awin1*=float(iv[6])
                    elif iv[5]==confed1:
                        win1*=float(iv[3])
                        awin1*=float(iv[7])
                    else:
                        win1*=1
                        awin1*=1

                    win2 = float(i[3])
                    awin2 = float(i[7])
                    if ii[4]==confed2:
                        win2*=float(ii[2])
                        awin2*=float(ii[6])
                    elif ii[5]==confed2:
                        win2*=float(ii[3])
                        awin2*=float(ii[7])
                    else:
                        win2*=1
                        awin2*=1
                    if iii[4]==confed2:
                        win2*=float(iii[2])
                        awin2*=float(iii[6])
                    elif iii[5]==confed2:
                        win2*=float(iii[3])
                        awin2*=float(iii[7])
                    else:
                        win2*=1
                        awin2*=1
                    if iv[4]==confed2:
                        win2*=float(iv[2])
                        awin2*=float(iv[6])
                    elif iv[5]==confed2:
                        win2*=float(iv[3])
                        awin2*=float(iv[7])
                    else:
                        win2*=1
                        awin2*=1


                    broll -= win1
                    broll -= win2
                    broll += awin1
                    broll += awin2

                    ngames +=1

print broll,ngames



cid = 0
for cid in []:
    games = []
    for i in confedteams[cid]:
        games.append([]) 
        for ii in allpred:
            if ii[0]==i and ii[1] not in confedteams[cid]:
                games[-1].append([float(ii[2]),float(ii[6]),float(ii[3]),float(ii[7])])
            if ii[1]==i and ii[0] not in confedteams[cid]:
                games[-1].append([float(ii[3]),float(ii[7]),float(ii[2]),float(ii[6])])

    for i in games:
        print i

    if cid==0:
        broll = 0.
        for i in range(0,81):
            g1 = games[0][i%3]
            g2 = games[1][(i%9)/3]
            g3 = games[2][(i%27)/9]
            g4 = games[3][(i%81)/27]
            parlaywins = g1[0]*g2[0]*g3[0]*g4[0]
            parlaylosses = g1[2]*g2[2]*g3[2]*g4[2]
            if g1[1]>.5 and g2[1]>.5 and g3[1]>.5 and g4[1]>.5:
                broll +=1
            if g1[3]>.5 and g2[3]>.5 and g3[3]>.5 and g4[3]>.5:
                broll +=1
            broll -=parlaywins
            broll -=parlaylosses
        print broll

        for ii in range(0,4):

            broll = 0.
            allids = []
            for i in range(0,4):
                if i !=ii:
                    allids.append(i)
            for i in range(0,27):
                g1 = games[allids[0]][i%3]
                g2 = games[allids[1]][(i%9)/3]
                g3 = games[allids[2]][(i%27)/9]
                parlaywins = g1[0]*g2[0]*g3[0]
                parlaylosses = g1[2]*g2[2]*g3[2]
                if g1[1]>.5 and g2[1]>.5 and g3[1]>.5:
                    broll +=1
                if g1[3]>.5 and g2[3]>.5 and g3[3]>.5:
                    broll +=1
                broll -=parlaywins
                broll -=parlaylosses
            print broll
    elif cid in [4,5]:
        broll = 0.
        for i in range(0,27):
            g1 = games[0][i%3]
            g2 = games[1][(i%9)/3]
            g3 = games[2][(i%27)/9]
            parlaywins = g1[0]*g2[0]*g3[0]
            parlaylosses = g1[2]*g2[2]*g3[2]
            if g1[1]>.5 and g2[1]>.5 and g3[1]>.5:
                broll +=1
            if g1[3]>.5 and g2[3]>.5 and g3[3]>.5:
                broll +=1
            broll -=parlaywins
            broll -=parlaylosses
        print broll
    elif cid==1:
        broll = 0.
        for i in range(0,243):
            g1 = games[0][i%3]
            g2 = games[1][(i%9)/3]
            g3 = games[2][(i%27)/9]
            g4 = games[3][(i%81)/27]
            g5 = games[4][(i%243)/81]
            parlaywins = g1[0]*g2[0]*g3[0]*g4[0]*g5[0]
            parlaylosses = g1[2]*g2[2]*g3[2]*g4[2]*g5[2]
            if g1[1]>.5 and g2[1]>.5 and g3[1]>.5 and g4[1]>.5 and g5[1]>.5:
                broll +=1
            if g1[3]>.5 and g2[3]>.5 and g3[3]>.5 and g4[3]>.5 and g5[3]>.5:
                broll +=1
            broll -=parlaywins
            broll -=parlaylosses
        print cid, broll
        for ii in range(0,5):

            broll = 0.
            allids = []
            for i in range(0,5):
                if i !=ii:
                    allids.append(i)
            for i in range(0,81):
                g1 = games[allids[0]][i%3]
                g2 = games[allids[1]][(i%9)/3]
                g3 = games[allids[2]][(i%27)/9]
                g4 = games[allids[3]][(i%81)/27]
                parlaywins = g1[0]*g2[0]*g3[0]*g4[0]
                parlaylosses = g1[2]*g2[2]*g3[2]*g4[2]
                if g1[1]>.5 and g2[1]>.5 and g3[1]>.5 and g4[1]>.5:
                    broll +=1
                if g1[3]>.5 and g2[3]>.5 and g3[3]>.5 and g4[3]>.5:
                    broll +=1
                broll -=parlaywins
                broll -=parlaylosses
            print cid, allids, broll
        for ii in range(0,10):

            broll = 0.
            notids = []
            if ii<4:
                notids.append(0)
                notids.append(ii+1)
            elif ii<7:
                notids.append(1)
                notids.append(ii-2)
            elif ii<9:
                notids.append(2)
                notids.append(ii-4)
            else:
                notids.append(3)
                notids.append(4)
            allids = []
            for i in range(0,5):
                if i not in notids:
                    allids.append(i)
            for i in range(0,27):
                g1 = games[allids[0]][i%3]
                g2 = games[allids[1]][(i%9)/3]
                g3 = games[allids[2]][(i%27)/9]
                parlaywins = g1[0]*g2[0]*g3[0]
                parlaylosses = g1[2]*g2[2]*g3[2]
                if g1[1]>.5 and g2[1]>.5 and g3[1]>.5:
                    broll +=1
                if g1[3]>.5 and g2[3]>.5 and g3[3]>.5:
                    broll +=1
                broll -=parlaywins
                broll -=parlaylosses
            print cid, allids, broll
    elif cid==3:
        broll = 0.
        allids = [0,3,4,7]
        for i in range(0,81):
            g1 = games[allids[0]][i%3]
            g2 = games[allids[1]][(i%9)/3]
            g3 = games[allids[2]][(i%27)/9]
            g4 = games[allids[3]][(i%81)/27]
            parlaywins = g1[0]*g2[0]*g3[0]*g4[0]
            parlaylosses = g1[2]*g2[2]*g3[2]*g4[2]
            if g1[1]>.5 and g2[1]>.5 and g3[1]>.5 and g4[1]>.5:
                broll +=1
            if g1[3]>.5 and g2[3]>.5 and g3[3]>.5 and g4[3]>.5:
                broll +=1
            broll -=parlaywins
            broll -=parlaylosses
        print broll
    elif cid==30:
        broll = 0.
        for i in range(0,243*27):
            g1 = games[0][i%3]
            g2 = games[1][(i%9)/3]
            g3 = games[2][(i%27)/9]
            g4 = games[3][(i%81)/27]
            g5 = games[4][(i%243)/81]
            g6 = games[5][(i%729)/243]
            g7 = games[6][(i%(243*9))/729]
            g8 = games[7][(i%(243*27))/729/3]
            parlaywins = g1[0]*g2[0]*g3[0]*g4[0]*g5[0]*g6[0]*g7[0]*g8[0]
            parlaylosses = g1[2]*g2[2]*g3[2]*g4[2]*g5[0]*g6[2]*g7[2]*g8[2]
            if g1[1]>.5 and g2[1]>.5 and g3[1]>.5 and g4[1]>.5 and g5[1]>.5 and g6[1]>.5 and g7[1]>.5 and g8[1]>.5:
                broll +=1
            if g1[3]>.5 and g2[3]>.5 and g3[3]>.5 and g4[3]>.5 and g5[3]>.5 and g6[3]>.5 and g7[3]>.5 and g8[3]>.5:
                broll +=1
            broll -=parlaywins
            broll -=parlaylosses
        print broll

































print soto

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




    
