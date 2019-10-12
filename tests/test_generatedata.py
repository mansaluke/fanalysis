#################imports#################################
import unittest
from pandas.util.testing import assert_frame_equal

from fanalysis.src.fanalysis import generatedata

from datetime import datetime, timedelta

##########################################################



time_start = datetime.now()
diff = 50
time_end = time_start + timedelta(seconds = diff)
print(time_start, time_end)

df_1 = generatedata.create_data('s', date=time_start,
                 direction='Backwards', num_periods=diff).create_brownian_motion()

for i in range(2):
    df_1 = generatedata.append_data(df_1).create_brownian_motion()
print(df_1.head())

df_2 = generatedata.create_data_sef(time_start, time_start, 's').gendateseries()
df_3 = generatedata.create_data_sef(time_start, time_start, 's').gendateseries()
df_4 = generatedata.append_data(df_3).dates






class TestDataFrameMethods(unittest.TestCase):
    """
    tests output of generatedata module functions
    """
    def test_headers(self):
        self.assertEqual(df_1.columns.to_list(), \
            ['Date', 'bm', 'bm1', 'bm2'])

    def test_class_df(self):
        assert_frame_equal(df_2, df_3)
        assert_frame_equal(df_3, df_4)



if __name__ == "__main__":
    unittest.main()

