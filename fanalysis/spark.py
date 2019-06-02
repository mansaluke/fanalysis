import extract

def islarge_dataset(dataframe):
    print(df.memory_usage().sum())
    if df.memory_usage().sum()>100*10^6:
        return

import numpy as np
import pandas as pd
import pyspark
import spark
# Enable Arrow-based columnar data transfers
spark.conf.set("spark.sql.execution.arrow.enabled", "true")

# Generate a Pandas DataFrame
pdf = pd.DataFrame(np.random.rand(100, 3))

# Create a Spark DataFrame from a Pandas DataFrame using Arrow
df = spark.createDataFrame(pdf)

# Convert the Spark DataFrame back to a Pandas DataFrame using Arrow
result_pdf = df.select("*").toPandas()

if __name__ == "__main__":
    df = use_csvs()

