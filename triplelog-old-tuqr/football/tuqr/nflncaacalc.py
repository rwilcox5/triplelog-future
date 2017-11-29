def calcnflqbrating(x):
    completions = x[0]
    attempts = float(x[1])
    yards = x[2]
    touchdowns = x[3]
    interceptions = x[4]
    if attempts>0:
        completionpercentage = completions/attempts*100
        ypa = yards/attempts
        tdpa = touchdowns/attempts*100
        intpa = interceptions/attempts*100
        if completionpercentage > .30:
            if completionpercentage < .775:
                cppoints = (completionpercentage-30)*.05
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
        if tdpa > 11.875:
            tdpoints = 2.375
        else:
            tdpoints = tdpa*.2
        if intpa > 9.5:
            intpoints = 0
        else:
            intpoints = 2.375-.25*intpa
    else:
        cppoints = 0
        ypapoints = 0
        tdpoints = 0
        intpoints = 0
    return cppoints, ypapoints, tdpoints, intpoints, (cppoints+ ypapoints+ tdpoints+ intpoints)*100./6
def calcncaaqbrating(x):
    completions = x[0]
    attempts = float(x[1])
    yards = x[2]
    touchdowns = x[3]
    interceptions = x[4]
    if attempts>0:
        cppoints = completions/attempts*100
        ypapoints = yards/attempts
        tdpoints = touchdowns/attempts*100
        intpoints = interceptions/attempts*100
    else:
        cppoints = 0
        ypapoints = 0
        tdpoints = 0
        intpoints = 0
    return cppoints, ypapoints, tdpoints, intpoints, cppoints+ 8.4*ypapoints+ 3.3*tdpoints-2*intpoints


@interact
def _(Completions=slider(0,100,1,default=10),Attempts=slider(0,100,1,default=10),Yards=slider(0,1000,1,default=200),TDs=slider(0,10,1,default=1),INTs=slider(0,10,1,default=0)):
    stats = [Completions,Attempts,Yards,TDs,INTs]
    print "NFL: ",round(calcnflqbrating(stats)[4],2)
    print "NCAA: ",round(calcncaaqbrating(stats)[4],2)

