import generatedata as g
import structureforfinance as sff
import plotting as p

from datetime import datetime, timedelta
import pandas as pd

time_start = datetime.now()
diff = 500
time_end = time_start + timedelta(seconds = diff)

df = g.create_data('s', date=time_start,
                direction='Backwards', num_periods=diff).create_brownian_motion()

df = g.append_data(df).create_brownian_motion()


print(df.head())


my_plot = p.graph_vars(df)
my_plot.show()
print(my_plot.header)

