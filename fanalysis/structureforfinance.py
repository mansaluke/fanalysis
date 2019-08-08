"""
Reference: advances_in_financial_machine_learning_wiley (2018)
"""


import numpy as np
import pandas as pd


#SNIPPET 2.1 PCA WEIGHTS FROM A RISK DISTRIBUTION R 

def pcaWeights(cov,riskDist=None,riskTarget=1.): 
    # Following the riskAlloc distribution, match riskTarget 
    eVal,eVec=np.linalg.eigh(cov) # # must be Hermitian  
    indices=eVal.argsort()[::-1] # arguments for sorting eVal desc 
    eVal,eVec=eVal[indices],eVec[:,indices] 
    if riskDist is None: 
        riskDist=np.zeros(cov.shape[0]) 
        riskDist[-1]=1. 
    loads=riskTarget*(riskDist/eVal)**.5 
    wghts=np.dot(eVec,np.reshape(loads,(-1,1))) 
    #ctr=(loads/riskTarget)**2*eVal # verify riskDist 
    return wghts


#SNIPPET 2.2 FORM A GAPS SERIES, DETRACT IT FROM PRICES
def getRolledSeries(pathIn,key): 
    series=pd.read_hdf(pathIn,key='bars/ES_10k') 
    series['Time']=pd.to_datetime(series['Time'],format='%Y%m%d%H%M%S%f') 
    series=series.set_index('Time') 
    gaps=rollGaps(series) 
    for ﬂd in ['Close','VWAP']:
        series[ﬂd]-=gaps 
    return series 

    #——————————————————————————————————————————— 
def rollGaps(series,dictio={'Instrument':'FUT_CUR_GEN_TICKER','Open':'PX_OPEN', 'Close':'PX_LAST'},matchEnd=True): 
    # Compute gaps at each roll, between previous close and next open 
    rollDates=series[dictio['Instrument']].drop_duplicates(keep='ﬁrst').index 
    gaps=series[dictio['Close']]*0 
    iloc=list(series.index) 
    iloc=[iloc.index(i)-1 for i in rollDates] # index of days prior to roll 
    gaps.loc[rollDates[1:]]=series[dictio['Open']].loc[rollDates[1:]]- \
        series[dictio['Close']].iloc[iloc[1:]].values 
    gaps=gaps.cumsum() 
    if matchEnd:gaps-=gaps.iloc[-1] # roll backward 
    return gaps


#SNIPPET 2.3 NON-NEGATIVE ROLLED PRICE SERIES 
def nonneg_rolled():
    raw=pd.read_csv(ﬁlePath,index_col=0,parse_dates=True) 
    gaps=rollGaps(raw,dictio={'Instrument':'Symbol','Open':'Open','Close':'Close'}) 
    rolled=raw.copy(deep=True) 
    for ﬂd in ['Open','Close']:rolled[ﬂd]-=gaps 
    rolled['Returns']=rolled['Close'].diff()/raw['Close'].shift(1) 
    rolled['rPrices']=(1+rolled['Returns']).cumprod()
    return rolled



#SNIPPET 2.4 THE SYMMETRIC CUSUM FILTER
def getTEvents(gRaw,h): 
    tEvents,sPos,sNeg=[],0,0 
    diff=gRaw.diff() 
    for i in diff.index[1:]: 
        sPos,sNeg=max(0,sPos+diff.loc[i]),min(0,sNeg+diff.loc[i]) 
        if sNeg<-h: 
            sNeg=0;tEvents.append(i) 
        elif sPos>h: 
            sPos=0;tEvents.append(i) 
    return pd.DatetimeIndex(tEvents)



if __name__ == "__main__":
    pass
