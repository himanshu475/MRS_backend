# 🎬 Movie Recommendation System (SuggestIO)

This is a **content-based movie recommendation system** built with **Python** and **FastAPI**. It suggests movies similar to the one entered by the user based on metadata such as **keywords, genres, cast, and director**.

---

## 📌 What I Did

- ✅ Collected and preprocessed data from the TMDB 5000 movies and credits datasets.
- 🔄 Merged movies and credits CSV files on the movie title.
- 🧠 Extracted important features:
  - `keywords`
  - `genres`
  - `top 4 cast members`
  - `director`
- 🏷 Combined these features into a single `tags` column for each movie.
- ✨ Used `CountVectorizer` to convert tags into feature vectors (max 5000 words, excluding stop words).
- 📐 Calculated cosine similarity between movie vectors to measure closeness.
- 🔍 Built a function to recommend top N similar movies based on the input title.
- 🚀 Created a FastAPI backend with:
  - Root endpoint (`/`)
  - Recommendation endpoint (`/recommend?title=MovieName&top_n=5`)
- 🌐 Enabled CORS middleware to support frontend requests.

---

## 📁 Files Explained

- `content_based.py`: Contains data loading, preprocessing, and the recommendation logic.
- `api.py`: FastAPI server with defined endpoints and CORS settings.
- `data/`: Folder where `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` should be placed.

---

## 📽️ Demo Video

🔗 [Watch the demo on LinkedIn](https://www.linkedin.com/posts/himanshhhu47_movierecommendation-machinelearning-python-activity-7330609055511564291-F8Oq?utm_source=share&utm_medium=member_android&rcm=ACoAADoJJvQB1zf77ODWBj6fT6M0X1U-0MymkkE)

