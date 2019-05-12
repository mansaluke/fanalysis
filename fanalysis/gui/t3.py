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

	x = str.split()
	
	
	def match_text(text, firstoccuranceonly = False):
		match = (a for a, r in enumerate(x) if text in r)
		if firstoccuranceonly ==False:
			matches = []
			matches = list(match)
			return matches
		else: 
			return(next(match))

	match_input = match_text(str_replace.replace("('", ""), True)

	if ".format" in str:
		match_format = match_text(".format", True)

		y=[]
		for i in x[match_input+1:match_format]:
  		  y.append(i)

		#if i == x[match_format]:
		#	new_word = i.replace(".format", "")

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

	else:
		y=[]
		for i in x[match_input+1:]:
  		  y.append(i)			
		return str





def getsourcelines(object):
	"""from inspect module
	Return a list of source lines and starting line number for an object.	
	The argument may be a module, class, method, function, traceback, frame,
	or code object.  The source code is returned as a list of the lines
	corresponding to the object and the line number indicates where in the
	original source file the first line of code was found.  An OSError is
	raised if the source code cannot be retrieved."""
	import inspect as i
	object = i.unwrap(object)
	lines, lnum = i.findsource(object)	
	if i.ismodule(object):
	    return lines, 0
	else:
		#return False
	    return i.getblock(lines[lnum:]), lnum + 1

if __name__=='__main__':
	#a='(random stuff hahaha) '
	#freq="days"
	#print('How many {} would you like to {} generate? '.format(freq, a))
	#str =  "p = print('How many {} would you like to {} generate? '.format(freq, a))"
	#str = input_to_string(str)
	#ps = 'input('+str+')'
	##exec(ps)
	#x = eval(ps)
	#print(x)
	import inspect as i
	import t2
	x=1
	print(getsourcelines(t2.func_adj.do))
	
	#getclasstree
	