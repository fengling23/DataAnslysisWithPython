import pandas as pd 
import os
encoding = 'latin1'

upath = os.path.expanduser("pydata-book-1st-edition/ch02/movielens/users.dat") 
rpath = os.path.expanduser("pydata-book-1st-edition/ch02/movielens/ratings.dat") 
mpath = os.path.expanduser("pydata-book-1st-edition/ch02/movielens/movies.dat") 

unames = ['user_id','gender', 'age', 'occupation', 'zip'] 
rnames = ['user_id', 'movie_id', 'rating', 'timestamp'] 
mnames = ['movie_id', 'title', 'genres']

users = pd.read_csv(upath, sep='::', header=None, names=unames, encoding=encoding, engine='python') 
ratings = pd.read_csv(rpath, sep='::', header=None, names=rnames,encoding=encoding, engine='python') 
movies = pd.read_csv(mpath, sep='::', header=None, names=mnames,encoding=encoding, engine='python')
print(users[:5]) 
print(ratings[:5]) 
print(movies[:5])


# join action based on same column name
data = pd.merge(pd.merge(ratings, users), movies) 
print(data[:5])

# get avg rating for each movie and gender
mean_ratings = data.pivot_table('rating' , index='title', columns='gender', aggfunc='mean') 
print(mean_ratings[:5])

# filter by count>=250 I 
ratings_by_title = data.groupby('title').size() 
print(ratings[:10])
active_titles = ratings_by_title.index[ratings_by_title>=250] 
print(active_titles[:10])
mean_ratings = mean_ratings.loc[active_titles] 
print(mean_ratings[:10])

# order by female rating
top_female_ratings = mean_ratings.sort_values(by='F',ascending=False) 
print(top_female_ratings[:10])

# order by rating gap between gender
mean_ratings['diff']= mean_ratings['M']- mean_ratings['F'] 
sorted_by_diff = mean_ratings.sort_values(by='diff') 
print(sorted_by_diff[:10])
# reverse
print(sorted_by_diff[::-1][:10])

#计算标准差
rating_std_by_title = data.groupby('title')['rating'].std() 
rating_std_by_title =rating_std_by_title.loc[active_titles] 
print(rating_std_by_title.sort_values(ascending=False)[:10])