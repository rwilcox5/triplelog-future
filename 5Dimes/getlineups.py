import time

import random
import csv
import math
import threading
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


def writecsvstr(parr, filen):
        with open(filen, 'wb') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in range(0,len(parr)):
                        try:
                                spamwriter.writerow(parr[i])
                        except:
                                print parr[i], i


pagen = 10
theyear = 2016

#combine()
#print stopit




##This gets all the owners from the conferences to check if sims or not.

def getplayerlist(driver,pagen):

    b_url = "http://www.baseballpress.com/lineups/2017-08-14"
    driver.get(b_url)
    time.sleep(3)
    allgames = driver.find_elements_by_class_name('game')
    print len(allgames)
    allteams = []
    allplayers = []
    for game in allgames:
        teams = game.find_elements_by_class_name('team-data')
        for team in teams:
            allteams.append(team.find_element_by_tag_name('a').get_attribute('href'))
        lineups = game.find_elements_by_class_name('players')
        for lineup in lineups:
            teamplayers = []
            players = lineup.find_elements_by_tag_name('a')
            for player in players:
                teamplayers.append([str(player.text),str(player.get_attribute('data-mlb'))])
            allplayers.append(teamplayers)
    print len(allteams)

    print allteams
    print allplayers
        
    return ap

def getbref(driver,pagen):
    allteams = ['ARI','ATL','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET','HOU','KCR','LAA','LAD','MIA','MIL','MIN','NYM','NYY','OAK','PHI','PIT','SDP','SEA','SFG','STL','TBR','TEX','TOR','WSN']
    allplayers = []
    for team in allteams:
        b_url = "https://www.baseball-reference.com/teams/"+team+"/2017-roster.shtml"
        driver.get(b_url)
        time.sleep(3)
        roster = driver.find_element_by_id('the40man')
        players = roster.find_elements_by_tag_name('a')
        
        for player in players:
            pname = str(player.text)
            if pname[1]=='.' and pname[3]=='.':
                pname = pname[0]+pname[2]+'.'+pname[5:]
            else:
                index = pname.find(' ')
                pname = pname[0]+'.'+pname[index+1:]
            href = str(player.get_attribute('href'))
            index = href.find('mlb_ID=')
            allplayers.append([team, pname,href[index+7:]])
        print allplayers

        
    return allplayers

def login5dimes(driver):
    b_url = "https://www.5dimes.eu/"
    driver.get(b_url)
    time.sleep(1)
    driver.find_element_by_id('customerID').send_keys('5d1998716')
    time.sleep(1)
    driver.find_element_by_name('password').send_keys('5DimeS')
    time.sleep(1)
    driver.find_element_by_name('submit1').click()
    time.sleep(1)
    driver.find_element_by_id('chkRead').click()
    time.sleep(1)
    driver.find_element_by_name('Baseball_Props').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="btnContinue"]').click()

def get5dimes(driver,pagen):
    brefteams = ['ARI','ATL','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET','HOU','KCR','LAA','LAD','MIA','MIL','MIN','NYM','NYY','OAK','PHI','PIT','SDP','SEA','SFG','STL','TBR','TEX','TOR','WSN']
    teams5dimes = ['ARI','ATL','BAL','BOS','CUB','CWS','CIN','CLE','COL','DET','HOU','KAN','LAA','LOS','MIA','MIL','MIN','NYM','NYY','OAK','PHI','PIT','SDG','SEA','SFO','STL','TAM','TEX','TOR','WAS']
    time.sleep(1)
    tophalves = driver.find_elements_by_class_name('linesRow')
    bothalves = driver.find_elements_by_class_name('linesRowBot')
    for top in tophalves:
        try:
            allcells = top.find_elements_by_tag_name('td')
            cell1 = str(allcells[0].text)
            if cell1.find('Mon')>-1 or cell1.find('Tue')>-1 or cell1.find('Wed')>-1 or cell1.find('Thu')>-1 or cell1.find('Fri')>-1 or cell1.find('Sat')>-1 or cell1.find('Sun')>-1:
                cell2 = str(allcells[2].text) 
                index = cell2.find(' ')
                betid = cell2[:index]
                index2 = cell2.find(' ', index+1)
                teamid = cell2[index+1:index2]
                if teamid not in teams5dimes:
                    if len(teamid)==3:
                        print teamid
                index3 = cell2.find(' ', index2+1)
                playerid = cell2[index2+1:index3]
                blankid = allcells[4].find_element_by_tag_name('input').get_attribute('name')
                #print betid, teamid, playerid
                for i,teamabb in enumerate(teams5dimes):
                    if teamid == teamabb:
                        print blankid

        except:
            pass
    for bot in bothalves:
        try:
            allcells = bot.find_elements_by_tag_name('td')
            cell1 = str(allcells[0].text)
            if cell1.find('PM')>-1 or cell1.find('AM')>-1:
                cell2 = str(allcells[2].text) 
                index = cell2.find(' ')
                betid = cell2[:index]
                index2 = cell2.find(' ', index+1)
                teamid = cell2[index+1:index2]
                if teamid not in teams5dimes:
                    if len(teamid)==3:
                        print teamid
                index3 = cell2.find(' ', index2+1)
                playerid = cell2[index2+1:index3]
                blankid = allcells[4].find_element_by_tag_name('input').get_attribute('name')
                #print betid, teamid, playerid
        except:
            pass

    for team in allteams:
        
        
        for player in players:
            pname = str(player.text)
            if pname[1]=='.' and pname[3]=='.':
                pname = pname[0]+pname[2]+'.'+pname[5:]
            else:
                index = pname.find(' ')
                pname = pname[0]+'.'+pname[index+1:]
            href = str(player.get_attribute('href'))
            index = href.find('mlb_ID=')
            allplayers.append([team, pname,href[index+7:]])
        print allplayers

        
    return allplayers

driver = webdriver.Chrome()
login5dimes(driver)
get5dimes(driver,0)
print stopit

print stopit
allplayers = getplayerlist(driver,0)
writecsvstr(allplayers,"lineup"+str(theyear)+".csv")
print stopit
#allplayers = ["https://n.rivals.com/content/prospects/maple/138337"]
def readcsv(filen):
        allgamesa  =[]
        with open(filen, 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                        allgamesa.append(row)
        return allgamesa
def readcsva(filen):
        allgamesa  =[]
        with open(filen, 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                        allgamesa.append(row[0])
        return allgamesa
try:
        playersdone = readcsva("allplayers2016act"+str(theyear)+"done.csv")
except:
        playersdone = []
allplayersa = readcsva("allplayers2016act"+str(theyear)+".csv")
allplayers = []
print allplayersa[:3]
print playersdone[:3]
for i in allplayersa:
        if i not in playersdone:
                allplayers.append(i)
print len(allplayers)

#print stopit
def runthis(driver,ii,adone,allsl):
        iii = 0
        lx =len(allplayers)
        lx = 1000
        nerror = 0
        nodone = 0
        for i in allplayers[(lx/5+1)*ii:(lx/5+1)*(1+ii)]:
                #allsl = getreclist(driver,i,allsl)
                if i not in adone:
                        try:
                                allsl = getreclist(driver,i,[])
                                adone = [[i,"Y"]]
                                writecsva(allsl,"allrecs"+str(theyear)+str(ii)+".csv")
                                writecsva(adone,"allplayers2016act"+str(theyear)+"done.csv")
                        except:
                                nodone = 1
                                break
                        iii=iii+1
                        
        print ii, "DONE", nodone
        driver.close()
for ii in range(0,1):
        driver = []
        t = []
        for i in range(0,5):
                t.append(0)
                #firefox_profile = webdriver.FirefoxProfile()
                #firefox_profile.set_preference("browser.download.folderList",2)
                #firefox_profile.set_preference("permissions.default.stylesheet",2)
                #firefox_profile.set_preference("permissions.default.image",2)
                #firefox_profile.set_preference("javascript.enabled", False)
                options = webdriver.ChromeOptions() 

                driver.append(webdriver.Chrome(chrome_options=options))
                driver[i].implicitly_wait(30)
                t[i] = Thread(target=runthis,args=(driver[i],i,[],[]))
                t[i].start()
                print "TAC=", threading.active_count()
                print "started", i


