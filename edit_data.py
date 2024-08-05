import sqlite3
import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

# Koneksi ke SQLite
def create_table():
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS series (
        id INTEGER PRIMARY KEY,
        series_name TEXT,
        rating REAL,
        total_watches INTEGER,
        genre TEXT,
        release_year INTEGER,
        average_watch_time REAL,
        total_seasons INTEGER,
        country_of_origin TEXT,
        language TEXT,
        lead_actor TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Koneksi ke MySQL/MariaDB
def get_mysql_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',          # Ganti dengan username MySQL/MariaDB Anda
        password='',          # Ganti dengan password MySQL/MariaDB Anda
        database='netflix_webseries'  # Ganti dengan nama database MySQL/MariaDB Anda
    )

# Tambahkan series ke SQLite dan MySQL
def add_series():
    series_name = entry_series_name.get()
    rating = float(entry_rating.get())
    total_watches = int(entry_total_watches.get())
    genre = entry_genre.get()
    release_year = int(entry_release_year.get())
    average_watch_time = float(entry_average_watch_time.get())
    total_seasons = int(entry_total_seasons.get())
    country_of_origin = entry_country_of_origin.get()
    language = entry_language.get()
    lead_actor = entry_lead_actor.get()

    # Koneksi ke SQLite
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO series (series_name, rating, total_watches, genre, release_year, 
                        average_watch_time, total_seasons, country_of_origin, language, lead_actor) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (series_name, rating, total_watches, genre, release_year, average_watch_time, total_seasons, country_of_origin, language, lead_actor))
    conn.commit()
    conn.close()

    # Koneksi ke MySQL/MariaDB
    mysql_conn = get_mysql_connection()
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute('''
    INSERT INTO series (series_name, rating, total_watches, genre, release_year, 
                        average_watch_time, total_seasons, country_of_origin, language, lead_actor) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (series_name, rating, total_watches, genre, release_year, average_watch_time, total_seasons, country_of_origin, language, lead_actor))
    mysql_conn.commit()
    mysql_conn.close()

    messagebox.showinfo("Info", "Series telah ditambahkan!")
    load_data()  # Reload data after adding a series

# Hapus series dari SQLite dan MySQL
def delete_series():
    series_name = entry_delete_series_name.get()

    # Hapus dari SQLite
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM series WHERE series_name = ?', (series_name,))
    conn.commit()
    conn.close()

    # Hapus dari MySQL/MariaDB
    mysql_conn = get_mysql_connection()
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute('DELETE FROM series WHERE series_name = %s', (series_name,))
    mysql_conn.commit()
    mysql_conn.close()

    messagebox.showinfo("Info", "Series deleted successfully!")
    load_data()  # Reload data after deleting a series

# Hapus semua series dari SQLite dan MySQL
def delete_all_series():
    # Hapus dari SQLite
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM series')
    conn.commit()
    conn.close()

    # Hapus dari MySQL/MariaDB
    mysql_conn = get_mysql_connection()
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute('DELETE FROM series')
    mysql_conn.commit()
    mysql_conn.close()

    messagebox.showinfo("Info", "All series deleted successfully!")
    load_data()  # Reload data after deleting all series

# Update series di SQLite dan MySQL
def update_series():
    series_name = entry_series_name.get()
    rating = float(entry_rating.get())
    total_watches = int(entry_total_watches.get())
    genre = entry_genre.get()
    release_year = int(entry_release_year.get())
    average_watch_time = float(entry_average_watch_time.get())
    total_seasons = int(entry_total_seasons.get())
    country_of_origin = entry_country_of_origin.get()
    language = entry_language.get()
    lead_actor = entry_lead_actor.get()

    # Update di SQLite
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE series
    SET rating = ?, total_watches = ?, genre = ?, release_year = ?, 
        average_watch_time = ?, total_seasons = ?, country_of_origin = ?, 
        language = ?, lead_actor = ?
    WHERE series_name = ?
    ''', (rating, total_watches, genre, release_year, average_watch_time, total_seasons, country_of_origin, language, lead_actor, series_name))
    conn.commit()
    conn.close()

    # Update di MySQL/MariaDB
    mysql_conn = get_mysql_connection()
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute('''
    UPDATE series
    SET rating = %s, total_watches = %s, genre = %s, release_year = %s, 
        average_watch_time = %s, total_seasons = %s, country_of_origin = %s, 
        language = %s, lead_actor = %s
    WHERE series_name = %s
    ''', (rating, total_watches, genre, release_year, average_watch_time, total_seasons, country_of_origin, language, lead_actor, series_name))
    mysql_conn.commit()
    mysql_conn.close()

    messagebox.showinfo("Info", "Series updated successfully!")
    load_data()  # Reload data after updating a series

# Load data from SQLite and display it in the Treeview
def load_data():
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM series')
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert('', 'end', values=row)

# Search for series based on the search query
def search_series():
    search_query = entry_search.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM series WHERE series_name LIKE ?', ('%' + search_query + '%',))
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert('', 'end', values=row)

# GUI untuk aplikasi
def create_gui():
    global tree  # Declare tree as a global variable

    root = tk.Tk()
    root.title("Netflix Series Manager")

    # Search box
    tk.Label(root, text="Search Series:", anchor='e').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    global entry_search
    entry_search = tk.Entry(root)
    entry_search.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    tk.Button(root, text="Search", command=search_series).grid(row=0, column=2, padx=5, pady=5)

    # Treeview and scrollbar
    global tree
    tree = ttk.Treeview(root, columns=(
        'id', 'series_name', 'rating', 'total_watches', 'genre', 'release_year',
        'average_watch_time', 'total_seasons', 'country_of_origin', 'language', 'lead_actor'
    ), show='headings')

    for col in tree['columns']:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

    vsb = tk.Scrollbar(root, orient='vertical', command=tree.yview)
    vsb.grid(row=1, column=3, sticky='ns')
    tree.configure(yscrollcommand=vsb.set)

    hs = tk.Scrollbar(root, orient='horizontal', command=tree.xview)
    hs.grid(row=2, column=0, columnspan=3, sticky='ew')
    tree.configure(xscrollcommand=hs.set)

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Define labels and their positions
    labels = [
        "Series Name:",
        "Rating:",
        "Total Watches:",
        "Genre:",
        "Release Year:",
        "Average Watch Time (minutes):",
        "Total Seasons:",
        "Country of Origin:",
        "Language:",
        "Lead Actor:"
    ]

    # Create and place labels in the grid
    for idx, text in enumerate(labels):
        tk.Label(root, text=text, anchor='e').grid(row=idx + 3, column=0, sticky='e', padx=5, pady=5)

    # Create entry widgets
    global entry_series_name, entry_rating, entry_total_watches, entry_genre, entry_release_year
    global entry_average_watch_time, entry_total_seasons, entry_country_of_origin, entry_language
    global entry_lead_actor, entry_delete_series_name

    entry_series_name = tk.Entry(root)
    entry_rating = tk.Entry(root)
    entry_total_watches = tk.Entry(root)
    entry_genre = tk.Entry(root)
    entry_release_year = tk.Entry(root)
    entry_average_watch_time = tk.Entry(root)
    entry_total_seasons = tk.Entry(root)
    entry_country_of_origin = tk.Entry(root)
    entry_language = tk.Entry(root)
    entry_lead_actor = tk.Entry(root)

    # Place entry widgets in the grid
    entries = [
        entry_series_name,
        entry_rating,
        entry_total_watches,
        entry_genre,
        entry_release_year,
        entry_average_watch_time,
        entry_total_seasons,
        entry_country_of_origin,
        entry_language,
        entry_lead_actor
    ]

    for idx, entry in enumerate(entries):
        entry.grid(row=idx + 3, column=1, padx=5, pady=5, sticky='w')

    tk.Button(root, text="Add Series", command=add_series).grid(row=len(labels) + 3, column=0, columnspan=2, pady=10)
    tk.Button(root, text="Update Series", command=update_series).grid(row=len(labels) + 4, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Series Name to Delete:", anchor='e').grid(row=len(labels) + 5, column=0, sticky='e', padx=5, pady=5)
    entry_delete_series_name = tk.Entry(root)
    entry_delete_series_name.grid(row=len(labels) + 5, column=1, padx=5, pady=5, sticky='w')
    tk.Button(root, text="Delete Series", command=delete_series).grid(row=len(labels) + 6, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Delete All Series", command=delete_all_series).grid(row=len(labels) + 7, column=0, columnspan=2, pady=10)

    load_data()  # Load data when the application starts

    root.mainloop()

if __name__ == '__main__':
    create_gui()
