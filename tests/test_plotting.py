import unittest

from fanalysis.src.fanalysis import generatedata
from fanalysis.src.fanalysis import plotting as p

from datetime import datetime, timedelta
import pandas as pd

time_start = datetime.now()
diff = 500
time_end = time_start + timedelta(seconds = diff)

df = generatedata.create_data('s', date=time_start,
                direction='Backwards', num_periods=diff).create_brownian_motion()

df = generatedata.append_data(df).create_brownian_motion()

class TestDataFrameMethods(unittest.TestCase):
    def test_headers(self):
        self.assertEqual(my_plot.header, \
            ['Date', 'bm', 'bm1', 'bm2'])

if __name__ == "__main__":
    my_plot = p.graph_vars(df, )
    my_plot.show()
    unittest.main()

