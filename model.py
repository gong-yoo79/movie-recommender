import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('final_movies.csv')

movies['tags'] = movies['overview'] + " " + movies['genres']

cv = CountVectorizer(max_features=3000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vectors)

def recommend(movie):
    movie = movie.lower()
    movies['title'] = movies['title'].str.lower()

    if movie not in movies['title'].values:
        return ["Movie not found"]

    idx = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]

    movie_list = sorted(list(enumerate(distances)),
                        reverse=True,
                        key=lambda x: x[1])[1:6]

    return [movies.iloc[i[0]].title for i in movie_list]
