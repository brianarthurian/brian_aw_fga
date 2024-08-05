import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import webbrowser
import subprocess

# Fungsi untuk mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM series')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fungsi untuk menampilkan bar chart jumlah series per tahun
def show_bar_chart():
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT release_year, COUNT(*) FROM series
    GROUP BY release_year
    ORDER BY release_year
    ''')
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("No Data", "Tidak ada data yang ditampilkan.")
        return

    years, counts = zip(*data)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(years, counts, color='skyblue')
    plt.xlabel('Tahun Rilis')
    plt.ylabel('Jumlah Series')
    plt.title('Jumlah Series Per Tahun')
    plt.xticks(rotation=45)

    # Menambahkan tooltip
    mplcursors.cursor(bars, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{years[sel.index]}: {counts[sel.index]}"))

    chart_window = tk.Toplevel(root)
    chart_window.title("Chart Tahun Rilis")
    canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Fungsi untuk menampilkan pie chart jumlah series berdasarkan genre
def show_genre_pie_chart():
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT genre, COUNT(*) FROM series
    GROUP BY genre
    ORDER BY COUNT(*) DESC
    ''')
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("No Data", "Tidak ada data yang ditampilkan.")
        return

    genres, counts = zip(*data)
    plt.figure(figsize=(10, 6))
    plt.pie(counts, labels=genres, autopct='%1.1f%%', colors=plt.cm.Paired(range(len(genres))))
    plt.title('Presentasi Series per Genre')

    chart_window = tk.Toplevel(root)
    chart_window.title("Presentase per Genre")
    canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Fungsi untuk menampilkan bar chart genre dengan rating terbaik
def show_genre_rating_chart():
    conn = sqlite3.connect('netflix.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT genre, AVG(rating) FROM series
    GROUP BY genre
    ORDER BY AVG(rating) DESC
    ''')
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("No Data", "Tidak ada data yang ditampilkan.")
        return

    genres, avg_ratings = zip(*data)
    plt.figure(figsize=(10, 6))
    bars = plt.barh(genres, avg_ratings, color='skyblue')
    plt.xlabel('Rata-rata Rating')
    plt.ylabel('Genre')
    plt.title('Rata-rata Rating Tiap Genre')

    # Menambahkan tooltip
    mplcursors.cursor(bars, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{genres[sel.index]}: {avg_ratings[sel.index]:.2f}"))

    chart_window = tk.Toplevel(root)
    chart_window.title("Chart Rating per Genre")
    canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Fungsi untuk membuka PDF
def open_pdf():
    pdf_path = 'FINAL TASK FGA BRIAN ARTHUR WILLIAM.pdf'  # Ganti dengan path ke file PDF Anda
    webbrowser.open_new(pdf_path)

# Fungsi untuk membuka situs web sumber data
def open_website():
    url = 'https://www.kaggle.com/datasets/harshdipsaha/netflix-web-series'  # Ganti dengan URL situs web Anda
    webbrowser.open(url)

# Fungsi untuk menjalankan edit_data.py
def open_edit():
    subprocess.Popen(["python", "edit_data.py"])

# Buat jendela utama
root = tk.Tk()
root.title("Visualisasi Netflix Webseries Dataset")

# Frame untuk menampung tombol
button_frame = tk.Frame(root)
button_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

# Tombol untuk mengedit data
edit_button = tk.Button(button_frame, text="Edit Data", command=open_edit)
edit_button.pack(fill=tk.X, pady=5)

# Tombol untuk menampilkan bar chart jumlah series per tahun
chart_button = tk.Button(button_frame, text="Chart Tahun Rilis", command=show_bar_chart)
chart_button.pack(fill=tk.X, pady=5)

# Tombol untuk menampilkan pie chart jumlah series berdasarkan genre
genre_pie_button = tk.Button(button_frame, text="Chart Presentase Genre", command=show_genre_pie_chart)
genre_pie_button.pack(fill=tk.X, pady=5)

# Tombol untuk menampilkan bar chart genre dengan rating terbaik
genre_rating_button = tk.Button(button_frame, text="Chart Rating per Genre", command=show_genre_rating_chart)
genre_rating_button.pack(fill=tk.X, pady=5)

# Tombol untuk membuka PDF
pdf_button = tk.Button(button_frame, text="Buka PDF", command=open_pdf)
pdf_button.pack(fill=tk.X, pady=5)

# Tombol untuk membuka website sumber data
website_button = tk.Button(button_frame, text="Sumber Data", command=open_website)
website_button.pack(fill=tk.X, pady=5)

# Tombol untuk keluar
exit_button = tk.Button(button_frame, text="Exit", command=root.quit)
exit_button.pack(fill=tk.X, pady=5)

# Jalankan aplikasi Tkinter
root.mainloop()
