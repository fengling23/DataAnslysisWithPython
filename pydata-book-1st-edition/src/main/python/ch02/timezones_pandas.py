#%matplotlib inline 
import json
from pandas import DataFrame, Series 
from numpy.random import randn 
import numpy as np 
import os
import matplotlib.pyplot as plt 
import pandas as pd
plt.rc('figure', figsize=(10,6)) 
np.set_printoptions(precision=4)

path ="pydata-book-1st-edition/ch02/usagov_bitly_data2012-03-16-1331923249.txt" 
records =[json.loads(line) for line in open(path)] 
print(records[0])

# create dataframe
frame = DataFrame(records) 
print(frame[:10])
print(frame['tz'][:10])

# get count for values
tz_counts = frame['tz'].value_counts( ) 
print(tz_counts[:10])

# handle na and empty data
clean_tz = frame['tz'].fillna('Missing') 
clean_tz[clean_tz == ''] = 'Unknown' 
tz_counts = clean_tz.value_counts() 
print(tz_counts[:10])

# draw bar chart
#plt.figure(figsize=(10，4))
#tz_counts[:10].plot(kind='barh',rot=0)
#plt.show()

# get browser of agents
browers = Series([x.split()[0] for x in frame['a'].dropna()]) 
print(browers[:10])
# identify the operating system 
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'),'Windows', 'Not Windows') 
print(operating_system[:10])

# group by tz then os
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
print(agg_counts[:10])

#sort by sum count for tz with asc 
indexer = agg_counts.sum(1).argsort() 
print(indexer[:10])

# take last 10 row with above sort
count_subset = agg_counts.take(indexer)[-10:]
print(count_subset )
# draw stacked bar chart
#plt.figure( )
#count_subset.plot(kind='barh',stacked=True
#plt.show()

# draw stacked bar chart for percentage
plt.figure()
normed_subset = count_subset.div(count_subset.sum(1),axis=0) 
normed_subset.plot(kind='barh',stacked=True)
plt.show()