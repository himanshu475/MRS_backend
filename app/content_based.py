import pandas as pd
import numpy as np
import os
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Get base directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct full paths to the CSV files
movies_path = os.path.join(BASE_DIR, '../data/tmdb_5000_movies.csv')
credits_path = os.path.join(BASE_DIR, '../data/tmdb_5000_credits.csv')

# Load datasets
df = pd.read_csv(movies_path)
credits_df = pd.read_csv(credits_path)

# Merge datasets
df = df.merge(credits_df, on='title')

# Parse and clean keywords
df['keywords'] = df['keywords'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df['keywords'] = df['keywords'].apply(lambda x: ' '.join([kw['name'] for kw in x]))

# Parse and clean genres
def parse_genres(text):
    try:
        genres = ast.literal_eval(text)
        return [g['name'] for g in genres]
    except:
        return []

df['genres'] = df['genres'].apply(parse_genres)
df['genres'] = df['genres'].apply(lambda x: ' '.join(x) if isinstance(x, list) else '')

# Parse and clean cast
def extract_cast(text):
    try:
        cast_list = ast.literal_eval(text)
        return [c['name'] for c in cast_list[:4]]
    except:
        return []

df['cast'] = df['cast'].apply(extract_cast)
df['cast'] = df['cast'].apply(lambda x: ' '.join(x) if isinstance(x, list) else '')

# Parse and extract director from crew
def extract_director(crew_text):
    try:
        crew_list = ast.literal_eval(crew_text)
        for member in crew_list:
            if member.get("job") == "Director":
                return member.get("name")
    except:
        return ""
    return ""

df['director'] = df['crew'].apply(extract_director)

print(df['cast'])

# Vectorize keywords and genres
vectorizer = CountVectorizer(stop_words='english')
keywords_matrix = vectorizer.fit_transform(df['keywords'])
genres_matrix = vectorizer.fit_transform(df['genres'])

# Cosine similarities
cosine_sim_keywords = cosine_similarity(keywords_matrix, keywords_matrix)
cosine_sim_genres = cosine_similarity(genres_matrix, genres_matrix)
combined_similarity = (cosine_sim_keywords + cosine_sim_genres) / 2

# Recommendation function
def recommend_movie(movie_title, top_n=5):
    movie_title_lower = movie_title.lower()
    lowercased_titles = df['title'].str.lower()

    if movie_title_lower not in lowercased_titles.values:
        return []

    movie_idx = lowercased_titles[lowercased_titles == movie_title_lower].index[0]
    similarities = combined_similarity[movie_idx]
    scored_movies = list(enumerate(similarities))
    scored_movies = sorted(scored_movies, key=lambda x: x[1], reverse=True)
    top_movies = scored_movies[1:top_n + 1]

    recommendations = []
    for idx, _ in top_movies:
        movie = df.iloc[idx]
        recommendations.append({
            "title": movie["title"],
            "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if pd.notna(movie.get("poster_path")) else "",
            "rating": str(movie.get("vote_average", "")),
            "genre": movie["genres"].split(),
            "year": movie["release_date"].split("-")[0] if pd.notna(movie.get("release_date")) else "",
            "runtime": f"{int(movie['runtime'])} min" if pd.notna(movie.get("runtime")) else "",
            "director": movie.get("director", ""),
            "plot": movie.get("overview", ""),
            "cast": movie["cast"].split()
        })

    return recommendations
