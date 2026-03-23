import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv('final_movies.csv')

# Select important columns
movies = movies[['title', 'overview', 'genres']]

# Clean data
movies.dropna(inplace=True)

# Convert to string
movies['overview'] = movies['overview'].astype(str)

# Create tags (combine features)
movies['tags'] = movies['overview'] + " " + movies['genres']

# Convert text → vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# Compute similarity
similarity = cosine_similarity(vectors)

def recommend(movie_name):
    movie_name = movie_name.lower()

    # Find movie index
    for i, title in enumerate(movies['title']):
        if movie_name in title.lower():
            distances = similarity[i]
            movie_list = sorted(list(enumerate(distances)),
                                reverse=True,
                                key=lambda x: x[1])[1:6]

            return [movies.iloc[j[0]].title for j in movie_list]

    return ["Movie not found"]
