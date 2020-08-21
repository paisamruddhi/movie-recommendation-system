import pandas as pd 


ratings=pd.read_csv('ratings.csv')
movies=pd.read_csv('movies.csv')


movies['genres']=movies['genres'].str.replace("|"," ")
movies['title']=movies['title'].str.replace(r"\(.*?\)","")#to remove year ex:(2014)
movies['title']=movies['title'].str.replace("'","")#to remove single quotes example '71 
movies['title']=movies['title'].str.replace(', The','')# removs The at the end example:Shawshank Redemption, The
movies['title']=movies['title'].str.strip()#to remove wide spaces at the end


from sklearn.feature_extraction.text import CountVectorizer  #to encode the genres
vectorizer=CountVectorizer()
vector=vectorizer.fit_transform(movies['genres']).toarray()


from sklearn.metrics.pairwise import cosine_similarity   #get similarity matrix
similarity=cosine_similarity(vector)

dataset = pd.merge(ratings,movies,on='movieId')
dataset_based_on_ratings = pd.DataFrame(dataset.groupby('title')['rating'].mean())
dataset_based_on_ratings['number of ratings']=pd.DataFrame(dataset.groupby('title')['rating'].count())


movie_matrix = dataset.pivot_table(index='userId',columns='title',values='rating')
movie_matrix

        
def search_for_movie(movie_name):
    if movie_name  in movies['title'].unique():
        return 1
    else:
        return 0


def content_based_recomendation(movie_name):
    if search_for_movie(movie_name):
        try:
            movie_index=movies.loc[movies['title']==movie_name,['movieId']].index[0]
            #gets movie index based on name given
        
            similarity_values = pd.Series(similarity[movie_index])
            similar_movie_indexes = list(similarity_values.sort_values(ascending=False).index)
            #sorts the values based on the most similar movies first
        
            similar_movie_indexes.remove(movie_index)
            #removes the recomendation of same movie
        
        
            def get_movie_by_index(idx):
                return movies.loc[movies.index==idx,['title']].values[0][0]
        
        
            print("Since u watched --->",get_movie_by_index(movie_index),"<--- We recommend you")
            similar1=[]
            for i in range(15):
                similar1.append(get_movie_by_index(similar_movie_indexes[i]))
            return similar1
        except:
            return 0
    else:
        return 0



def ratings_based_recomendation(movie_name):
    if search_for_movie(movie_name):
        try:
            movie_watched = movie_matrix[movie_name]
            print("similar movies based on rating")
            li = []
            for i in range(len(movie_matrix.columns)):
                li.append(movie_watched.corr(movie_matrix.iloc[:,i]))
            li = pd.Series(li)
            df = pd.DataFrame({"title": movie_matrix.columns,"Correlation": li,"number of ratings" : dataset_based_on_ratings["number of ratings"].values})
            df=list(df[df["number of ratings"] >= 100].sort_values(by=["Correlation","number of ratings"],ascending=False).iloc[1:16,0])
            similar2=[]
            for i in range(15):
                similar2.append((df[i]))
            return similar2
        except:
            return 0
    else:
        return 0
