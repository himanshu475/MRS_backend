import pandas as pd
import numpy as np
import os
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = None
similarity = None

def load_and_prepare_data():
    global df, similarity
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    movies_path = os.path.join(BASE_DIR, '../data/tmdb_5000_movies.csv')
    credits_path = os.path.join(BASE_DIR, '../data/tmdb_5000_credits.csv')

    print(f"Movies file size: {os.path.getsize(movies_path) / (1024 * 1024):.2f} MB")
    print(f"Credits file size: {os.path.getsize(credits_path) / (1024 * 1024):.2f} MB")

    df_movies = pd.read_csv(movies_path)
    df_credits = pd.read_csv(credits_path)

    df = df_movies.merge(df_credits, on='title')

    df['keywords'] = df['keywords'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    df['keywords'] = df['keywords'].apply(lambda x: ' '.join([kw['name'] for kw in x]))

    df['genres'] = df['genres'].apply(lambda x: ' '.join(g['name'] for g in ast.literal_eval(x)) if pd.notna(x) else '')
    df['cast'] = df['cast'].apply(lambda x: ' '.join(c['name'] for c in ast.literal_eval(x)[:4]) if pd.notna(x) else '')

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
    df['tags'] = df['keywords'] + ' ' + df['genres'] + ' ' + df['cast'] + ' ' + df['director'].fillna('')

    vectorizer = CountVectorizer(max_features=5000, stop_words='english')
    vector_matrix = vectorizer.fit_transform(df['tags'])
    similarity = cosine_similarity(vector_matrix)

def recommend_movie(movie_title, top_n=5):
    if df is None or similarity is None:
        return []

    movie_title_lower = movie_title.lower()
    titles = df['title'].str.lower()
    
    if movie_title_lower not in titles.values:
        return []

    index = titles[titles == movie_title_lower].index[0]
    distances = similarity[index]
    top_matches = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:top_n+1]

    result = []
    for idx, _ in top_matches:
        movie = df.iloc[idx]
        result.append({
            "title": movie["title"],
            
            "rating": str(movie.get("vote_average", "")),
            "genre": movie["genres"].split(),
            "year": movie["release_date"].split("-")[0] if pd.notna(movie.get("release_date")) else "",
            "runtime": f"{int(movie['runtime'])} min" if pd.notna(movie.get("runtime")) else "",
            "director": movie.get("director", ""),
            "plot": movie.get("overview", ""),
            "cast": movie["cast"].split()
        })
    return result
