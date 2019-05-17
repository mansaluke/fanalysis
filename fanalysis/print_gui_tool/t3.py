import inspect as i

def print_convert(str_input):
	"""
	removes "input"/"string" elements from string and replaces .format part with 
	corresponding variables
	"""
	if "print" in str_input or "input" in str_input:
		if "print" in str_input:
			str_replace = "print('"
		if "input" in str_input:
			str_replace = "input('"	
	else:
		raise ValueError('Can only enter strings containing "print" or "input"')
	
	def replace_all(text, dic):
		for i, j in dic.items():
			text = text.replace(i, j)
		return text

	#add space for correct string split
	if str_replace in str_input:
		if str_replace + ' ' in str_input:
			pass
		else:
			str_input = str_input.replace(str_replace, str_replace + ' ')


	def match_text(str_input, to_match, firstoccuranceonly = False):
		"""
		finds position of to_match in string.
		if len(to_match)>1 => enter str.split()
		"""
		match = (a for a, r in enumerate(str_input) if to_match in r)
		if firstoccuranceonly ==False:
			matches = []
			matches = list(match)
			return matches
		else: 
			return(next(match))
	
	str_split = str_input.split()

	#easier to search ( instead of ' or "
	match_sym1 = match_text(str_input,"(", True)
	match_sym2 = match_text(str_input,")", True)
	match_sym3 = match_text(str_split,"(", True)
	
	if ".format" in str_input:	
		match_format = match_text(str_split,".format", True)
		y=[]
		for i in str_split[match_sym3+1:match_format]:
  		  y.append(i)

		vars= ''.join(str_split[match_format:])
		vars= replace_all(vars, {"'.format(":"",")":""})
		vars= list(vars.split(","))
		vars= ["'+{}+'".format(v) for v in vars]
		c=0
		for n, i in enumerate(y):
			if i == '{}':
				y[n] = vars[c]
				c+=1
		y=' '.join(y)
		str_input="'"+y+"'"
		return str_input

	else:
		y=[]
		for i in str_input[match_sym1+2:match_sym2-1]:
  		  y.append(i)	
		y=''.join(y)
		str_input="'"+y+"'"
		return str_input





#def getsourcelines(object):
#	"""from inspect module
#	Return a list of source lines and starting line number for an object.	
#	The argument may be a module, class, method, function, traceback, frame,
#	or code object.  The source code is returned as a list of the lines
#	corresponding to the object and the line number indicates where in the
#	original source file the first line of code was found.  An OSError is
#	raised if the source code cannot be retrieved."""
#	import inspect as i
#	object = i.unwrap(object)
#	lines, lnum = i.findsource(object)	
#	if i.ismodule(object):
#	    return lines, 0
#	else:
#		#return False
#	    return i.getblock(lines[lnum:]), lnum + 1



def input_to_string(fn):
	fn_str = i.getsourcelines(fn)[0]
	#fn_str = '\n'.join(map(str, fn_str))
	for line in range(len(fn_str)):
		if "print(" in fn_str[line] or "input(" in fn_str[line]:
			if "print" in fn_str[line]:
				fn_str[line] = "print" + str(line) + "=" + print_convert(fn_str[line])
			if "input" in fn_str[line]:
				fn_str[line] = "input" + str(line) + "=" + print_convert(fn_str[line])
	return fn_str



if __name__=='__main__':
	#a='(random stuff hahaha) '
	#freq="days"
	#print('How many {} would you like to {} generate? '.format(freq, a))
	#str =  "p = print('How many {} would you like to {} generate? '.format(freq, a))"
	#str = print_convert(str)
	#ps = 'input('+str+')'
	#exec(ps)
	#x = eval(ps)
	#print(x)
	
	import appgui
	fn = input_to_string(appgui.foo)
	print(fn)
	str = 'print("hi")'
	str = print_convert(str)
	print(str)
