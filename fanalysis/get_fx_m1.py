import csv
import os
import shutil
from datetime import timedelta
from datetime import date
from api import download_fx_m1_data, download_fx_m1_data_year
import pandas as pd

def mkdir_p(path):
    import errno
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def mkfile(file):
    try:
       open(file, 'x')
    except FileExistsError:
       pass

def month_year_iter_download(start_month, start_year, currency_pair_code,output_folder):
    '''Downloads all periods from starting month/year to most recent'''
    first_day_current_month = date.today().replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    end_month = (last_day_previous_month.month)
    end_year = (last_day_previous_month.year)
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    collectym = {}
    collecty = []
    a = []
    s = pd.Series(['y', 'm'])
    for ym in range( ym_start, ym_end ):
        #print(ym)
        y, m = divmod( ym, 12 )
        print(y, m+1)
        m = m+1
        s.append([y, m])
    print(s)
    return

#        collectym[m] = y
#        if m== 1:
#            collecty.append(y)
#    print(collectym)
#    print(collecty)
#    collectym = {key:val for key, val in collectym.items() if val not in collecty[0:-1]}
#    print(collectym)
#    for k in collecty[0:-1]:
#        print(k, currency_pair_code)
#        try:
#            print(1)
#            while True:
#                could_download_full_year = False
#                try:
#                    output_filename = download_fx_m1_data_year(str(k), currency_pair_code)
#                    shutil.move(output_filename, os.path.join(output_folder, output_filename))
#                    could_download_full_year = True
#                except:
#                    pass  #download month by month.
#                month = 1
#                while not could_download_full_year:
#                    output_filename = download_fx_m1_data(str(k), str(month), currency_pair_code)
#                    shutil.move(output_filename, os.path.join(output_folder, output_filename))
#                    month += 1
#    
#        except Exception:
#            print('[DONE] for currency', currency_pair_code)


        
        
#month_year_iter(12, 2010)        
 #download_fx_m1_data(y, m+1, 'eurgbp')
if __name__ == '__main__':
    mkdir_p('data')
    month_year_iter_download(5, 2016, 'eurgbp','data')

