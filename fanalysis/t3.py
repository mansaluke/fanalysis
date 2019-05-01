def input_to_string(str):
	"""
	removes "input"/"string" elements from string and replaces .format part with 
	corresponding variables
	"""
	if "print" in str or "input" in str:
		if "print" in str:
			str_replace = "print('"
		if "input" in str:
			str_replace = "input('"	
	else:
		raise ValueError('Can only enter strings containing "print" or "input"')
	
	def replace_all(text, dic):
		for i, j in dic.items():
			text = text.replace(i, j)
		return text

	#add space for correct string split
	if str_replace in str:
		if str_replace + ' ' in str:
			print(str_replace + ' ')
			pass
		else:
			str = str.replace(str_replace, str_replace + ' ')

	#print(str)
	x = str.split()
	#print(x)

	def match_text(text, firstoccuranceonly = False):
		match = (a for a, r in enumerate(x) if text in r)
		if firstoccuranceonly ==False:
			matches = []
			matches = list(match)
			return matches
		else: 
			return(next(match))


	match_input = match_text(str_replace.replace("('", ""), True)
	match_format = match_text(".format", True)

	y=[]
	for i in x[match_input+1:match_format]:
  	  y.append(i)

	if i == x[match_format]:
		new_word = i.replace(".format", "")

	vars = x[match_format:]
	vars= ''.join(vars)
	vars=replace_all(vars, {"'.format(":"",")":""})
	vars=list(vars.split(","))
	vars = ["'+{}+'".format(v) for v in vars]

	c=0
	for n, i in enumerate(y):
		if i == '{}':
			y[n] = vars[c]
			c+=1
	y=' '.join(y)
	str="'"+y+"'"
	return str



if __name__=='__main__':
	a='(random stuff hahaha) '
	freq="days"
	str =  "p = print('How many {} would you like to {} generate? '.format(freq, a))"
	str = input_to_string(str)
	ps = 'input('+str+')'
	#exec(ps)
	x = eval(ps)
	print(x)
