import csv
import os
import shutil
from datetime import timedelta
from datetime import date
from api import download_fx_m1_data, download_fx_m1_data_year


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
    for ym in range( ym_start, ym_end ):
        ##print(ym)
        y, m = divmod( ym, 12 )
        print(y, m, start_month, end_month)
        #collectym[y] = m
        if m== 1:
            collecty.append(y)
    print(collecty)
    print(collectym)
    for k in collecty[1:-1]:
        print(k)
        try:
            while True:
                could_download_full_year = False
                try:
                    output_filename = download_fx_m1_data_year(k, currency_pair_code)
                    shutil.move(output_filename, os.path.join(output_folder, output_filename))
                    could_download_full_year = True
                except:
                    pass  #download month by month.
                month = 1
                while not could_download_full_year and month <= 12:
                    output_filename = download_fx_m1_data(str(k), str(month), currency_pair_code)
                    shutil.move(output_filename, os.path.join(output_folder, output_filename))
                    month += 1
                #year += 1
        except Exception as e:
            print('[DONE] for currency', currency_pair_name)


        
        
#month_year_iter(12, 2010)        
 #download_fx_m1_data(y, m+1, 'eurgbp')

mkdir_p('fanalysis/data')

#if __name__ == '__main__':
while 1 ==2:    
    with open('fanalysis/data/pairs.csv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader, None)  # skip the headers
        for row in reader:
            currency_pair_name, currency_pair_code, history_first_trading_month = row
            year = int(history_first_trading_month[0:4])
            print(currency_pair_name)
            output_folder = os.path.join('output', currency_pair_code)
            mkdir_p(output_folder)
            try:
                while True:
                    could_download_full_year = False
                    try:
                        output_filename = download_fx_m1_data_year(year, currency_pair_code)
                        shutil.move(output_filename, os.path.join(output_folder, output_filename))
                        could_download_full_year = True
                    except:
                        pass  # lets download it month by month.
                    month = 1
                    while not could_download_full_year and month <= 12:
                        output_filename = download_fx_m1_data(str(year), str(month), currency_pair_code)
                        shutil.move(output_filename, os.path.join(output_folder, output_filename))
                        month += 1
                    year += 1
            except Exception as e:
                print('[DONE] for currency', currency_pair_name)






