def sagetoreddittable(myrows, myheader):
    tablestr = ""
    for i in myheader[0:len(myheader)-1]:
        tablestr=tablestr+str(i)+" | "
    tablestr=tablestr+str(myheader[len(myheader)-1])+"\n"
    for i in range(len(myheader)-1):
        tablestr=tablestr+":--: | "
    tablestr=tablestr+":--:\n"
    for ii in range(len(myrows)):
        for i in myrows[ii][0:len(myrows[ii])-1]:
            tablestr=tablestr+str(i)+" | "
        tablestr=tablestr+str(myrows[ii][len(myrows[ii])-1])+"\n"
    return tablestr 
def sagetoredditlist(mylist, mytitle):
    print mytitle
    for i in mylist:
        print "1. ", i
