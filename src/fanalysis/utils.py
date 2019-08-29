# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:23:50 2019

@author: Luke
"""


def try_import(module_names):

    failed_imports = []

    def import_module_fn(mod_in):
        try:
            import mod_in
        except ImportError:
            failed_imports.append(mod_in)

    if isinstance(module_names, list):
        for mod in module_names:
            import_module_fn(mod)
    else:
        import_module_fn(module_names)

    if failed_imports ==[]:
        pass
    else:
        print('Unable to import ' + ', '.join(failed_imports))


class Ipython():
    @staticmethod
    def run_from_ipython():
        try:
            __IPYTHON__
            return True
        except NameError:
            return False

class timing():
    import threading
    from datetime import datetime, timedelta

    local = threading.local()
    class ExecutionTimeout(Exception): pass

    def start(max_duration = timedelta(seconds=1)):
        local.start_time = datetime.now()
        local.max_duration = max_duration

    def check():
        if datetime.now() - local.start_time > local.max_duration:
            raise ExecutionTimeout()

    def do_work():
        start()
        while True:
            check()
            # do stuff here
        return 10


def islarge_dataset(dataframe):
    print(df.memory_usage().sum())
    if df.memory_usage().sum()>100*10^6:
        return
