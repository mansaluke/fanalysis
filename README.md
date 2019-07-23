
# ML for Financial Analysis (fanalysis)

## Objectives

Download exchange rates and perform predictive analyses using various techniques including the following:

- Standard Econometric Time Series Forecasts
- Machine\deep learning models e.g. Random forests, Neural networks etc

**Finally, the forecasts will be used as inputs in a dynamic optimization model which identifies the optimal portfolio of the set of rates.**

## Current funcionality

- Create dummy data
- Download historical data (m1)
- Store in various formats i.e. json, csv, pickle and parquet formats
- Generate very basic random forest

### Use

#### Setup

```shell
pip install -r "/path/to/requirements.txt"
```

#### Download data

``` python
#download all data from first available month up until last closed month.
import get_fx_m1 as g

path = 'fanalysis\\data\\get_fx_data'
g.mkdir_p(path)
g.month_year_iter_download(1, 2000, 'eurgbp',path)
g.unzip_files(path)
g.delete_zip_files(path)

#load and concatenate CSVs into single dataframe.
import dfconvert as dfc
df = dfc.use_csvs(path)

import plotting as p
p.plots(df)

import structure as s

columns = 'Bar OPEN Bid Quote', 'Bar HIGH Bid Quote', 'Bar LOW Bid Quote', 'Bar CLOSE Bid Quote', 'Volume'

for col in columns:
    print(col)
    try:
        a = s.outlier_detect(df, col, graph = False)
        print(a.outliers)
        df= a.delete_threshold()
    except:
        pass

p.plots(df)

#columns added for RF
df = s.date_split(df)
df = s.lag_var(df, 'Bar OPEN Bid Quote', -1)

#here we store file in HDF5 format.
dfc.df_store("data.h5").store_df(df)
#HDF5 or feather recommended for large files. See dfconvert module for full list of file formats.

##############################################
df = dfc.df_store("data.h5").load_df()
print(df.head())


```

## To be introduced/developed

- Tick data and current data
- Improve performance - big data techniques (e.g. spark and hadoop)
- Additional independent variables
- Time series and neural network integration
- Incorporate dynamic optimization model
- Full integration of all modules
- App gui
- Automate continuous analysis
