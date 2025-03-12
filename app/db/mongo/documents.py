from typing import List
from beanie import Document

class Moovie(Document):
    title: str
    release_year: int
    director: List[str]
    plot: str
    genres: List[str]
    starring: List[str]
    imdb_link: str
    imdb_rating: float
    posted: bool = False

    class Settings:
        name = "moovies"