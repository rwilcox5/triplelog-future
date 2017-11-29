import random

def creategame():
    thedeck = []
    for iii in range(0,52):
        thecard = []
        thecard.append(iii%13+1)
        thecard.append(iii%4)
        thedeck.append(thecard)
    #print thedeck

    columns = []
    for iii in range(0,7):
        tcol = []
        for ii in range(0,iii+1):
            randomcard = random.randint(0,len(thedeck)-1)
            tcard = thedeck[randomcard]
            if iii==ii:
                thecard = [tcard[0],tcard[1],1]
            else:
                thecard = [tcard[0],tcard[1],0]
            tcol.append(thecard)
            thedeck.remove(tcard)
        
        columns.append(tcol)

    tdeck = []
    for ii in range(0,24):
        randomcard = random.randint(0,len(thedeck)-1)
        tdeck.append(thedeck[randomcard])
        thedeck.remove(thedeck[randomcard])

    thedeck = tdeck

    toprow = [0,0,0,0]

    i=2
    counter = 0

    return thedeck,toprow,columns,i,counter

def movecards(x,y,columns):
    maxi = 0
    for ii in range(0,len(columns[x])):
        if columns[x][ii][2]==0:
            maxi = maxi+1
            
    columns[y]=columns[y]+columns[x][maxi:]
    columns[x]=columns[x][:maxi]
    return columns

def flipcard(x,columns):
    if len(columns[x])>0:
        columns[x][len(columns[x])-1][2]=1
    return columns

def uptotop(x,columns,toprow):
    stotop = columns[x][len(columns[x])-1][1]
    toprow[stotop] = toprow[stotop]+1
    columns[x]=columns[x][:len(columns[x])-1]
    
    return columns, toprow

def deal(i,thedeck):
    if len(thedeck)>i+3:
        i=i+3
    elif len(thedeck)-1==i:
        if len(thedeck)>2:
            i=2
        else:
            i=len(thedeck)-1
    else:
        i = len(thedeck)-1
    return i

def downfromdeal(x,columns,thedeck,i):
    columns[x]=columns[x]+[thedeck[i]]
    thedeck.remove(thedeck[i])
    if i>0:
        i=i-1
    return columns, thedeck, i
    
    
def upfromdeal(thedeck,toprow,i):
    stotop = thedeck[i][1]
    toprow[stotop] = toprow[stotop]+1
    thedeck.remove(thedeck[i])
    if i>0:
        i=i-1
    return thedeck,toprow,i
def dispcolumns(columns, toprow, upcard):
    print '----------------------------------------------------------------'
    print upcard,
    print "                           ",
    print toprow
    for ii in range(0,20):
        iscard=True
        for iii in range(0,7):
            if len(columns[iii])>ii:
                if columns[iii][ii][2]==1:
                    iscard=False
                    if columns[iii][ii][0]>9:
                        cc0 = ""+str(columns[iii][ii][0])
                        cc1 = columns[iii][ii][1]
                        print [cc0,cc1],
                    else:
                        cc0 = " "+str(columns[iii][ii][0])
                        cc1 = columns[iii][ii][1]
                        print [cc0,cc1],
                else:
                    iscard=False
                    print '---------',
            else:
                
                print '         ',
        print ""
        if iscard:
            break

def deckfreescard(type,columns,thedeck,i):
    if type == 'down':
        for ii in range(0,7):
            maxi = 0
            for iii in range(0,len(columns[ii])):
                if columns[ii][iii][2]==0:
                    maxi = maxi+1
            if len(columns[ii])>0:
                if columns[ii][maxi][0]==thedeck[i][0]-1 and columns[ii][maxi][1]%2!=thedeck[i][1]%2:
                    return True
    if type == 'up':
        for ii in range(0,7):
            maxi = 0
            for iii in range(0,len(columns[ii])):
                if columns[ii][iii][2]==0:
                    maxi = maxi+1
            if len(columns[ii])>0:
                if len(columns[ii])==maxi+1:
                    if columns[ii][maxi][0]==thedeck[i][0]+1 and columns[ii][maxi][1]==thedeck[i][1]:
                        return True
    return False

def stackfreescard(columns,card):
    for ii in range(0,7):
        maxi = 0
        for iii in range(0,len(columns[ii])):
            if columns[ii][iii][2]==0:
                maxi = maxi+1
        if len(columns[ii])>0:
            if columns[ii][maxi][0]==card[0] and columns[ii][maxi][1]%2==card[1]%2:
                return True

    return False
def waitingking(columns):
    for ii in range(0,7):
        maxi = 0
        for iii in range(0,len(columns[ii])):
            if columns[ii][iii][2]==0:
                maxi = maxi+1
        if maxi>0:
            if columns[ii][maxi][0]==13:
                return True

    return False
def getups(columns,toprow):
    ups = []
    for ii in range(0,7):
        covered = False
        freescard = False
        clearking = False
        if len(columns[ii])>0:
            maxi = 0
            for iii in range(0,len(columns[ii])):
                if columns[ii][iii][2]==0:
                    maxi = maxi+1
            if columns[ii][len(columns[ii])-1][0]==toprow[columns[ii][len(columns[ii])-1][1]]+1:
                if columns[ii][len(columns[ii])-1][1] in [0,2]:
                    if toprow[1]>columns[ii][len(columns[ii])-1][0]-3 and toprow[3]>columns[ii][len(columns[ii])-1][0]-3:
                        covered = True
                    elif len(columns[ii])==maxi+1:
                        freescard = True
                    elif len(columns[ii])==1:
                        if waitingking(columns):
                            clearking = True
                    elif stackfreescard(columns,columns[ii][len(columns[ii])-2]):
                        freescard = True
                elif columns[ii][len(columns[ii])-1][1] in [1,3]:
                    if toprow[0]>columns[ii][len(columns[ii])-1][0]-3 and toprow[2]>columns[ii][len(columns[ii])-1][0]-3:
                        covered = True
                    elif len(columns[ii])==maxi+1:
                        freescard = True
                    elif len(columns[ii])==1:
                        if waitingking(columns):
                            clearking = True
                    elif stackfreescard(columns,columns[ii][len(columns[ii])-2]):
                        freescard = True    
                ups.append([ii,covered,freescard,clearking])
    return ups
#thedeck, toprow, i = upfromdeal(thedeck,toprow, 7)
def getsides(columns):
    sides = []
    for ii in range(0,7):
        fromblank = False
        if len(columns[ii])>0:
            maxi = 0
            for iii in range(0,len(columns[ii])):
                if columns[ii][iii][2]==0:
                    maxi = maxi+1
            if maxi > 0:
                for iii in range(0,7):
                    isking = False
                    if len(columns[iii])>0:
                        if columns[ii][maxi][0]==columns[iii][len(columns[iii])-1][0]-1 and columns[ii][maxi][1]%2!=columns[iii][len(columns[iii])-1][1]%2:
                            toblank = False
                            sides.append([ii,maxi,toblank,isking,iii,fromblank])
                    else:
                        toblank = True
                        if columns[ii][maxi][0]==13:
                            isking = True
                            sides.append([ii,maxi,toblank,isking,iii,fromblank])

            elif columns[ii][0][0]!= 13:
                for iii in range(0,7):
                    isking = False
                    if len(columns[iii])>0:
                        if columns[ii][maxi][0]==columns[iii][len(columns[iii])-1][0]-1 and columns[ii][maxi][1]%2!=columns[iii][len(columns[iii])-1][1]%2:
                            toblank = False
                            fromblank = True
                            sides.append([ii,maxi,toblank,isking,iii,fromblank])


    return sides
def getdowns(columns,thedeck,i):
    downs = []
    if len(thedeck)>0:
        for ii in range(0,7):
            isking = False
            if len(columns[ii])>0:
                if columns[ii][len(columns[ii])-1][0]==thedeck[i][0]+1 and columns[ii][len(columns[ii])-1][1]%2!=thedeck[i][1]%2:
                    freescard = deckfreescard('down',columns,thedeck,i)
                    downs.append([ii,freescard,isking])
            else:
                freescard = deckfreescard('down',columns,thedeck,i)
                if thedeck[i][0]==13:
                    isking = True
                downs.append([ii,freescard,isking])
    return downs
def gettoptotops(columns,thedeck,i,toprow):
    toptotops = []
    covered = False
    if len(thedeck)>0:
        if thedeck[i][0]==toprow[thedeck[i][1]]+1:
            freescard = deckfreescard('up',columns,thedeck,i)
            if thedeck[i][1] in [0,2]:
                if toprow[1]>thedeck[i][0]-2 and toprow[3]>thedeck[i][0]-2:
                    covered = True
            else:
                if toprow[0]>thedeck[i][0]-2 and toprow[2]>thedeck[i][0]-2:
                    covered = True

            toptotops.append([freescard,covered])
    return toptotops


def playsmart(thedeck,toprow,columns,i,counter,ncardsup,allplays):
    sideblank = False
    downking = False
    downother = False
    upother = False
    topother = False
    topcover = False
    for iiii in range(0,10000):
        keepgoing = True
        ups = getups(columns,toprow)
        sides = getsides(columns)
        downs = getdowns(columns,thedeck,i)
        toptotops = gettoptotops(columns,thedeck,i,toprow)
        for iii in ups:
            if iii[1]:
                columns, toprow = uptotop(iii[0],columns,toprow)
                columns = flipcard(iii[0],columns)
                keepgoing = False
                allplays[0] +=1
                break
        
        if keepgoing:
            maxbelow = -1
            sidenow = False
            for iii in sides:
                if not iii[5]:
                    if not iii[2]:
                        if iii[1]>maxbelow:
                            doside = iii
                            maxbelow = iii[1]
                            sidenow = True
                    elif iii[3]:
                        if iii[1]>maxbelow:
                            doside = iii
                            maxbelow = iii[1]
                            sidenow = True
            if sidenow:
                columns = movecards(doside[0],doside[4],columns)
                columns = flipcard(doside[0],columns)
                keepgoing = False
                allplays[1] +=1
        
        if keepgoing:
            goodcard = False
            lasti = -1
            if len(thedeck)>2:
                for iii in range(i/3,(len(thedeck)-1)/3):
                    downst = getdowns(columns,thedeck,iii*3+2)
                    toptotopst = gettoptotops(columns,thedeck,iii*3+2,toprow)
                    for iiiii in downst:
                        if iiiii[1]:
                            goodcard = True
                            lasti = iii*3+2
                            downsi = iiiii
            if lasti > -1:
                columns,thedeck,i = downfromdeal(downsi[0],columns,thedeck,lasti)
                columns[downsi[0]][len(columns[downsi[0]])-1].append(1)
                keepgoing = False
                allplays[3] +=1
            else:
                if i == len(thedeck)-1:
                    for iii in downs:
                        if iii[1]:
                            columns,thedeck,i = downfromdeal(iii[0],columns,thedeck,i)
                            columns[iii[0]][len(columns[iii[0]])-1].append(1)
                            keepgoing = False
                            allplays[3] +=1
                            break
                else:
                    if not goodcard:
                        for iii in downs:
                            if iii[1]:
                                columns,thedeck,i = downfromdeal(iii[0],columns,thedeck,i)
                                columns[iii[0]][len(columns[iii[0]])-1].append(1)
                                keepgoing = False
                                allplays[3] +=1
                                break
                    elif i%3 != 2:
                    #else:
                        for iii in downs:
                            if iii[1]:
                                columns,thedeck,i = downfromdeal(iii[0],columns,thedeck,i)
                                columns[iii[0]][len(columns[iii[0]])-1].append(1)
                                keepgoing = False
                                allplays[3] +=1
                                break
        
        
        if keepgoing:
            goodcard = False
            lasti = -1
            if len(thedeck)>2:
                for iii in range(i/3,(len(thedeck)-1)/3):
                    downst = getdowns(columns,thedeck,iii*3+2)
                    toptotopst = gettoptotops(columns,thedeck,iii*3+2,toprow)
                    for iiiii in downst:
                        if iiiii[1]:
                            goodcard = True

                    for iiiii in toptotopst:
                        if iiiii[1]:
                            goodcard = True  
                            lasti = iii*3+2


            if lasti > -1:
                thedeck,toprow,i =upfromdeal(thedeck,toprow,lasti)
                keepgoing = False
                topcover = False
                allplays[4] +=1
            else:
                if i == len(thedeck)-1:
                    for iii in toptotops:
                        if iii[1]:
                            thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                            keepgoing = False
                            topcover = False
                            allplays[4] +=1
                            break
                else:
                    if not goodcard:
                        for iii in toptotops:
                            if iii[1]:
                                thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                keepgoing = False
                                topcover = False
                                allplays[4] +=1
                                break
        #if keepgoing:
        #    for iii in ups:
        #        if iii[2] or iii[3]:
        #            columns, toprow = uptotop(iii[0],columns,toprow)
        #            columns = flipcard(iii[0],columns)
        #            keepgoing = False
        #            allplays[2] +=1
        #            break

        if sideblank:
            if keepgoing:
                maxbelow = -1
                sidenow = False
                for iii in sides:
                    if iii[1]>maxbelow:
                        doside = iii
                        maxbelow = iii[1]
                        sidenow = True

                if sidenow:
                    columns = movecards(doside[0],doside[4],columns)
                    columns = flipcard(doside[0],columns)
                    keepgoing = False
                    sideblank = False
                    allplays[5] +=1
        if topcover:
            if keepgoing:
                for iii in toptotops:
                    if iii[1] or iii[0]:
                        thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                        keepgoing = False
                        topcover = False
                        allplays[4] +=1
                        break
        if downking:
            if keepgoing:
                for iii in downs:
                    if iii[2]:
                        columns,thedeck,i = downfromdeal(iii[0],columns,thedeck,i)
                        columns[iii[0]][len(columns[iii[0]])-1].append(1)
                        keepgoing = False
                        downking = False
                        allplays[6] +=1
                        break
        if downother:
            if keepgoing:
                for iii in downs:
                    columns,thedeck,i = downfromdeal(iii[0],columns,thedeck,i)
                    columns[iii[0]][len(columns[iii[0]])-1].append(1)
                    keepgoing = False
                    downother = False
                    allplays[7] +=1
                    break
        if upother:
            if keepgoing:
                for iii in ups:
                    columns, toprow = uptotop(iii[0],columns,toprow)
                    columns = flipcard(iii[0],columns)
                    keepgoing = False
                    upother = False
                    allplays[8] +=1
                    break
        if topother:
            if keepgoing:
                for iii in toptotops:
                    thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                    keepgoing = False
                    topother = False
                    allplays[9] +=1
                    break
        if keepgoing:
            counter += 1
            i = deal(i,thedeck)
        else:
            counter = 0
        if counter > 25:
            if not sideblank:
                sideblank = True
            elif not topcover:
                topcover = True
            elif not downking:
                downking = True
            elif not downother:
                downother = True
            elif not upother:
                upother = True
            elif not topother:
                topother = True
            else:
                allplays[10] += len(ups)
                allplays[11] += len(downs)
                allplays[10] += len(sides)
                allplays[11] += len(toptotops)
                ncardsup.append(toprow)
                break




    ups = getups(columns,toprow)
    sides = getsides(columns)
    downs = getdowns(columns,thedeck,i)
    toptotops = gettoptotops(columns,thedeck,i,toprow)
    if 3>4:
        if len(thedeck)>0:
            dispcolumns(columns,toprow, thedeck[i])
            print ups
            print downs
            print sides
            print toptotops
        else:
            dispcolumns(columns,toprow, [])
            print ups
            print downs
            print sides
            print toptotops
    return ncardsup, columns, toprow, thedeck, i, allplays
    


def playdumbgame(thedeck,toprow,columns,i,counter,ncardsup):
    for iiii in range(0,10000):

        moved = True
        while moved:
            moved = False

            #Move cards to the top
            moved2 = True
            while moved2:
                moved2 = False
                moved1 = True
                while moved1:
                    moved1 = False
                    moved0 = True
                    while moved0:
                        moved0 = False
                        for ii in range(0,7):
                            if len(columns[ii])>0:
                                if columns[ii][len(columns[ii])-1][0]==toprow[columns[ii][len(columns[ii])-1][1]]+1:
                                    columns, toprow = uptotop(ii,columns,toprow)
                                    columns = flipcard(ii,columns)
                                    #dispcolumns(columns,toprow, thedeck[i])
                                    moved = True
                                    moved0 = True
                                    moved1 = True
                                    moved2 = True
                                    break
            
                    #Move cards amongst columns
                    for ii in range(0,7):
                        maxi = 0
                        for iii in range(0,len(columns[ii])):
                            if columns[ii][iii][2]==0:
                                maxi = maxi+1
                        for iii in range(0,7):
                            if len(columns[ii])>0 and len(columns[iii])>0:
                                if columns[ii][maxi][0]==columns[iii][len(columns[iii])-1][0]-1:
                                    if columns[ii][maxi][1]%2!=columns[iii][len(columns[iii])-1][1]%2:
                                        columns = movecards(ii,iii,columns)
                                        columns = flipcard(ii,columns)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved = True
                                        moved1 = True
                                        moved2 = True
                                        break

                #Move kings to blank columns
                for ii in range(0,7):
                    maxi = 0
                    for iii in range(0,len(columns[ii])):
                        if columns[ii][iii][2]==0:
                            maxi = maxi+1
                    if maxi>0:
                        if columns[ii][maxi][0]==13:
                            for iii in range(0,7):
                                if len(columns[iii])==0:
                                    columns = movecards(ii,iii,columns)
                                    columns = flipcard(ii,columns)
                                    #dispcolumns(columns,toprow, thedeck[i])
                                    moved = True
                                    moved2 = True
                                    break

            #Move card from deck to columns or top row
            if len(thedeck)>0:
                if toprow[thedeck[i][1]]==thedeck[i][0]-1:
                    #dispcolumns(columns,toprow, thedeck[i])
                    thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                    #dispcolumns(columns,toprow, thedeck[i])
                    moved=True
                else:
                    for ii in range(0,7):
                        if len(columns[ii])>0:
                            if thedeck[i][0]==columns[ii][len(columns[ii])-1][0]-1:
                                if thedeck[i][1]%2!=columns[ii][len(columns[ii])-1][1]%2:
                                    columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                    columns[ii][len(columns[ii])-1].append(1)
                                    #dispcolumns(columns,toprow, thedeck[i])
                                    moved=True
                                    break
                        else:
                            if thedeck[i][0]==13:
                                columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                columns[ii][0].append(1)
                                #dispcolumns(columns,toprow, thedeck[i])
                                moved=True
                                break




            if moved:
                counter = 0
            else:
                counter+=1
        if counter > 25:
            ncardsup.append(toprow)
            break
        else:
            i = deal(i,thedeck)
            #dispcolumns(columns,toprow, thedeck[i])
    return ncardsup, columns, toprow, thedeck, i
    
def playsmartgame(thedeck,toprow,columns,i,counter,ncardsup,strategy):
    movenonking = False
    moveallup = False
    clearall = False
    dropfirst = False
    for iiii in range(0,100000):
        ups = []
        sides = []
        downs = []
        deals = []
        toptotops = []


        moved = True
        while moved:
            moved = False

            
            moved2 = True
            while moved2:
                moved2 = False
                moved1 = True
                while moved1:
                    moved1 = False
                    moved0 = True
                    while moved0:
                        moved0 = False
                        #Move cards to the top
                        for ii in range(0,7):
                            if len(columns[ii])>0:
                                maxi = 0
                                for iii in range(0,len(columns[ii])):
                                    if columns[ii][iii][2]==0:
                                        maxi = maxi+1
                                if columns[ii][len(columns[ii])-1][0]==toprow[columns[ii][len(columns[ii])-1][1]]+1:
                                    if strategy[1]==1:
                                        if columns[ii][len(columns[ii])-1][1] in [0,2]:
                                            if toprow[1]>columns[ii][len(columns[ii])-1][0]-3 and toprow[3]>columns[ii][len(columns[ii])-1][0]-3:
                                                columns, toprow = uptotop(ii,columns,toprow)
                                                columns = flipcard(ii,columns)
                                                #dispcolumns(columns,toprow, thedeck[i])
                                                moved = True
                                                moved0 = True
                                                moved1 = True
                                                moved2 = True
                                                break
                                            elif len(columns[ii])==maxi+1:
                                                columns, toprow = uptotop(ii,columns,toprow)
                                                columns = flipcard(ii,columns)
                                                #dispcolumns(columns,toprow, thedeck[i])
                                                moved = True
                                                moved0 = True
                                                moved1 = True
                                                moved2 = True
                                                break
                                            elif moveallup:
                                                columns, toprow = uptotop(ii,columns,toprow)
                                                columns = flipcard(ii,columns)
                                                #dispcolumns(columns,toprow, thedeck[i])
                                                moved = True
                                                moved0 = True
                                                moved1 = True
                                                moved2 = True
                                                moveallup = False
                                                break
                                        elif columns[ii][len(columns[ii])-1][1] in [1,3]:
                                            if toprow[0]>columns[ii][len(columns[ii])-1][0]-3 and toprow[2]>columns[ii][len(columns[ii])-1][0]-3:
                                                columns, toprow = uptotop(ii,columns,toprow)
                                                columns = flipcard(ii,columns)
                                                #dispcolumns(columns,toprow, thedeck[i])
                                                moved = True
                                                moved0 = True
                                                moved1 = True
                                                moved2 = True
                                                break
                                            elif len(columns[ii])==maxi+1:
                                                columns, toprow = uptotop(ii,columns,toprow)
                                                columns = flipcard(ii,columns)
                                                #dispcolumns(columns,toprow, thedeck[i])
                                                moved = True
                                                moved0 = True
                                                moved1 = True
                                                moved2 = True
                                                break
                                            elif moveallup:
                                                columns, toprow = uptotop(ii,columns,toprow)
                                                columns = flipcard(ii,columns)
                                                #dispcolumns(columns,toprow, thedeck[i])
                                                moved = True
                                                moved0 = True
                                                moved1 = True
                                                moved2 = True
                                                moveallup = False
                                                break
                                    else:
                                        columns, toprow = uptotop(ii,columns,toprow)
                                        columns = flipcard(ii,columns)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved = True
                                        moved0 = True
                                        moved1 = True
                                        moved2 = True
                                        break
            
                    #Move cards amongst columns
                    for ii in range(0,7):
                        maxi = 0
                        for iii in range(0,len(columns[ii])):
                            if columns[ii][iii][2]==0:
                                maxi = maxi+1
                        if strategy[2]==1:
                            if maxi>0:
                                for iii in range(0,7):
                                    if len(columns[ii])>0 and len(columns[iii])>0:
                                        if columns[ii][maxi][0]==columns[iii][len(columns[iii])-1][0]-1:
                                            if columns[ii][maxi][1]%2!=columns[iii][len(columns[iii])-1][1]%2:
                                                columns = movecards(ii,iii,columns)
                                                columns = flipcard(ii,columns)
                                                #dispcolumns(columns,toprow, thedeck[i])
                                                moved = True
                                                moved1 = True
                                                moved2 = True
                                                break
                            else:
                                if clearall:
                                    for iii in range(0,7):
                                        if len(columns[ii])>0 and len(columns[iii])>0:
                                            if columns[ii][maxi][0]==columns[iii][len(columns[iii])-1][0]-1:
                                                if columns[ii][maxi][1]%2!=columns[iii][len(columns[iii])-1][1]%2:
                                                    columns = movecards(ii,iii,columns)
                                                    columns = flipcard(ii,columns)
                                                    #dispcolumns(columns,toprow, thedeck[i])
                                                    moved = True
                                                    moved1 = True
                                                    moved2 = True
                                                    clearall = False
                                                    break
                                else:
                                    for iiii in range(0,7):
                                        maxu = 0
                                        for iii in range(0,len(columns[iiii])):
                                            if columns[iiii][iii][2]==0:
                                                maxu = maxu+1
                                        if len(columns[iiii])>0:
                                            if columns[iiii][maxu][0]==13:
                                                for iii in range(0,7):
                                                    if len(columns[ii])>0 and len(columns[iii])>0:
                                                        if columns[ii][maxi][0]==columns[iii][len(columns[iii])-1][0]-1:
                                                            if columns[ii][maxi][1]%2!=columns[iii][len(columns[iii])-1][1]%2:
                                                                columns = movecards(ii,iii,columns)
                                                                columns = flipcard(ii,columns)
                                                                #dispcolumns(columns,toprow, thedeck[i])
                                                                moved = True
                                                                moved1 = True
                                                                moved2 = True
                                                                break

                        else:
                            for iii in range(0,7):
                                if len(columns[ii])>0 and len(columns[iii])>0:
                                    if columns[ii][maxi][0]==columns[iii][len(columns[iii])-1][0]-1:
                                        if columns[ii][maxi][1]%2!=columns[iii][len(columns[iii])-1][1]%2:
                                            columns = movecards(ii,iii,columns)
                                            columns = flipcard(ii,columns)
                                            #dispcolumns(columns,toprow, thedeck[i])
                                            moved = True
                                            moved1 = True
                                            moved2 = True
                                            break

                #Move kings to blank columns
                for ii in range(0,7):
                    maxi = 0
                    for iii in range(0,len(columns[ii])):
                        if columns[ii][iii][2]==0:
                            maxi = maxi+1
                    if maxi>0:
                        if columns[ii][maxi][0]==13:
                            for iii in range(0,7):
                                if len(columns[iii])==0:
                                    columns = movecards(ii,iii,columns)
                                    columns = flipcard(ii,columns)
                                    #dispcolumns(columns,toprow, thedeck[i])
                                    moved = True
                                    moved2 = True
                                    break
                        if movenonking:
                            if maxi>0:
                                for iii in range(0,7):
                                    if len(columns[iii])==0:
                                        columns = movecards(ii,iii,columns)
                                        columns = flipcard(ii,columns)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved = True
                                        moved2 = True
                                        movenonking = False
                                        break

            #Move card from deck to columns or top row
            if len(thedeck)>0:
                if toprow[thedeck[i][1]]==thedeck[i][0]-1:
                    if strategy[1]==1:
                        if strategy[3]==1:
                            if deckfreescard('up',columns,thedeck,i):
                                if thedeck[i][1] in [0,2]:
                                    if toprow[1]>thedeck[i][0]-2 and toprow[3]>thedeck[i][0]-2:
                                        thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved=True
                                    elif moveallup:
                                        thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moveallup = False
                                        moved=True
                                elif thedeck[i][1] in [1,3]:
                                    if toprow[0]>thedeck[i][0]-2 and toprow[2]>thedeck[i][0]-2:
                                        thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved=True
                                    elif moveallup:
                                        thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moveallup = False
                                        moved=True
                            elif dropfirst:
                                if thedeck[i][1] in [0,2]:
                                    if toprow[1]>thedeck[i][0]-2 and toprow[3]>thedeck[i][0]-2:
                                        thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved=True
                                        dropfirst = False
                                    elif moveallup:
                                        thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moveallup = False
                                        dropfirst = False
                                        moved=True
                                elif thedeck[i][1] in [1,3]:
                                    if toprow[0]>thedeck[i][0]-2 and toprow[2]>thedeck[i][0]-2:
                                        thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved=True
                                        dropfirst = False
                                    elif moveallup:
                                        thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moveallup = False
                                        dropfirst = False
                                        moved=True

                        else:
                            if thedeck[i][1] in [0,2]:
                                if toprow[1]>thedeck[i][0]-2 and toprow[3]>thedeck[i][0]-2:
                                    thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                    #dispcolumns(columns,toprow, thedeck[i])
                                    moved=True
                                elif moveallup:
                                    thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                    #dispcolumns(columns,toprow, thedeck[i])
                                    moveallup = False
                                    moved=True
                            elif thedeck[i][1] in [1,3]:
                                if toprow[0]>thedeck[i][0]-2 and toprow[2]>thedeck[i][0]-2:
                                    thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                    #dispcolumns(columns,toprow, thedeck[i])
                                    moved=True
                                elif moveallup:
                                    thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                                    #dispcolumns(columns,toprow, thedeck[i])
                                    moveallup = False
                                    moved=True

                    else:
                        #dispcolumns(columns,toprow, thedeck[i])
                        thedeck,toprow,i =upfromdeal(thedeck,toprow,i)
                        #dispcolumns(columns,toprow, thedeck[i])
                        moved=True
                else:
                    for ii in range(0,7):
                        if len(columns[ii])>0:
                            if thedeck[i][0]==columns[ii][len(columns[ii])-1][0]-1:
                                if thedeck[i][1]%2!=columns[ii][len(columns[ii])-1][1]%2:
                                    if strategy[3]==1:
                                        if deckfreescard('down',columns,thedeck,i):
                                            columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                            columns[ii][len(columns[ii])-1].append(1)
                                            #dispcolumns(columns,toprow, thedeck[i])
                                            moved=True
                                            break
                                        elif dropfirst:
                                            columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                            columns[ii][len(columns[ii])-1].append(1)
                                            #dispcolumns(columns,toprow, thedeck[i])
                                            moved=True
                                            dropfirst = False
                                            break
                                    else:
                                        columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                        columns[ii][len(columns[ii])-1].append(1)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved=True
                                        break
                        else:
                            if thedeck[i][0]==13:
                                if strategy[3]==1:
                                    if deckfreescard('down',columns,thedeck,i):
                                        columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                        columns[ii][0].append(1)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved=True
                                        break
                                    elif dropfirst:
                                        columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                        columns[ii][0].append(1)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved=True
                                        dropfirst = False
                                        break
                                else:
                                    columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                    columns[ii][0].append(1)
                                    #dispcolumns(columns,toprow, thedeck[i])
                                    moved=True
                                    break
                            elif movenonking:
                                if strategy[3]==1:
                                    if deckfreescard('down',columns,thedeck,i):
                                        columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                        columns[ii][0].append(1)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved=True
                                        movenonking = False
                                        break
                                    elif dropfirst:
                                        columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                        columns[ii][0].append(1)
                                        #dispcolumns(columns,toprow, thedeck[i])
                                        moved=True
                                        dropfirst = False
                                        movenonking = False
                                        break
                                else:
                                    columns,thedeck,i = downfromdeal(ii,columns,thedeck,i)
                                    columns[ii][0].append(1)
                                    #dispcolumns(columns,toprow, thedeck[i])
                                    moved=True
                                    movenonking = False
                                    break




            if moved:
                counter = 0
            else:
                counter+=1
        if counter > 25:
            
            if strategy[0]==1 and movenonking==False:
                movenonking = True
                counter = 0
            elif strategy[1]==1 and moveallup==False:
                moveallup = True
                counter = 0
            elif strategy[2]==1 and clearall==False:
                clearall = True
                counter = 0
            elif strategy[3]==1 and dropfirst==False:
                dropfirst = True
                counter = 0
            else:
                ncardsup.append(toprow)
                break

        else:
            i = deal(i,thedeck)
            #dispcolumns(columns,toprow, thedeck[i])
    return ncardsup, columns, toprow, thedeck, i

ncardsup = []

for i in range(0,100):
    thedeck,toprow,columns,i,counter = creategame()    
    #dispcolumns(columns,toprow, thedeck[i])
    ncardsup, columns, toprow, thedeck, i = playdumbgame(thedeck,toprow,columns,i,counter,ncardsup)  
    #if len(thedeck)>0:
    #    dispcolumns(columns,toprow, thedeck[i])
    #else:
    #    dispcolumns(columns,toprow, [])
#print ncardsup
payout = 0
payin = 0
for game in ncardsup:
    payout += .05*(game[0]+game[1]+game[2]+game[3])
    payin += 1.35
print payout, payin

ncardsup = []

for i in range(0,100):
    thedeck,toprow,columns,i,counter = creategame()    
    #dispcolumns(columns,toprow, thedeck[i])
    ncardsup, columns, toprow, thedeck, i = playsmartgame(thedeck,toprow,columns,i,counter,ncardsup,[1,1,1,1])  
    #if len(thedeck)>0:
    #    dispcolumns(columns,toprow, thedeck[i])
    #else:
    #    dispcolumns(columns,toprow, [])
#print ncardsup
payout = 0
payin = 0
for game in ncardsup:
    payout += .05*(game[0]+game[1]+game[2]+game[3])
    payin += 1.35
print payout, payin

ncardsup = []
allplays = [0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(0,1000):
    thedeck,toprow,columns,i,counter = creategame()  
    
    #dispcolumns(columns,toprow, thedeck[i])
    ncardsup, columns, toprow, thedeck, i, allplays = playsmart(thedeck,toprow,columns,i,counter,ncardsup,allplays)  
    #if len(thedeck)>0:
    #    dispcolumns(columns,toprow, thedeck[i])
    #else:
    #    dispcolumns(columns,toprow, [])
#print ncardsup
payout = 0
payin = 0
for game in ncardsup:
    payout += .05*(game[0]+game[1]+game[2]+game[3])
    payin += 1.35
print payout, payin
print allplays
