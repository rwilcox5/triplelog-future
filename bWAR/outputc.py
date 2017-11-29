import time
import random
import csv
import math
import threading
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


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
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in spamreader:
                        allgamesa.append(row)
        return allgamesa

year = 2010
allbatwar = readcsv('war_daily_bat.csv')
allpitchwar = readcsv('war_daily_pitch.csv')
teams = []
for i in allbatwar[1:]:
        if i[13]=='N':
                if i[2] not in teams:
                        teams.append(i[2])


alli = []
print len(allpitchwar), len(allbatwar)
for idx,i in enumerate(allpitchwar[1:]):
        if idx %1000==0:
                print idx, len(alli)
        for iidx,ii in enumerate(teams):
                if ii==i[2]:
                        teamid = iidx
        if i[3]=='NL':
                lgid = 0
        elif i[3]=='AL':
                lgid=1
        else:
                lgid=2
        try:
                noadd = False
                for iidx,ii in enumerate(alli):
                        if int(i[0])==ii[0] and int(i[1])==ii[1] and teamid==ii[2] and lgid==ii[3]:
                                alli[iidx][4]+= int(float(i[9])*100)
                                noadd = True
                if not noadd:
                        alli.append([int(i[0]),int(i[1]),teamid,lgid,int(float(i[9])*100),0])
        except:
                print i




for idx,i in enumerate(allbatwar[1:]):
        if idx %1000==0:
                print idx, len(alli)
        if i[13]=='N':
                for iidx,ii in enumerate(teams):
                        if ii==i[2]:
                                teamid = iidx
                if i[3]=='NL':
                        lgid = 0
                elif i[3]=='AL':
                        lgid=1
                else:
                        lgid=2
                try:
                        noadd = False
                        for iidx,ii in enumerate(alli):
                                if int(i[0])==ii[0] and int(i[1])==ii[1] and teamid==ii[2] and lgid==ii[3]:
                                        alli[iidx][5]+= int(float(i[9])*100)
                                        noadd = True
                        if not noadd:
                                alli.append([int(i[0]),int(i[1]),teamid,lgid,0,int(float(i[9])*100)])

                except:
                        print i
istr = 'int alldata[] = {'
np  = 0
for i in alli:
        istr += str(int(i[0]))+','+str(int(i[1]))+','+str(i[2])+','+str(i[3])+','+str(i[4])+','+str(i[5])+','
        np+=1

istr = istr[:-1]+'};'
f = open('helloworld.txt','w')
f.write(istr+'\n'+'int nplayers = '+str(np)+';')
f.close()