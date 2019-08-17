import os, sys
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '/../../'))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)

#from fanalysis.Models import t



if __name__ == "__main__":
    print(parentdir)

    
#c:\Users\lmcleary\Documents\python\fanalysis\fanalysis\Models