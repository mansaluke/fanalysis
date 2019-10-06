


call_count = {}

def count_calls(fn):   

    print("decorating" )    

    def new_function(*args,**kwargs):

        print("starting timer" )      
        import datetime                 
        before = datetime.datetime.now()                     
        print(fn.__name__)
        if call_count.get(fn.__name__) is None:
            call_count[fn.__name__] = 1 
        else:
            call_count[fn.__name__] = call_count.get(fn.__name__) + 1
        print(call_count)

        x = fn(*args,**kwargs)

        after = datetime.datetime.now()                      
        print("Elapsed Time: {0}".format(after-before)   )   

        return x

    return new_function

def count_class_funcion_calls(cls):
    """
    counts and times each occasion a function is run in a class
    """

    class NewCls(object):

        def __init__(self,*args,**kwargs):
            self.oInstance = cls(*args,**kwargs)

        def __getattribute__(self,s):
            """
            this is called whenever any attribute of a NewCls object is accessed. This function first tries to 
            get the attribute off NewCls. If it fails then it tries to fetch the attribute from self.oInstance (an
            instance of the decorated class). If it manages to fetch the attribute from self.oInstance, and 
            the attribute is an instance method then `count_calls` is applied.
            """

            try:    
                x = super(NewCls,self).__getattribute__(s)
            except AttributeError:      
                pass
            else:
                return x

            x = self.oInstance.__getattribute__(s)

            if type(x) == type(self.__init__): # it is an instance method
                return count_calls(x)
            else:
                return x

    return NewCls




if __name__ == '__main__':

    #@count_class_funcion_calls
    class test_class():
        def __init__(self, a):
            self.x = 5
            self.a = a

        @count_calls
        def fn(self):
            print("ran fn")
            return 2

        def b(self): return self.a

    my_class = test_class(5)
    print(my_class.fn())
    print(my_class.a)
    print(my_class.b())

    print(test_class.__name__)



