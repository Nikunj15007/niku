import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationEngine:
    """Content-based recommender using TF-IDF and cosine similarity."""

    def __init__(self, movies: pd.DataFrame):
        self.movies = movies.copy()
        self.movies["content"] = (
            self.movies["genres"] + " " + self.movies["keywords"] + " " +
            self.movies["overview"] + " " + self.movies["cast"] + " " +
            self.movies["director"]
        ).fillna("")
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=15000)
        self.matrix = self.vectorizer.fit_transform(self.movies["content"])
        self.similarity = cosine_similarity(self.matrix)
        self._title_map = {self._normalize_title(t): i for i, t in enumerate(self.movies["title"])}

    @staticmethod
    def _normalize_title(title):
        return re.sub(r"[^a-z0-9]+", " ", str(title).lower()).strip()

    def search(self, query, limit=8):
        query = self._normalize_title(query)
        if not query:
            return self.movies.iloc[0:0]
        exact = self.movies[self.movies["title"].map(self._normalize_title) == query]
        if not exact.empty:
            return exact.head(limit)
        mask = self.movies["title"].map(self._normalize_title).str.contains(re.escape(query), regex=True, na=False)
        matches = self.movies[mask].copy()
        if matches.empty:
            words = query.split()
            mask = self.movies["title"].map(self._normalize_title).apply(lambda x: all(w in x for w in words))
            matches = self.movies[mask].copy()
        return matches.head(limit)

    def find_index(self, title):
        normalized = self._normalize_title(title)
        if normalized in self._title_map:
            return self._title_map[normalized]
        results = self.search(title, 1)
        return int(results.index[0]) if not results.empty else None

    def recommend(self, title, n=10, genre=None, sort_by_rating=False):
        index = self.find_index(title)
        if index is None:
            return self.movies.iloc[0:0].copy()
        scores = self.similarity[index]
        result = self.movies.copy()
        result["similarity"] = scores
        result = result.drop(index=index, errors="ignore")
        if genre and genre != "All Genres":
            result = result[result["genres"].str.contains(re.escape(genre), case=False, na=False)]
        result = result.sort_values("similarity", ascending=False).head(max(n * 3, n))
        if sort_by_rating:
            result = result.sort_values(["rating", "similarity"], ascending=False)
        return result.head(n)
