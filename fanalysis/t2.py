import inspect
import generatedata
import t3


class func_adj():
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
                    if "print(" in all_lines[line] or "input(" in all_lines[line]:
                        
                        print(t3.input_to_string(all_lines[line]))
                        all_lines[line] = t3.input_to_string(all_lines[line])                
                print('\n'.join(map(str, all_lines)))  
                return all_lines
            all_lines = p(self)

            return all_lines

        else:
            print("to be applied to external modules")
            pass        
    

if __name__ == "__main__":
    function = generatedata.df_user
    l = func_adj.do(function)

