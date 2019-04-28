import inspect
import generatedata



class func_adj:
    """functions in same module cannot use inspect
    """
    def __init__(self, name):
        self.name = self
       
    
    def do(self, same_mod = False):
        """
        will need to extract all functions recursively 
        """
        if same_mod ==False:
            def p(self):
                source = inspect.getsource(self)
                all_lines = source.splitlines()
                for line in range(len(all_lines)):
                    if "print(" in all_lines[line]:
                        
                        new_line = all_lines[line].replace("print", "a = ")
                        print(new_line)
                        all_lines[line] = new_line

                    if "input(" in all_lines[line]:
                        """
                        e.g.p = input('How many {} would you like to generate? '.format(freq))
                        """
                        
                        print(all_lines[line])
                        print(all_lines[line].find("input("))

                        
                        print(len(all_lines[line].rstrip()))

                        new_line = all_lines[line].replace("input(", "a = ")
                        print(new_line)
                        all_lines[line] = new_line

                #print('\n'.join(map(str, all_lines)))  
                return all_lines
            all_lines = p(self)
            return all_lines

        else:
            print("to be applied to external modules")
            pass        
    


function = generatedata.df_user
l = func_adj.do(function)

