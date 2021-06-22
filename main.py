import tkinter as tk
from tkinter import *
from tkinter import filedialog
import shutil

from pygame import mixer
import sqlite3
import os.path
from os import path


# delete db if it exists
if path.exists("SQLite_Python.db"):
    conn = sqlite3.connect("SQLite_Python.db")
    cursor = conn.cursor()
else:
    conn = sqlite3.connect("SQLite_Python.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE songs (path TEXT, city_id INTEGER, title TEXT, artist TEXT, description TEXT)")
    cursor.execute("CREATE TABLE cities (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO cities (name) VALUES('Paris')")
    cursor.execute("INSERT INTO cities (name) VALUES('Rome')")
    cursor.execute("INSERT INTO cities (name) VALUES('Berlin')")
    cursor.execute("INSERT INTO cities (name) VALUES('Barcelona')")
    cursor.execute("INSERT INTO cities (name) VALUES('Tbilisi')")
    cursor.execute(
        "INSERT INTO songs (path,city_id,title,artist,description) VALUES('La_vien_rose.mp3', 1, 'La_vien_rose', 'Edith Piaf', 'Released: 1947')")
    cursor.execute(
        "INSERT INTO songs (path,city_id,title,artist,description) VALUES('Di_doo_dah.mp3', 1, 'Di_doo_dah', 'Jane_Birkin', 'Released: 1973')")
    cursor.execute(
        "INSERT INTO songs (path,city_id,title,artist,description) VALUES('Heart_of_Rome.mp3', 2, 'Heart_of_Rome', 'Elvis Presley', 'Released: 1971')")
    cursor.execute(
        "INSERT INTO songs (path,city_id,title,artist,description) VALUES('Via_con_me.mp3', 2, 'Via_con_me', 'Paolo Conte', 'Released: 1998')")
    cursor.execute(
        "INSERT INTO songs (path,city_id,title,artist,description) VALUES('Deutschland.mp3', 3, 'Deutschland', 'Rammstein', 'Released: 2019')")
    cursor.execute(
        "INSERT INTO songs (path,city_id,title,artist,description) VALUES('Ohne_dich.mp3', 3, 'Ohne_dich', 'Ramsstein', 'Released: 2004')")
    cursor.execute(
        "INSERT INTO songs (path,city_id,title,artist,description) VALUES('Barcelona_1.mp3', 4, 'Barcelona_1', 'freddie mercury and montserrat caballé', 'Released: 1988')")
    cursor.execute(
        "INSERT INTO songs (path,city_id,title,artist,description) VALUES('Barcelona_2.mp3', 4, 'Barcelona_2', 'giulia y los tellarini', 'released:2008')")
    cursor.execute(
        "INSERT INTO songs (path,city_id,title,artist,description) VALUES('Tbiliso.mp3', 5, 'Tbiliso', 'Niaz Diasamidze', 'Released: 2005')")
    cursor.execute(
        "INSERT INTO songs (path,city_id,title,artist,description) VALUES('She_is_here.mp3', 5, 'She_is_here', 'Giya Kancheli', 'Released: 1974')")
    conn.commit()


if __name__ == '__main__':
    filepath = 'something'


    def play_song(song):
        cursor.execute("SELECT path FROM songs WHERE title = ?", (song,))
        song_path = cursor.fetchall()[0][0]
        mixer.init()
        mixer.music.load(song_path)
        mixer.music.play()


    def insert_songs(lb, cc):
        songs.delete(0, 'end')
        id = cursor.execute("SELECT id FROM cities WHERE name=?", (cc,)).fetchall()[0][0]
        rows = cursor.execute("SELECT title FROM songs WHERE city_id=?", (id,)).fetchall()
        for row in rows:
            lb.insert(0, row[0])


    def stop_song():
        mixer.music.stop()


    def add_city(city_name):
        if city_name:
            cursor.execute("INSERT INTO cities (name) VALUES(?)", (city_name,))
            conn.commit()
            new_city.delete(0, END)
            current_city.set(city_name)
            optMenu['menu'].add_command(label=city_name, command=tk._setit(current_city, city_name))


    def update_songs(*args):
        insert_songs(songs, current_city.get())


    def browse_files():
        global filepath
        filepath = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                              filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")))
        song_label.configure(text=os.path.basename(filepath))


    def upload_song():
        shutil.copy(filepath, os.getcwd())
        title = song_title_entry.get()
        song_title_entry.delete(0, END)
        artist = song_artist_entry.get()
        song_artist_entry.delete(0, END)
        description = song_description_entry.get()
        song_description_entry.delete(0, END)
        song_label.configure(text="choose an mp3 file")
        city_id = cursor.execute("SELECT id FROM cities WHERE name=?", (current_city.get(),)).fetchall()[0][0]
        cursor.execute("INSERT INTO songs (path,city_id,title,artist,description) VALUES(?, ?, ?, ?, ?)", (os.path.basename(filepath), city_id, title, artist, description))
        conn.commit()
        update_songs()


    root = Tk()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f'{900}x{600}+{int(sw/2-450)}+{int(sh/2-300)}')

    # Specify Grid
    Grid.rowconfigure(root, 0, weight=1)
    Grid.rowconfigure(root, 1, weight=9)

    Grid.columnconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 1, weight=1)
    Grid.columnconfigure(root, 2, weight=1)

    # Create Frames
    city_container = Frame(root, bg="gray")
    song_container = Frame(root, bg="blue")
    photo_container = Frame(root, bg="yellow")
    food_container = Frame(root, bg="green")

    # Set grid
    city_container.grid(row=0, column=0, columnspan=3, sticky="NSEW")
    song_container.grid(row=1, column=0, sticky="NSEW")
    photo_container.grid(row=1, column=1, sticky="NSEW")
    food_container.grid(row=1, column=2, sticky="NSEW")

    # City dropdown
    cities = []
    cursor.execute("SELECT name FROM cities")
    rows = cursor.fetchall()
    for row in rows:
        cities.append(row[0])
    current_city = StringVar()
    current_city.set(cities[0])
    current_city.trace('w', update_songs)
    optMenu = OptionMenu(city_container, current_city, *cities)
    optMenu.pack(pady=10)

    # Add City
    add_container = Frame(city_container)
    add_container.pack()
    new_city = Entry(add_container)
    new_city.pack(side=LEFT, padx=10)
    add = tk.Button(add_container, text="Add City", command=lambda: add_city(new_city.get()))
    add.pack(side=RIGHT, padx=10)

    # songs
    songs = Listbox(song_container)
    insert_songs(songs, current_city.get())
    songs.pack()
    # control buttons
    control_buttons = Frame(song_container, bg="lightgray")
    control_buttons.pack()
    play = tk.Button(control_buttons, text="Play", command=lambda: play_song(songs.get(ACTIVE)))
    play.pack(pady=10, padx=10, side=LEFT)
    stop = tk.Button(control_buttons, text="Stop", command=stop_song)
    stop.pack(pady=10, padx=10, side=RIGHT)
    # add songs container
    add_container = Frame(song_container, bg="lightgray")
    add_container.pack(pady=20)
    song_title_label = Label(add_container, text="Title")
    song_title_label.grid(row=0, column=0, pady=10)
    song_title_entry = Entry(add_container)
    song_title_entry.grid(row=0, column=1, pady=10)
    song_artist_label = Label(add_container, text="Artist")
    song_artist_label.grid(row=1, column=0, pady=10)
    song_artist_entry = Entry(add_container)
    song_artist_entry.grid(row=1, column=1, pady=10)
    song_description_label = Label(add_container, text="Description")
    song_description_label.grid(row=2, column=0, pady=10)
    song_description_entry = Entry(add_container)
    song_description_entry.grid(row=2, column=1, pady=10)
    add = tk.Button(add_container, text="Browse", command=browse_files)
    add.grid(row=3, column=0, pady=10)
    song_label = Label(add_container, text="Choose an mp3 file")
    song_label.grid(row=3, column=1, pady=10)
    upload_button = Button(add_container, text="Upload", command=upload_song)
    upload_button.grid(row=4, column=0, pady=10)

    # images
    photos = Listbox(photo_container)
    photos.pack()

    # food
    foods = Listbox(food_container)
    foods.pack()

    root.mainloop()

    # songs.grid(row=0, column=0, columnspan=4)
    # play = tk.Button(text="Play", command=lambda: play_song(songs.get(ACTIVE)))
    # stop = tk.Button(text="stop", command=stop_song)
    # play.grid(row=1, column=1)
    # stop.grid(row=1, column=2)
    # photos = tk.Canvas(root)
    # photos.configure(bg='red')
    # photos.grid(row=0, column=4, columnspan=4)