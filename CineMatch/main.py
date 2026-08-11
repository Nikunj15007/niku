from gui import CineMatchApp
from data_loader import load_movies
from recommendation_engine import RecommendationEngine
from database import Database


def main():
    try:
        movies = load_movies()
    except Exception as exc:
        print(f"Could not load movie data: {exc}")
        return

    engine = RecommendationEngine(movies)
    database = Database()
    app = CineMatchApp(movies, engine, database)
    app.run()


if __name__ == "__main__":
    main()
