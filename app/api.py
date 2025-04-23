from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from content_based import recommend_movie

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to SuggestIO API!"}

@app.get("/recommend")
def get_recommendations(title: str, top_n: int = 5):
    recommendations = recommend_movie(title, top_n)
    if not recommendations:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"recommendations": recommendations}
