import t2
import inspect as i


def foo(a, b):
    a= fee(a)
    return a + b

def fee(a):
    return a+1    

def unwrap_cls(object):
    """
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
    def foo(a):
        return a +1
    print(unwrap_fn(foo))
    """
    return i.getsource(object)


def unwrap_all(object):
    """
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
    fn[line] = fn[line]
    return fn


if __name__ == '__main__':
    #line = unwrap_all(t2.func_adj.do)
    source = i.getsource(t2.func_adj.do)
    #source = i.getsource(foo)
    all_lines = source.splitlines()
    line = unwrap_recur(all_lines)
    print(line)


