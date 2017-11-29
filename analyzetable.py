table_str = "<tr><td>Arizona</td><td>Baltimore</td><td>Chicago</td><td>Detroit</td><td>5.44%</td><td>64.0%</td><td>64.0%</td></tr>            <tr><td>Arizona</td><td>Baltimore</td><td>Detroit</td><td>Chicago</td><td>4.08%</td><td>70.3%</td><td>57.1%</td></tr>            <tr><td>Arizona</td><td>Chicago</td><td>Baltimore</td><td>Detroit</td><td>6.82%</td><td>57.1%</td><td>57.1%</td></tr>            <tr><td>Arizona</td><td>Chicago</td><td>Detroit</td><td>Baltimore</td><td>6.69%</td><td>57.1%</td><td>42.9%</td></tr>            <tr><td>Arizona</td><td>Detroit</td><td>Baltimore</td><td>Chicago</td><td>3.84%</td><td>70.3%</td><td>42.9%</td></tr>            <tr><td>Arizona</td><td>Detroit</td><td>Chicago</td><td>Baltimore</td><td>5.03%</td><td>64.0%</td><td>36.0%</td></tr>            <tr><td>Baltimore</td><td>Arizona</td><td>Chicago</td><td>Detroit</td><td>4.08%</td><td>57.1%</td><td>70.3%</td></tr>            <tr><td>Baltimore</td><td>Arizona</td><td>Detroit</td><td>Chicago</td><td>3.07%</td><td>64.0%</td><td>64.0%</td></tr>            <tr><td>Baltimore</td><td>Chicago</td><td>Arizona</td><td>Detroit</td><td>3.84%</td><td>42.9%</td><td>70.3%</td></tr>            <tr><td>Baltimore</td><td>Chicago</td><td>Detroit</td><td>Arizona</td><td>2.83%</td><td>36.0%</td><td>64.0%</td></tr>            <tr><td>Baltimore</td><td>Detroit</td><td>Arizona</td><td>Chicago</td><td>2.16%</td><td>57.1%</td><td>57.1%</td></tr>            <tr><td>Baltimore</td><td>Detroit</td><td>Chicago</td><td>Arizona</td><td>2.13%</td><td>42.9%</td><td>57.1%</td></tr>            <tr><td>Chicago</td><td>Arizona</td><td>Baltimore</td><td>Detroit</td><td>6.69%</td><td>42.9%</td><td>57.1%</td></tr>            <tr><td>Chicago</td><td>Arizona</td><td>Detroit</td><td>Baltimore</td><td>6.82%</td><td>42.9%</td><td>42.9%</td></tr>            <tr><td>Chicago</td><td>Baltimore</td><td>Arizona</td><td>Detroit</td><td>5.03%</td><td>36.0%</td><td>64.0%</td></tr>            <tr><td>Chicago</td><td>Baltimore</td><td>Detroit</td><td>Arizona</td><td>3.84%</td><td>29.7%</td><td>57.1%</td></tr>            <tr><td>Chicago</td><td>Detroit</td><td>Arizona</td><td>Baltimore</td><td>5.44%</td><td>36.0%</td><td>36.0%</td></tr>            <tr><td>Chicago</td><td>Detroit</td><td>Baltimore</td><td>Arizona</td><td>4.08%</td><td>29.7%</td><td>42.9%</td></tr>            <tr><td>Detroit</td><td>Arizona</td><td>Baltimore</td><td>Chicago</td><td>2.83%</td><td>64.0%</td><td>36.0%</td></tr>            <tr><td>Detroit</td><td>Arizona</td><td>Chicago</td><td>Baltimore</td><td>3.84%</td><td>57.1%</td><td>29.7%</td></tr>            <tr><td>Detroit</td><td>Baltimore</td><td>Arizona</td><td>Chicago</td><td>2.13%</td><td>57.1%</td><td>42.9%</td></tr>            <tr><td>Detroit</td><td>Baltimore</td><td>Chicago</td><td>Arizona</td><td>2.16%</td><td>42.9%</td><td>42.9%</td></tr>            <tr><td>Detroit</td><td>Chicago</td><td>Arizona</td><td>Baltimore</td><td>4.08%</td><td>42.9%</td><td>29.7%</td></tr>            <tr><td>Detroit</td><td>Chicago</td><td>Baltimore</td><td>Arizona</td><td>3.07%</td><td>36.0%</td><td>36.0%</td></tr>"

index = 0
allrows = []
for i in range(0,24):
	sindex = table_str.find('<tr>',index)
	eindex = table_str.find('</tr>',index)
	index = eindex+1
	allrows.append(table_str[sindex+4:eindex])

the_table = []
for idx,i in enumerate(allrows):
	index= 0
	allcells = []
	probboth = 1.
	for ii in range(0,7):
		sindex = i.find('<td>',index)
		eindex = i.find('</td>',index)
		index=eindex+1
		if ii >3:
			allcells.append(float(i[sindex+4:eindex-1])/100.)
		if ii > 4:
			probboth = probboth*float(i[sindex+4:eindex-1])/100.
	pboth = '<td>'+str(int(probboth*1000.)/10.)+'%</td>'
	allrows[idx]='<tr>'+i+pboth+'</tr>\n'
	the_table.append(allcells)

for i in allrows:
	print i,

print soto
tsum = 0.
ttsum = 0.
tttsum = 0.
ttttsum = 0.
for i in the_table:
	i[0]=(i[0]-1./24.)*3+1./24.
	i[1]=(i[1]-1./2.)*2+1./2.
	i[2]=(i[2]-1./2.)*2+1./2.
	tsum+=i[0]
	i.append(i[0]*i[1])
	ttsum+=i[0]*i[1]
	tttsum+=i[0]*i[2]
	ttttsum+=i[0]*i[1]*i[2]
	i.append(i[0]*i[2])
	i.append(i[0]*i[1]*i[2])
	print i
print tsum, ttsum, tttsum, ttttsum, 360.*ttttsum


