#%matplotlib inline
import pandas as pd
#from __future_import division 
from numpy.random import randn 
import numpy as np
import matplotlib.pyplot as plt 
plt.rc('figure',figsize=(12,5)) 
np.set_printoptions(precision=4)

#%pwd
#!head -n 10 pydata-book-1st-edition/ch02/names/yob1880.txt

names1880 = pd.read_csv('pydata-book-1st-edition/ch02/names/yob1880.txt', names=['name', 'sex','births'])
print(names1880)
print(names1880.groupby('sex').births.sum())

# write python code to read files under 'pydata-book-Ist-edition/ch02/names/' then concat all years 
years = range(1880,2011) 
pieces = []
columns = ['name', 'sex', 'births'] 
for year in years:
    path ='pydata-book-1st-edition/ch02/names/yob%d.txt' % year 
    frame = pd.read_csv(path,names=columns) 
    frame['year']=year 
    pieces.append(frame)
#names = pd.concat(pieces,ignore_index=True)
print(names)

# get total birth for each year and sex
total_births = names.pivot_table('births',index='year',columns="sex", aggfunc=sum) 
print(total_births.tail(10))
#total_births.plot(title='Total births by sex and year')
#plt.show( )

# add percentage prop
def add_prop(group):
    births = group.births.astype(float) 
    group['prop'] = births / births.sum() 
    return group

names = names.groupby(['year','sex']).apply(add_prop) 
print(names)
print(np.allclose(names.groupby(['year','sex']).prop.sum(),1))

#get top 1000 names for each year and sex
def get_top(group,n=1000):
    return group.sort_values(by='births', ascending=False)[:n] 
top1000 = names.groupby(['year','sex']).apply(get_top,n=1000)
# 'year' is both an index level and a column label,which is ambiguous 
top1000.index = np.arange(len(top1000))
print(top1000)

# get total birth for each year and name 
boys = top1000[top1000.sex=='M'] 
girls = top1000[top1000.sex=='F']
total_births = top1000.pivot_table('births',index='year',columns= 'name', aggfunc=sum)
print(total_births)

subset = total_births[['John','Harry','Mary','Marilyn']]
#subset.plot(subplots=True,figsize=(12,10),grid=False, title="Number of births per year")
#plt.show()
plt.figure()

# top1000 percentage trend
table = top1000.pivot_table('prop', index='year', columns='sex' , aggfunc=sum)
#table.plot(title='Sum of table1000.prop by year and sex' , yticks=np.linspace(0,1.2,13), xticks-range (1880, 2020,10))
#plt.show()

# distince name count for 50% baby 
df = boys[boys.year ==2010] 
print(df)
prop_cumsum = df.sort_values(by='prop',ascending=False).prop.cumsum()
print(prop_cumsum[:10])
# search insert index in an sorted array 
print(prop_cumsum.searchsorted(0.5))
# 116
df = boys[boys.year ==1900]
in1900 = df.sort_values(by='prop',ascending=False).prop.cumsum() 
print(in1900[:10])
# search insert index in an sorted array 
print(in1900.searchsorted(0.5))
# 25

def get_quantile_count(group,q=0.5):
    group = group.sort_values(by='prop', ascending=False) 
    return group.prop.cumsum( ).searchsorted(q) +1

# seems unstack not take effect
#diversity = top1000.groupby(['year','sex']).apply(get_quantile_count)
#diversity.unstack('sex')
diversity = top1000.groupby('year').apply(get_quantile_count) 
print(diversity.head())
#diversity.plot(title='Number of popular names in top 50%')
#plt.show( )

last_letters = names.name.map(lambda x: x[-1]) 
last_letters.name = 'last_letter'
table = names.pivot_table('births',index=last_letters, columns=['sex', 'year'], aggfunc=sum) 
subtable = table.reindex(columns=[1910,1960,2010],level='year') 
print(subtable)
letter_prop = subtable/subtable.sum().astype(float)
#fig, axes = plt.subplots(nrows=2,ncols=1,figsize=(10,8))
#letter_prop['M'].plot(kind='bar' ,rot=0, ax=axes[0], title='Male ')
#letter_prop['F'].plot(kind='bar',rot=0,ax=axes[1],title='Male',legend=False)
#plt.show()

letter_prop = table/table.sum().astype(float)
boys_dny_ts = letter_prop.loc[['d','n','y'],'M'].T 
print(boys_dny_ts.head( ))
#boys_dny_ts.plot()
#plt.show()

# percentage trend of boy and gril for some names
all_names = top1000.name.unique( )
mask = np.array(['lesl' in x.lower( ) for x in all_names]) 
lesl_like = all_names[mask] 
print(lesl_like)
#filtered =top1000[top1000['name'].str.contains('lesl', case=False)] 
filtered = top1000[top1000.name.isin(lesl_like)] 
print(filtered.groupby('name').births.sum())
table = filtered.pivot_table('births', index='year', columns='sex' , aggfunc=sum) 
table = table.div(table.sum(1),axis=0) 
print(table.tail())
table.plot(style={'M':'k-','F':'k--'})
plt.show()