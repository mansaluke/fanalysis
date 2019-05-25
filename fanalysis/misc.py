# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:23:50 2019

@author: Luke
"""

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



