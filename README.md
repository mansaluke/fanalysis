
# ML for Financial Analysis (fanalysis)

## Objectives

Download exchange rates and perform predictive analyses using various techniques, including the following:

- Standard Econometric Time Series Forecasts
- Machine\deep learning models e.g. Random forests, Neural networks etc

**Finally, the forecasts will be used as inputs in a dynamic optimization (mean variance) model which identifies the optimal portfolio of the set of rates.**

## Current funcionality

- Create dummy data.
- Download historical data (m1).
- Structure data appropriately for analysis.
- Store data in various formats i.e. json, csv, pickle, parquet, feather and HDF5.
- Generate basic random forest for feature and predictive analysis.

### Use

#### Requirements

Major requirements

- Required: python 3.7
- Recommended: https://github.com/cuemacro/findatapy - for installation of tick data.

#### Setup

```shell
pip install -r "/path/to/requirements.txt"
```

#### Download data

``` python
#run.py


```

## To be introduced/developed

- Tick data and current data
- Include finance specific structural functions
- Improve performance - big data techniques (e.g. spark and hadoop)
- Time series and neural network integration
- Incorporate dynamic optimization model
- Additional independent variables
- Full integration of all modules
- App gui
- Automate continuous analysis
