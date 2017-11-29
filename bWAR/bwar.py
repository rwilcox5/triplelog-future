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
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                        allgamesa.append(row)
        return allgamesa

year = 2010
allbatwar = readcsv('war_daily_bat.csv')
allpitchwar = readcsv('war_daily_pitch.csv')

allyearsb = []
for ii in range(0,60):
        allyearsb.append(0)
for i in allbatwar[1:]:
        if int(i[1])>year:
                if i[13]=='N':
                        try:
                                allyearsb[int(i[0])]+=float(i[9])
                        except:
                                pass
allyearsb[20]=sum(allyearsb[:21])
allyearsb[40]=sum(allyearsb[40:])

allyearsp = []
for ii in range(0,60):
        allyearsp.append(0)
for i in allpitchwar[1:]:
        if int(i[1])>year:
                try:
                        allyearsp[int(i[0])]+=float(i[9])
                except:
                        pass
allyearsp[20]=sum(allyearsp[:21])
allyearsp[40]=sum(allyearsp[40:])
sumb = sum(allyearsb)
sump = sum(allyearsp)
allratings = []
for i in range(20,41):
        allratings.append([500*max(allyearsb[i]/sumb,0),500*max(allyearsp[i]/sump,0)])

print 'allratings1=',allratings,';'

allyearsb = []
for ii in range(0,60):
        allyearsb.append(0)
for i in allbatwar[1:]:
        if int(2017)>year:
                if i[13]=='N':
                        try:
                                allyearsb[int(i[0])]+=float(i[9])
                        except:
                                pass
allyearsb[20]=sum(allyearsb[:21])
allyearsb[40]=sum(allyearsb[40:])

allyearsp = []
for ii in range(0,60):
        allyearsp.append(0)
for i in allpitchwar[1:]:
        if int(2017)>year:
                try:
                        allyearsp[int(i[0])]+=float(i[9])
                except:
                        pass
allyearsp[20]=sum(allyearsp[:21])
allyearsp[40]=sum(allyearsp[40:])
sumb = sum(allyearsb)
sump = sum(allyearsp)
allratings = []
for i in range(20,41):
        allratings.append([500*max(allyearsb[i]/sumb,0),500*max(allyearsp[i]/sump,0)])

print 'allratings2=',allratings,';'                   
