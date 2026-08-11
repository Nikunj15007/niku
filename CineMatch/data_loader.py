from pathlib import Path
import ast
import json
import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "movies.csv"


def _parse_list(value):
    if pd.isna(value) or str(value).strip() == "":
        return []
    text = str(value).strip()
    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list):
            return [str(x.get("name", x)) if isinstance(x, dict) else str(x) for x in parsed]
    except (ValueError, SyntaxError):
        pass
    return [part.strip() for part in text.replace("|", ",").split(",") if part.strip()]


def _first_column(df, names, default=""):
    for name in names:
        if name in df.columns:
            return df[name]
    return pd.Series([default] * len(df), index=df.index)


def load_movies(path=DATA_PATH):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}. Put movies.csv inside CineMatch/data/")

    df = pd.read_csv(path)
    if "title" not in df.columns:
        raise ValueError("Dataset must contain a 'title' column.")

    result = pd.DataFrame()
    result["title"] = df["title"].fillna("").astype(str)
    result["genres"] = _first_column(df, ["genres", "genre"]).apply(lambda x: ", ".join(_parse_list(x)))
    result["keywords"] = _first_column(df, ["keywords", "keyword"]).apply(lambda x: ", ".join(_parse_list(x)))
    result["overview"] = _first_column(df, ["overview", "description", "plot"]).fillna("").astype(str)
    result["cast"] = _first_column(df, ["cast", "actors", "stars"]).apply(lambda x: ", ".join(_parse_list(x)))
    result["director"] = _first_column(df, ["director", "Director"]).fillna("").astype(str)
    result["rating"] = pd.to_numeric(_first_column(df, ["rating", "vote_average", "imdb_rating"], 0), errors="coerce").fillna(0)
    result["release_year"] = _first_column(df, ["release_year", "year", "release_date"], "").astype(str).str[:4]
    result["release_year"] = result["release_year"].replace({"nan": "", "0.0": ""})
    result = result[result["title"].str.strip() != ""].drop_duplicates("title").reset_index(drop=True)
    return result
