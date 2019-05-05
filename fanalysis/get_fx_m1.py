import csv
import os
import shutil
from datetime import timedelta
from datetime import date
from api import download_fx_m1_data, download_fx_m1_data_year
import pandas as pd
from extract import mkdir_p
import zipfile


def delete_old_data(path):
    files = os.listdir(path) #use os.getcwd() if files in same path. otherwise set path
    print(files)
    from extract import str_listconcat
    files = str_listconcat(files, path + '/')
    print('Existing files in the '+path+' folder will be deleted.')
    for f in files: 
        print(f)
    f = input('Press s to skip this step or any other key to delete the files. ')
    if f == 's':
        pass
    else:
        for f in files: 
            os.remove(f)
            print(f+ ' DELETED')



def unzip_files(path):
    files = os.listdir(path) #use os.getcwd() if files in same path. otherwise set path
    from extract import str_listconcat
    print(files)
    try:
        files = str_listconcat(files, path + '/')
        print('Existing files in the '+path+' folder will be unzipped.')
        for f in files: 
            print(f)
        f = input('Press s to skip this step or any other key to unzip the files. ')
        if f == 's':
            pass
        else:
            for f in files: 
                with zipfile.ZipFile(f,"r") as zip_ref:
                    zip_ref.extractall(path)
                #os.remove(f)
                print(f+ ' UNZIPPED')
    except:
        print("no files found")



def delete_zip_files(path):
    files = os.listdir(path) #use os.getcwd() if files in same path. otherwise set path
    print(files)
    from extract import str_listconcat
    files = [f for f in files if f[-3:] == 'zip']
    files = str_listconcat(files, path + '/')
    print('Zip files in the '+path+' folder will be deleted.')
    for f in files: 
        print(f)
    f = input('Press s to skip this step or any other key to delete the files. ')
    if f == 's':
        pass
    else:
        for f in files: 
            os.remove(f)
            print(f+ ' DELETED')



def try_year_download(y, currency_pair_code):
    try:
        while True:
            could_download_full_year = False
            try:
                output_filename = download_fx_m1_data_year(str(y), currency_pair_code)
                shutil.move(output_filename, os.path.join(output_folder, output_filename))
                could_download_full_year = True
            except:
                pass  #download month by month.
            month = 1
            while not could_download_full_year:
                output_filename = download_fx_m1_data(str(y), str(month), currency_pair_code)
                shutil.move(output_filename, os.path.join(output_folder, output_filename))
                month += 1

    except Exception:
        print('[DONE] for currency', currency_pair_code)



def month_year_iter_download(start_month, start_year, currency_pair_code,output_folder):
    """Downloads all periods from starting month/year to most recent"""
    first_day_current_month = date.today().replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    end_month = (last_day_previous_month.month)
    end_year = (last_day_previous_month.year)
#    ym_start= 12*start_year + start_month - 1
#    ym_end= 12*end_year + end_month - 1
    #y, m = divmod( ym, 12 )
    
    delete_old_data('data') #
    
    if start_year!=end_year:   
        if start_month == 1:
            for y in range(start_year, end_year):
                print(y)
                try_year_download(y, currency_pair_code)
                
            if end_month != 12:
                for m in range(1, end_month+1):
                    print(end_year, m)
                    download_fx_m1_data(end_year, m, currency_pair_code)
                    
            else:
                print(end_year)
                try_year_download(end_year, currency_pair_code)
                
        elif start_month > 1:
            for m in range(start_month-1, 12):
                print(start_year, m+1) 
                download_fx_m1_data(start_year, m+1, currency_pair_code)
                
            for y in range(start_year+1, end_year):
                print(y)
                try_year_download(end_year, currency_pair_code)
                
            if end_month != 12:
                for m in range(1, end_month+1):
                    print(end_year, m)
                    download_fx_m1_data(end_year, m, currency_pair_code)
                    
            else:
                print(end_year)
                try_year_download(end_year, currency_pair_code)
                
    elif start_year==end_year:
        if end_month !=12:
            for m in range(1, end_month+1):
                print(start_year, m)
                download_fx_m1_data(end_year, m, currency_pair_code)
                
        elif end_month ==12:
            print(end_year)
            try_year_download(end_year, currency_pair_code)
        
   

     
if __name__ == '__main__':
    print("choose the starting period and currency e.g. 2018 5 eurgbp")
    mkdir_p('data')
    path = 'data'
    y = int(input("enter start year e.g.2017:"))
    m = int(input("enter start month as an integer i.e for january enter 1:"))
    c = input("enter currency code e.g. eurgbp for euro to gbp")
    delete_zip_files('data')
    month_year_iter_download(m, y, c,path)
    unzip_files('data')
