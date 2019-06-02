import inspect as i
import sys
import os


def unwrap_cls(object):
    """
    returns full class code
    e.g.
    class foo_class():
        def foo(self, a, b):
            return a + b
    i._findclass(foo_class.foo)
    """
    if isinstance(i._findclass(object), type) == True:
        return i.getsource(i._findclass(object))
    else:
        raise TypeError(str(object) + "() is not class type")


def unwrap_fn(object):
    """
    returns function code
    def foo(a):
        return a +1
    print(unwrap_fn(foo))
    """
    return i.getsource(object)


def unwrap_all(object):
    """
    returns full function and class code
    if object not function or class none is returned
    """
    if i._findclass(object) is not None:
        return unwrap_cls(object)
    else:
        if i.isfunction(object):
            return unwrap_fn(object)
        else:
            return None


def unwrap_recur(fn):
    """
    finds root code
    while line = fn or class exists
    """
    for line in range(len(fn)):
        try:
            line = eval(fn[line])
            print(fn[line])
            while unwrap_all(fn[line]) is not None:
                fn[line] = unwrap_all(fn[line])
        except:
            pass
    # fn[line] = fn[line]
    return fn


def print_convert(str_input, print_replace="", input_replace=""):
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

	# add space for correct string split
	if str_replace in str_input:
		if str_replace + ' ' in str_input:
			pass
		else:
			str_input = str_input.replace(str_replace, str_replace + ' ')

	def match_text(str_input, to_match, firstoccuranceonly=False):
		"""
		finds position of to_match in string.
		if len(to_match)>1 => enter str.split()
		"""
		match = (a for a, r in enumerate(str_input) if to_match in r)
		if firstoccuranceonly == False:
			matches = []
			matches = list(match)
			return matches
		else:
			return(next(match))

	str_split = str_input.split()

	# easier to search ( instead of ' or "
	match_sym1 = match_text(str_input, "(", True)
	match_sym2 = match_text(str_input, ")", True)
	match_sym3 = match_text(str_split, "(", True)

	if ".format" in str_input:
		match_format = match_text(str_split, ".format", True)
		y = []
		for i in str_split[match_sym3+1:match_format]:
  		  y.append(i)

		vars = ''.join(str_split[match_format:])
		vars = replace_all(vars, {"'.format(": "", ")": ""})
		vars = list(vars.split(","))
		vars = ["'+{}+'".format(v) for v in vars]
		c = 0
		for n, i in enumerate(y):
			if i == '{}':
				y[n] = vars[c]
				c += 1
		y = ' '.join(y)
		str_input = "'"+y+"'"

	else:
		y = []
		for i in str_input[match_sym1+2:match_sym2-1]:
  		  y.append(i)
		y = ''.join(y)
		str_input = "'"+y+"'"

    if str_replace =="print('":
        str_input = print_replace + str_input
    # elif "input('" in str_replace:
    #    str_input = input_replace + str_input
    
    # return str_input





def input_to_string(fn, isfunction = True):
    """
    converts all lines of function
    """
    if isfunction == True:
        fn_str = i.getsourcelines(fn)[0]
        # fn_str = '\n'.join(map(str, fn_str))
        for line in range(len(fn_str)):
            if "print(" in fn_str[line] or "input(" in fn_str[line]:
                if "print" in fn_str[line]:
                    fn_str[line] = "print" + str(line) + "=" + print_convert(fn_str[line])
                if "input" in fn_str[line]:
                    fn_str[line] = "input" + str(line) + "=" + print_convert(fn_str[line])
        return fn_str
    else:
    	if "print(" in fn or "input(" in fn:
    		fn_str = print_convert(fn)
    	else:
    		fn_str = fn
    	return fn_str



class func_adj():
    """
    e.g. 
    converts function or class
    parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if parentdir not in sys.path:
        sys.path.insert(0, parentdir)
    import generatedata
    function = generatedata.df_user
    f_print = func_adj.do(function)
    for line in f_print:
        print(line)
    functions in same module cannot use inspect
    """
    def __init__(self, name):
        self.name = self
       
    
    def do(self, same_mod = False):
        """
        will need to extract all functions recursively 
        """
        if same_mod ==False:
            def p(self):
                # source = inspect.getsource(self)
                source = unwrap_all(self)
                all_lines = source.splitlines()
                for line in range(len(all_lines)):
                    all_lines[line] = input_to_string(all_lines[line], False)                
                print('\n'.join(map(str, all_lines)))  
                return all_lines
            all_lines = p(self)

            return all_lines

        else:
            raise
            print("to be applied to external modules")
    

if __name__ == "__main__":
    parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if parentdir not in sys.path:
        sys.path.insert(0, parentdir)
    import generatedata
    function = generatedata.df_user
    f_print = func_adj.do(function)
    for line in f_print:
        print(line)





