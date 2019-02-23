import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

def download_fx_m1_data(year, month, pair):
    """
    Download 1-Minute FX data per month.
    :param year: Trading year. Format is 2016.
    :param month: Trading month. Format is 7 or 12.
    :param pair: Currency pair. Example: eurgbp.
    :return: ZIP Filename.
    """
    referer = 'http://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/{}/{}/{}'.format(
        pair.lower(),
        year, month)

    # Referer is the most important thing here.
    headers = {'Host': 'www.histdata.com',
               'Connection': 'keep-alive',
               'Content-Length': '104',
               'Cache-Control': 'max-age=0',
               'Origin': 'http://www.histdata.com',
               'Upgrade-Insecure-Requests': '1',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Referer': referer}

    r1 = requests.get(referer)
    assert r1.status_code == 200, 'Make sure the website www.histdata.com is up.'

    soup = BeautifulSoup(r1.content, 'html.parser')
    try:
        token = soup.find('input', {'id': 'tk'}).attrs['value']
        assert len(token) > 0
    except:
        raise AssertionError('There is no token. Please make sure your year/month/pair is correct.'
                             'Example is year=2016, month=7, pair=eurgbp')

    data = {'tk': token,
            'date': str(year),
            'datemonth': '{}{}'.format(year, str(month).zfill(2)),
            'platform': 'ASCII',
            'timeframe': 'M1',
            'fxpair': pair.upper()}
    r = requests.post(url='http://www.histdata.com/get.php',
                      data=data,
                      headers=headers)

    assert len(r.content) > 0, 'No data could be found here.'
    print(data)

    output_filename = 'DAT_ASCII_{}_M1_{}.zip'.format(pair.upper(), '{}{}'.format(year, str(month).zfill(2)))
    with open(output_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print('Wrote to {}'.format(output_filename))
    return output_filename


#if __name__ == '__main__':
#    download_fx_m1_data('2019', '1', 'eurgbp')
#download all data since start date and update itself


def month_year_iter(start_month, start_year):
    first_day_current_month = date.today().replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    end_month = (last_day_previous_month.month)
    end_year = (last_day_previous_month.year)
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end ):
        y, m = divmod( ym, 12 )
        print(y, m, start_month, end_month)
        download_fx_m1_data(y, m, 'eurgbp')

month_year_iter(12, 2018)
