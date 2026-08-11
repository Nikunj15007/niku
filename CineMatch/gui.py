import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
import matplotlib.pyplot as plt


BG = "#0b1020"
PANEL = "#151c31"
CARD = "#1d2740"
TEXT = "#f4f6fb"
MUTED = "#aab4cc"
ACCENT = "#e5b94e"


class CineMatchApp:
    def __init__(self, movies, engine, database):
        self.movies = movies
        self.engine = engine
        self.db = database
        self.selected_title = None
        self.root = tk.Tk()
        self.root.title("CineMatch – Movie Recommendation System")
        self.root.geometry("1180x760")
        self.root.minsize(980, 650)
        self.root.configure(bg=BG)
        self._build_style()
        self._build_ui()
        self._refresh_genres()

    def _build_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=CARD, background=CARD, foreground=TEXT, arrowcolor=ACCENT)
        style.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=TEXT, rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", background=PANEL, foreground=ACCENT, font=("Segoe UI", 10, "bold"))

    def _label(self, parent, text, size=11, color=TEXT, bold=False):
        return tk.Label(parent, text=text, bg=parent.cget("bg"), fg=color,
                        font=("Segoe UI", size, "bold" if bold else "normal"))

    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=28, pady=(24, 12))
        self._label(header, "CineMatch", 28, ACCENT, True).pack(anchor="w")
        self._label(header, "Find your next favorite movie", 12, MUTED).pack(anchor="w")

        controls = tk.Frame(self.root, bg=PANEL, padx=16, pady=14)
        controls.pack(fill="x", padx=28, pady=8)
        self.search_var = tk.StringVar()
        entry = tk.Entry(controls, textvariable=self.search_var, bg=CARD, fg=TEXT, insertbackground=TEXT,
                         relief="flat", font=("Segoe UI", 12))
        entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 10))
        entry.bind("<Return>", lambda _: self.search_movie())
        tk.Button(controls, text="Search", command=self.search_movie, bg=ACCENT, fg="#111111",
                  relief="flat", font=("Segoe UI", 10, "bold"), padx=18, pady=9).pack(side="left")
        self.genre_var = tk.StringVar(value="All Genres")
        self.genre_box = ttk.Combobox(controls, textvariable=self.genre_var, state="readonly", width=18)
        self.genre_box.pack(side="left", padx=(12, 0))
        self.genre_box.bind("<<ComboboxSelected>>", lambda _: self.genre_discovery())

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=28, pady=8)
        left = tk.Frame(body, bg=PANEL, padx=18, pady=18)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        right = tk.Frame(body, bg=PANEL, padx=18, pady=18)
        right.pack(side="right", fill="both", expand=True, padx=(8, 0))

        self._label(left, "Movie Details", 16, ACCENT, True).pack(anchor="w")
        self.details = tk.Text(left, bg=PANEL, fg=TEXT, relief="flat", wrap="word", font=("Segoe UI", 10), height=16)
        self.details.pack(fill="both", expand=True, pady=12)
        self.details.configure(state="disabled")
        buttons = tk.Frame(left, bg=PANEL)
        buttons.pack(fill="x")
        tk.Button(buttons, text="♡ Add Favorite", command=self.toggle_favorite, bg=CARD, fg=TEXT, relief="flat", padx=12, pady=8).pack(side="left")
        tk.Button(buttons, text="Favorites", command=self.show_favorites, bg=CARD, fg=TEXT, relief="flat", padx=12, pady=8).pack(side="left", padx=8)
        tk.Button(buttons, text="History", command=self.show_history, bg=CARD, fg=TEXT, relief="flat", padx=12, pady=8).pack(side="left")
        tk.Button(buttons, text="Statistics", command=self.show_statistics, bg=CARD, fg=TEXT, relief="flat", padx=12, pady=8).pack(side="right")

        self._label(right, "Recommendations", 16, ACCENT, True).pack(anchor="w")
        self.result_list = tk.Listbox(right, bg=CARD, fg=TEXT, selectbackground=ACCENT, selectforeground="#111111",
                                      relief="flat", font=("Segoe UI", 10), activestyle="none")
        self.result_list.pack(fill="both", expand=True, pady=12)
        self.result_list.bind("<<ListboxSelect>>", self.select_result)
        self.status = self._label(self.root, "Ready", 9, MUTED)
        self.status.pack(anchor="w", padx=30, pady=(0, 12))

    def _refresh_genres(self):
        counter = Counter()
        for genres in self.movies["genres"]:
            for genre in str(genres).split(","):
                genre = genre.strip()
                if genre:
                    counter[genre] += 1
        preferred = ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller", "Animation"]
        available = [g for g in preferred if g in counter] + [g for g in counter if g not in preferred]
        self.genre_box["values"] = ["All Genres"] + available

    def search_movie(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Search", "Please enter a movie name.")
            return
        matches = self.engine.search(query)
        self.result_list.delete(0, tk.END)
        if matches.empty:
            self.status.config(text="No movie found. Try another spelling or title.")
            return
        for title in matches["title"]:
            self.result_list.insert(tk.END, title)
        self.result_list.selection_set(0)
        self.select_result()

    def select_result(self, _event=None):
        selection = self.result_list.curselection()
        if not selection:
            return
        title = self.result_list.get(selection[0])
        self.selected_title = title
        row = self.movies[self.movies["title"] == title].iloc[0]
        text = (f"{row['title']}\n\nGenre: {row['genres'] or 'N/A'}\n"
                f"Rating: {row['rating']:.1f}\nRelease Year: {row['release_year'] or 'N/A'}\n"
                f"Director: {row['director'] or 'N/A'}\nCast: {row['cast'] or 'N/A'}\n\n"
                f"Overview\n{row['overview'] or 'No overview available.'}")
        self.details.configure(state="normal")
        self.details.delete("1.0", tk.END)
        self.details.insert(tk.END, text)
        self.details.configure(state="disabled")
        try:
            self.db.add_history(title)
            recommendations = self.engine.recommend(title, 10, self.genre_var.get())
            self.result_list.delete(0, tk.END)
            for _, movie in recommendations.iterrows():
                self.result_list.insert(tk.END, f"{movie['title']}  |  {movie['release_year']}  |  ★ {movie['rating']:.1f}  |  {movie['similarity'] * 100:.1f}%")
            self.status.config(text=f"Recommendations generated for {title}")
        except Exception as exc:
            messagebox.showerror("Recommendation Error", str(exc))

    def genre_discovery(self):
        genre = self.genre_var.get()
        self.result_list.delete(0, tk.END)
        if genre == "All Genres":
            data = self.movies.sort_values("rating", ascending=False).head(20)
        else:
            data = self.movies[self.movies["genres"].str.contains(genre, case=False, na=False)].sort_values("rating", ascending=False).head(20)
        for _, row in data.iterrows():
            self.result_list.insert(tk.END, f"{row['title']}  |  {row['release_year']}  |  ★ {row['rating']:.1f}")
        self.status.config(text=f"Showing {len(data)} movies in {genre}")

    def toggle_favorite(self):
        if not self.selected_title:
            messagebox.showinfo("Favorites", "Select a movie first.")
            return
        try:
            if self.db.is_favorite(self.selected_title):
                self.db.remove_favorite(self.selected_title)
                messagebox.showinfo("Favorites", "Removed from favorites.")
            else:
                self.db.add_favorite(self.selected_title)
                messagebox.showinfo("Favorites", "Added to favorites.")
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))

    def show_favorites(self):
        self._show_list_window("Favorites", self.db.get_favorites())

    def show_history(self):
        self._show_list_window("Watch History", [f"{title} — {date}" for title, date in self.db.get_history()])

    def _show_list_window(self, title, items):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("500x450")
        win.configure(bg=BG)
        tk.Label(win, text=title, bg=BG, fg=ACCENT, font=("Segoe UI", 18, "bold")).pack(pady=18)
        box = tk.Listbox(win, bg=CARD, fg=TEXT, relief="flat", font=("Segoe UI", 10))
        box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        for item in items:
            box.insert(tk.END, item)
        if not items:
            box.insert(tk.END, "Nothing here yet.")

    def show_statistics(self):
        try:
            avg = self.movies["rating"].mean()
            counts = Counter()
            for genres in self.movies["genres"]:
                for genre in str(genres).split(","):
                    if genre.strip():
                        counts[genre.strip()] += 1
            top = counts.most_common(8)
            messagebox.showinfo("CineMatch Statistics", f"Total movies: {len(self.movies)}\nAverage rating: {avg:.2f}\nMost common genre: {top[0][0] if top else 'N/A'}")
            if top:
                labels, values = zip(*top)
                plt.figure(figsize=(8, 4.5))
                plt.bar(labels, values)
                plt.title("Movies by Genre")
                plt.ylabel("Number of Movies")
                plt.xticks(rotation=30, ha="right")
                plt.tight_layout()
                plt.show()
        except Exception as exc:
            messagebox.showerror("Statistics Error", str(exc))

    def run(self):
        self.root.mainloop()
