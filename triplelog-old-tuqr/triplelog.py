from sage.all import *
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
def towikitable(header,rows, maxshow, roundrules=[[],[]]):
	tablestr = "{|class ='wikitable sortable'\n|-\n"
	for i in header:
		tablestr = tablestr+"! "+str(i)+"\n"
	for i in rows:
		tablestr = tablestr+"|-\n"
		for idx,ii in enumerate(i):
			if idx in roundrules[0]:
				mstr = "%."+str(roundrules[1][roundrules[0].index(idx)])+"f"
				ii = mstr % ii
				tablestr=tablestr+"| "+ii+"\n"
			else:
				tablestr=tablestr+"| "+str(ii)+"\n"
			
	tablestr = tablestr+"|}"
	return tablestr
	

def tohtmltable(header,rows, roundrules=[[],[]]):
	numbercols = []
	for idx,i in enumerate(rows[0]):
		if is_number(i):
			numbercols.append(idx)
	mystr = '<table class="dyna" id="my-table"><thead><tr>'
	for idx, i in enumerate(header):
		if idx in numbercols:
			if idx in roundrules[0]:
				mystr=mystr+'<th dround="'+str(roundrules[1][roundrules[0].index(idx)])+'" align="right">'+str(i)+'</th>'
			else:
				mystr=mystr+'<th align="right">'+str(i)+'</th>'
		else:
			mystr=mystr+'<th align="left">'+str(i)+'</th>'
	mystr=mystr+'</tr></thead><tbody>'
	for idx, i in enumerate(rows):
		mystr=mystr+'<tr>'
		for iidx, ii in enumerate(i):
			mystr=mystr+'<td>'+str(ii)+'</td>'
		mystr=mystr+'</tr>'
	if len(numbercols)==0:
		mystr=mystr+'</tbody></table>'
	else:
		mystr=mystr+'</tbody></table>|col='
		for idx, i in enumerate(numbercols):
			if is_number(str(header[i])[0]):
				mystr = mystr+str(header[i])
			else:
				mystr = mystr+header[i].lower()
			if idx < len(numbercols)-1:
				mystr=mystr+'|'
	return html(mystr)
def toreddittable(header,rows,maxshow=20, roundrules=[[],[]]):
	tablestr = ""
	for i in header[0:len(header)-1]:
		tablestr=tablestr+str(i)+" | "
	tablestr=tablestr+str(header[len(header)-1])+"\n"
	for i in range(len(header)-1):
		if is_number(rows[0][i]):
			tablestr=tablestr+"--: | "
		else:
			tablestr=tablestr+":-- | "
	if is_number(rows[0][len(rows[0])-1]):
		tablestr=tablestr+"--: \n"
	else:
		tablestr=tablestr+":-- \n"
	for ii in range(min(maxshow,len(rows))):
		for idx,i in enumerate(rows[ii][0:len(rows[ii])-1]):
			if idx in roundrules[0]:
				mstr = "%."+str(roundrules[1][roundrules[0].index(idx)])+"f"
				i = mstr % i
				tablestr=tablestr+i+" | "
			else:
				tablestr=tablestr+str(i)+" | "
		if len(rows[ii])-1 in roundrules[0]:
			mstr = "%."+str(roundrules[1][roundrules[0].index(len(rows[ii])-1)])+"f"
			i = mstr % rows[ii][len(rows[ii])-1]
			tablestr=tablestr+i+"\n"
		else:
			tablestr=tablestr+str(rows[ii][len(rows[ii])-1])+"\n"
	tablestr=tablestr+'Created with [Triple Log](http://triplelog.com "Learn how to make this and much more")\n'
	return tablestr 
def toredditlist(mylist, mytitle=""):
	if mytitle != "":
		mystr = "##"+mytitle+"\n\n"
	else:
		mystr = ""
	for idx,i in enumerate(mylist):
		mystr=mystr+ str(idx+1)+". "+ str(i) +"\n"
	return mystr
def maketable(header,rows,tabletype='Python',maxshow=25,roundrules=[[],[]]):
	if tabletype=='Html':
		mytable = tohtmltable(header,rows,roundrules)
	elif tabletype=='Reddit':
		mytable = toreddittable(header,rows,maxshow,roundrules)
	elif tabletype=='Wiki':
		mytable = towikitable(header,rows,maxshow,roundrules)
	else:
		x = maxshow-1
		mytable = table(rows[0:x],header_row=header)
	return mytable
