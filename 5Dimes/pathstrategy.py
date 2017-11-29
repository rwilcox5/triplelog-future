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
def getremovelist(columns, thedeck, toprow,i,card,column,colloc):
	cardstoexpose = [[card[0]+1,(card[1]+1)%2],[card[0]+1,(card[1]+1)%2+2]]
	if len(column)>colloc+1:
		cardtoremove = column[colloc+1]
	else:
		cardtoremove = []
	for ii in range(0,len(thedeck)):
		if thedeck[ii]==cardstoexpose[0]:
			cardstoexpose[0].append(['deck',ii])
		elif thedeck[ii]==cardstoexpose[1]:
			cardstoexpose[1].append(['deck',ii])
		elif len(cardtoremove)>0:
			if thedeck[ii]==cardtoremove[0]:
				cardtoremove[0].append(['deck',ii])
	for ii in range(0,7):
		for iii in range(0,len(columns[ii])):
			if columns[ii][iii][2]==1:
				if columns[ii][iii][0]==cardstoexpose[0][0] and columns[ii][iii][1]==cardstoexpose[0][1]:
					cardstoexpose[0].append(['columns',ii])
				elif columns[ii][iii][0]==cardstoexpose[1][0] and columns[ii][iii][1]==cardstoexpose[1][1]:
					cardstoexpose[1].append(['columns',ii])
				elif len(cardtoremove)>0:
					if columns[ii][iii][0]==cardtoremove[0][0] and columns[ii][iii][1]==cardtoremove[0][1]:
						cardtoremove[0].append(['columns',ii])
	print cardstoexpose,cardtoremove



ncardsup = []

for i in range(0,100):
    thedeck,toprow,columns,i,counter = creategame()    
    dispcolumns(columns,toprow, thedeck[i])
    for ii in range(0,7):
    	getremovelist(columns,thedeck,toprow,i,columns[ii][ii],columns[ii],ii)  