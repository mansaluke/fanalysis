import unittest
from fanalysis.src.fanalysis import generatedata



if __name__ == '__main__':
    from fanalysis.src.fanalysis import generatedata
    from datetime import datetime
    df = generatedata.create_data('s', date=datetime.now(),
                     direction='Backwards').create_brownian_motion()

    for i in range(10):
        df = generatedata.append_data(df).create_brownian_motion()

    print(df.head())

 
