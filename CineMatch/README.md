# CineMatch – A Python-Based Movie Recommendation System

CineMatch is a college-level Python mini-project that recommends movies using **content-based filtering**, **TF-IDF vectorization**, and **cosine similarity**. It has a Tkinter desktop GUI, SQLite favorites/history, CSV data loading, and a Matplotlib statistics chart.

## 1. Features

- Dark cinematic Tkinter interface
- Movie title search with case/spelling-tolerant matching
- Movie details: genre, rating, year, overview, director and cast
- Top 10 content-based recommendations
- Genre discovery and rating-based sorting
- Similarity percentage for recommendations
- SQLite favorites and watch history
- Dataset statistics and genre chart
- Graceful messages for empty search, missing data and database errors
- Works with a bundled sample CSV, so the project can be demonstrated immediately

## 2. Folder structure

```text
CineMatch/
├── main.py
├── recommendation_engine.py
├── database.py
├── data_loader.py
├── gui.py
├── requirements.txt
├── README.md
└── data/
    └── movies.csv
```

`cinematch.db` is created automatically after the first run. It does not need to be created manually.

## 3. Dataset

The included `data/movies.csv` is a small demonstration dataset. For a larger project, replace it with a suitable movie CSV such as the TMDB 5000 Movie Dataset after obtaining it from its legitimate source.

The loader expects at minimum:

- `title`

It can use these optional columns:

- `genres` or `genre`
- `keywords` or `keyword`
- `overview`, `description` or `plot`
- `cast`, `actors` or `stars`
- `director`
- `rating`, `vote_average` or `imdb_rating`
- `release_year`, `year` or `release_date`

The loader also accepts common list formats such as Python-list text or comma/pipe-separated values. If your dataset uses different names, edit the lists in `_first_column()` inside `data_loader.py`.

## 4. Installation

Python 3.10+ is recommended.

Open a terminal in the `CineMatch` folder:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Tkinter is normally included with standard Python on Windows. On some Linux distributions it must be installed separately through the operating system package manager.

## 5. Run

```bash
python main.py
```

Search for a sample movie such as `Inception`, `Interstellar`, `The Matrix`, or `La La Land`.

## 6. How the recommendation algorithm works

1. The CSV is loaded into a Pandas DataFrame.
2. Genre, keywords, overview, cast and director are combined into one text field.
3. `TfidfVectorizer` converts each movie's text into a numerical vector.
4. Cosine similarity compares the selected movie vector with all other movie vectors.
5. Movies are ranked by similarity score.
6. The top results are shown in the GUI.

A simple way to explain cosine similarity in viva is: it measures how similar two text vectors are by comparing the angle between them. A score closer to 1 means more similar.

## 7. Major files

### `main.py`
Loads the dataset, creates the recommendation engine and database, and starts the GUI.

### `data_loader.py`
Reads the CSV, validates the title field, maps common column names, cleans missing values and converts list-like metadata into text.

### `recommendation_engine.py`
Contains the main recommendation logic. It builds TF-IDF vectors and a cosine-similarity matrix, then searches titles and returns recommendations.

### `database.py`
Creates two SQLite tables: `favorites` and `history`. It provides simple functions to add/remove favorites and record/read history.

### `gui.py`
Contains the Tkinter interface, search, movie details, recommendation display, genre discovery, favorites/history windows and statistics graph.

## 8. Technologies used

- **Python:** main programming language
- **Pandas:** CSV loading and data cleaning
- **NumPy:** numerical ecosystem used with the ML stack
- **Scikit-learn:** TF-IDF and cosine similarity
- **Tkinter:** desktop GUI
- **SQLite:** local favorites/history storage
- **Matplotlib:** statistics visualization

## 9. Problem statement

Movie platforms contain thousands of titles, making it difficult for users to decide what to watch. CineMatch solves this problem by analyzing movie metadata and recommending titles similar to a movie the user already likes.

## 10. Objectives

1. Build a simple local movie recommendation application.
2. Implement content-based filtering using TF-IDF and cosine similarity.
3. Provide a student-friendly GUI for searching and discovering movies.
4. Store favorites and watch history using SQLite.
5. Display basic dataset statistics with a graph.

## 11. Methodology

**Dataset → Cleaning → Feature Combination → TF-IDF → Cosine Similarity → Ranking → GUI Recommendations → Favorites/History**

## 12. Architecture / block diagram

```text
+-------------------+
|    CSV Dataset    |
+---------+---------+
          |
          v
+-------------------+
|   Data Loader     |
| Pandas + Cleaning |
+---------+---------+
          |
          v
+-------------------+
| Feature Combining |
| genre/keywords/   |
| overview/cast/    |
| director          |
+---------+---------+
          |
          v
+-------------------+
| TF-IDF Vectorizer |
+---------+---------+
          |
          v
+-------------------+
| Cosine Similarity |
+---------+---------+
          |
          v
+-------------------+
| Recommendation    |
| Ranking / Filter  |
+---------+---------+
          |
          v
+-------------------+
| Tkinter GUI       |
+----+----------+---+
     |          |
     v          v
 SQLite      Matplotlib
 Favorites   Statistics
 History
```

## 13. Viva-friendly concepts

### What is a recommendation system?
A recommendation system is a program that predicts or suggests items a user may like based on available information.

### What is content-based filtering?
It recommends items that have similar characteristics to an item the user already selected. CineMatch compares movie content rather than depending on ratings from other users.

### What is TF-IDF?
TF-IDF stands for Term Frequency–Inverse Document Frequency. It converts text into numbers while giving higher importance to words that are useful for distinguishing documents.

### What is cosine similarity?
It measures similarity between two vectors using the cosine of the angle between them. Similar movies receive higher similarity scores.

### Why Pandas?
Pandas makes CSV loading, cleaning, filtering and sorting easy through DataFrames.

### Why NumPy?
NumPy provides efficient numerical arrays and is part of the scientific Python ecosystem used by the machine-learning stack.

### Why Scikit-learn?
It provides ready-to-use and reliable implementations of TF-IDF vectorization and cosine similarity.

### Why Tkinter?
Tkinter is included with standard Python installations on many systems and is sufficient for a local desktop GUI without introducing a web framework.

### Why SQLite?
SQLite stores favorites and history in a small local database file without requiring a separate database server.

## 14. What happens when a user searches?

The program checks the search box, finds a matching title, displays its metadata, stores the selected title in history, creates or uses its TF-IDF representation, compares it with the other movies, ranks the similarity scores, and displays the best matching movies.

## 15. Hardware requirements

- Normal college laptop/desktop
- 4 GB RAM or more recommended
- At least 500 MB free storage
- Keyboard and mouse/trackpad

## 16. Software requirements

- Windows, Linux or macOS
- Python 3.10+ recommended
- pip
- Required Python packages from `requirements.txt`

## 17. Expected output

The application opens with a dark cinematic dashboard. The user can search for a movie, read its details, view similar movies with similarity percentages, filter by genre, save favorites, review history, and open a genre statistics chart.

## 18. Advantages

- Easy to understand and demonstrate
- Fast recommendations after model preparation
- No internet/API required for core functionality
- No external poster or image dependency
- Uses real machine-learning concepts
- Data can be replaced with a larger CSV

## 19. Limitations

- Recommendations depend on the quality of movie metadata.
- It does not learn from multiple users' preferences.
- It is content-based, so it can recommend movies that are similar but not necessarily personally interesting.
- A very large dataset increases memory usage because the similarity matrix is calculated in memory.

## 20. Future scope

- Add movie posters through an optional API
- Add collaborative filtering
- Add user login/profiles
- Add hybrid recommendation combining content and ratings
- Add advanced fuzzy title matching
- Add a web/mobile interface
- Add model evaluation metrics

## 21. 12-day development plan

| Day | Work |
|---|---|
| 1 | Project planning, choose dataset, define CSV format |
| 2 | Data preprocessing, missing values and metadata cleaning |
| 3 | Build TF-IDF and cosine-similarity recommendation engine |
| 4 | Test recommendation quality with different movie titles |
| 5 | Design the dark Tkinter GUI |
| 6 | Add search and title matching |
| 7 | Add movie details and recommendation display |
| 8 | Add SQLite favorites and watch history |
| 9 | Add statistics and Matplotlib graph |
| 10 | Integrate all modules and improve error handling |
| 11 | Test edge cases, fix bugs and polish the interface |
| 12 | Final documentation, PPT, report, viva practice and demo |

## 22. Suggested PPT structure

1. Title – CineMatch
2. Problem Statement
3. Objectives
4. Existing Problem / Motivation
5. Dataset and Features
6. Content-Based Recommendation
7. TF-IDF
8. Cosine Similarity
9. System Architecture / Block Diagram
10. GUI Screenshots
11. Favorites, History and Statistics
12. Results / Sample Recommendations
13. Advantages and Limitations
14. Future Scope
15. Conclusion
16. References

## 23. Suggested project report structure

1. Cover Page
2. Certificate/Declaration if required by college
3. Abstract
4. Introduction
5. Problem Statement
6. Objectives
7. Literature/Technology Overview
8. Dataset Description
9. Methodology
10. System Architecture
11. Module Description
12. Algorithm / TF-IDF and Cosine Similarity
13. Implementation
14. GUI Screenshots
15. Database Design
16. Results and Discussion
17. Advantages
18. Limitations
19. Future Scope
20. Conclusion
21. References
22. Appendix / Code

## 24. Common viva questions

**Q: Is this collaborative filtering?**  
A: No. It is content-based filtering because recommendations are generated from movie metadata.

**Q: Why combine multiple fields?**  
A: Genre alone is too broad. Combining genres, keywords, overview, cast and director gives a richer description of each movie.

**Q: Why remove English stop words?**  
A: Common words such as “the” and “and” usually carry little information for comparing movies.

**Q: What does a 75% similarity mean?**  
A: It is the cosine similarity score converted to a percentage for easier display. It is not a probability that the user will like the movie.

**Q: Why not use deep learning?**  
A: The goal is a manageable 12-day college project. TF-IDF and cosine similarity demonstrate the recommendation concept clearly with fewer resources.

**Q: Where is user data stored?**  
A: Favorites and watch history are stored locally in the SQLite file `cinematch.db`.

**Q: What happens if the CSV is missing?**  
A: `data_loader.py` raises a clear file-not-found error instead of failing silently.
