import pandas as pd
#create data
#l = len(df)
rand = []
for r in enumerate(df):
    rand.append(rd.random())
rand = pd.Series(rand, name = 'rand')
df = pd.concat([df, rand], axis = 1, join = 'inner')


#funciton to extract date elements (not used for now)
def datesplit(df):
    df = df.copy()
    df['day'] = pd.DatetimeIndex(df['date']).day
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['week'] = pd.DatetimeIndex(df['date']).week
    df['year'] = pd.DatetimeIndex(df['date']).year
    return df
df = datesplit(df)


df['aggday'] = df[df['month']>1].apply(lambda row: monthrange(row['year'], row['month']), axis=1)

df[['a', 'aggday']] = df['aggday'].apply(pd.Series)

df.drop(columns=['a'], inplace=True)

df.loc[df['month'] ==1, 'aggday'] = 0
df['aggday'] = df['aggday'] + df['day']
print(df.head())
print(df.info())

print(datetime.now())
#out = df.to_json(orient='split')
#
#with open('temp.json', 'w') as f:
#    f.write(out)
fd.to_json('temp.json', orient='index')
print(datetime.now())

df['TS'] =  0.1 * df['aggday'] - df['rand'] *0.1 
print(df.head())
plt.plot(df['date'], df['TS'])
plt.title('TS')
plt.ylabel('Price (£)')
plt.show()

mean = df['d1'].mean()
print(mean)

variance = statistics.variance(df['d1'])
print(variance)