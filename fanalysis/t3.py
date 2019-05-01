import re

def input_to_string():
	def replace_all(text, dic):
		for i, j in dic.items():
			text = text.replace(i, j)
		return text

	#add space for string split
	if "input('" in str:
		if "input(' " in str:
			pass
		else:
			str.replace("input('", "input(' ")

	print(str)
	x = str.split()
	print(x)

	def match_text(text, firstoccuranceonly = False):
		match = (a for a, r in enumerate(x) if text in r)
		if firstoccuranceonly ==False:
			matches = []
			matches = list(match)
			return matches
		else: 
			return(next(match))

	match_input = match_text("input", True)
	match_sym = match_text("{}")
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
			print(y)
	y=' '.join(y)
	str="'"+y+"'"
	print(str)
	return str


a='5'
freq="freq"
str =  "p = input('How many {} would you like to {} generate? '.format(freq, a))"

if __name__=='__main__':
	ps = 'p = input('+str+')'
	print(ps)
	exec(ps)
