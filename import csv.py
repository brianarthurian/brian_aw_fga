import sqlite3
import csv
import mysql.connector

# Fungsi untuk membuat tabel SQLite dan mengisi data dari CSV
def setup_sqlite_database():
    # Buat dan hubungkan ke database SQLite
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()

    # Buat tabel baru
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

    # Baca data dari CSV dan masukkan ke dalam tabel
    with open('netflix_series_10_columns_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = [(row['Series Name'], row['Rating'], row['Total Watches'], row['Genre'], 
                 row['Release Year'], row['Average Watch Time (minutes)'], row['Total Seasons'], 
                 row['Country of Origin'], row['Language'], row['Lead Actor']) for row in reader]

    # Memasukkan data
    cursor.executemany('''
    INSERT INTO series (series_name, rating, total_watches, genre, release_year, 
                        average_watch_time, total_seasons, country_of_origin, language, lead_actor) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)

    # Simpan perubahan dan tutup koneksi
    conn.commit()
    conn.close()

# Fungsi untuk menyalin data dari SQLite ke MySQL/MariaDB
def migrate_data_to_mysql():
    # Koneksi ke SQLite
    sqlite_conn = sqlite3.connect('netflix.db')
    sqlite_cursor = sqlite_conn.cursor()

    # Koneksi ke MySQL/MariaDB
    mysql_conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='netflix_webseries'
    )
    mysql_cursor = mysql_conn.cursor()

    # Buat tabel baru di MySQL/MariaDB
    mysql_cursor.execute('''
    CREATE TABLE IF NOT EXISTS series (
        id INT AUTO_INCREMENT PRIMARY KEY,
        series_name VARCHAR(255),
        rating FLOAT,
        total_watches INT,
        genre VARCHAR(255),
        release_year INT,
        average_watch_time FLOAT,
        total_seasons INT,
        country_of_origin VARCHAR(255),
        language VARCHAR(255),
        lead_actor VARCHAR(255)
    )
    ''')

    # Baca data dari SQLite
    sqlite_cursor.execute('SELECT * FROM series')
    data = sqlite_cursor.fetchall()

    # Modifikasi data untuk menyesuaikan format (jika perlu)
    cleaned_data = [(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]) for row in data]

    # Masukkan data ke MySQL/MariaDB
    try:
        mysql_cursor.executemany('''
        INSERT INTO series (series_name, rating, total_watches, genre, release_year, 
                            average_watch_time, total_seasons, country_of_origin, language, lead_actor) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', cleaned_data)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    # Simpan perubahan dan tutup koneksi
    mysql_conn.commit()
    sqlite_conn.close()
    mysql_conn.close()

# Eksekusi fungsi
if __name__ == '__main__':
    setup_sqlite_database()
    migrate_data_to_mysql()
