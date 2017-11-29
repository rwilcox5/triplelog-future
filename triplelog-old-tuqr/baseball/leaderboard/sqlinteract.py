@interact
def _(age=range_slider(15,30,1,default=(20,25))):
	limit = 25
	mystr = 'SELECT * FROM batters WHERE year-yearob <= '+str(age[1])+' AND year-yearob>= '+str(age[0])+' SORT BY hr DESC LIMIT '+str(limit)
	print mystr