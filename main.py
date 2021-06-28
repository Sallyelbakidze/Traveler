import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil

from pygame import mixer
import sqlite3
import os.path
from os import path


# connect if DB exists else create one
if path.exists("SQLite_Python.db"):
    conn = sqlite3.connect("SQLite_Python.db")
    cursor = conn.cursor()
else:
    conn = sqlite3.connect("SQLite_Python.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE songs (path TEXT, city_id INTEGER, title TEXT, artist TEXT, description TEXT)")
    cursor.execute("CREATE TABLE cities (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE TABLE photos (path TEXT, city_id INTEGER, name TEXT)")
    cursor.execute("CREATE TABLE foods (city_id INTEGER, name TEXT, description TEXT)")


if __name__ == '__main__':
    filepath = 'something'


    def update_data(*args):
        update_songs()
        update_photos()
        update_foods()


    def change_photo(event):
        selection = event.widget.curselection()
        if selection:
            sel_name = event.widget.get(selection[0])
            cc = current_city.get()
            id = cursor.execute("SELECT id FROM cities WHERE name=?", (cc,)).fetchall()[0][0]
            cur_photo_path = cursor.execute("SELECT path FROM photos WHERE name = ? AND city_id = ?", (sel_name, id, )).fetchall()[0][0]
            cur_photo = Image.open(cur_photo_path)
            cur_photo_resized = cur_photo.resize((200, 200), Image.ANTIALIAS)
            cur_photo_conv = ImageTk.PhotoImage(cur_photo_resized)
            photo_display_label.configure(image=cur_photo_conv)
            photo_display_label.image = cur_photo_conv
        else:
            print('insert dummy photo')


    def change_food(event):
        selection = event.widget.curselection()
        if selection:
            sel_name = event.widget.get(selection[0])
            cc = current_city.get()
            id = cursor.execute("SELECT id FROM cities WHERE name=?", (cc,)).fetchall()[0][0]
            curr_food_description = cursor.execute("SELECT description FROM foods WHERE name = ? AND city_id = ?", (sel_name, id,)).fetchall()[0][0]
            food_description.configure(text=curr_food_description)
        else:
            print('insert dummy food')


    def play_song(song):
        cc = current_city.get()
        id = cursor.execute("SELECT id FROM cities WHERE name=?", (cc,)).fetchall()[0][0]
        cursor.execute("SELECT path FROM songs WHERE title = ? AND city_id = ?", (song, id, ))
        song_path = cursor.fetchall()[0][0]
        mixer.init()
        mixer.music.load(song_path)
        mixer.music.play()


    def insert_songs(lb, cc):
        songs.delete(0, 'end')
        statement = cursor.execute("SELECT id FROM cities WHERE name=?", (cc,)).fetchall()
        if statement:
            id = cursor.execute("SELECT id FROM cities WHERE name=?", (cc,)).fetchall()[0][0]
            rows = cursor.execute("SELECT title FROM songs WHERE city_id=?", (id,)).fetchall()
            for row in rows:
                lb.insert(0, row[0])


    def insert_photos(lb, cc):
        photos.delete(0, 'end')
        statement = cursor.execute("SELECT id FROM cities WHERE name=?", (cc,)).fetchall()
        if statement:
            id = cursor.execute("SELECT id FROM cities WHERE name=?", (cc,)).fetchall()[0][0]
            rows = cursor.execute("SELECT name FROM photos WHERE city_id=?", (id,)).fetchall()
            for row in rows:
                lb.insert(0, row[0])


    def insert_foods(lb, cc):
        foods.delete(0, 'end')
        statement = cursor.execute("SELECT id FROM cities WHERE name=?", (cc,)).fetchall()
        if statement:
            id = cursor.execute("SELECT id FROM cities WHERE name=?", (cc,)).fetchall()[0][0]
            rows = cursor.execute("SELECT name FROM foods WHERE city_id=?", (id,)).fetchall()
            for row in rows:
                lb.insert(0, row[0])


    def stop_song():
        mixer.music.stop()


    def add_city(city_name):
        if 'Select A City' in cities:
            optMenu.children['menu'].delete('Select A City')
            cities.remove('Select A City')
        if city_name:
            cursor.execute("INSERT INTO cities (name) VALUES(?)", (city_name,))
            conn.commit()
            new_city.delete(0, END)
            current_city.set(city_name)
            optMenu['menu'].add_command(label=city_name, command=tk._setit(current_city, city_name))


    def update_songs():
        insert_songs(songs, current_city.get())


    def update_photos():
        insert_photos(photos, current_city.get())
        photo_display_label.configure(image=def_photo_conv)


    def update_foods():
        insert_foods(foods, current_city.get())


    def browse_files():
        global filepath
        filepath = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                              filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")))
        if filepath:
            song_label.configure(text=os.path.basename(filepath))


    def browse_photos():
        global filepath
        filepath = filedialog.askopenfilename(initialdir="/", title="Select a Photo",
                                              filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
        if filepath:
            photo_label.configure(text=os.path.basename(filepath))


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


    def upload_photo():
        shutil.copy(filepath, os.getcwd())
        name = photo_name_entry.get()
        photo_name_entry.delete(0, END)
        photo_label.configure(text="Choose your photo")
        city_id = cursor.execute("SELECT id FROM cities WHERE name=?", (current_city.get(),)).fetchall()[0][0]
        cursor.execute("INSERT INTO photos (path,city_id,name) VALUES(?, ?, ?)",
                       (os.path.basename(filepath), city_id, name))
        conn.commit()
        update_photos()


    def add_food():
        name = food_name_entry.get()
        food_name_entry.delete(0, END)
        description = food_description_text.get("1.0", END)
        food_description_text.delete("1.0", END)
        city_id = cursor.execute("SELECT id FROM cities WHERE name=?", (current_city.get(),)).fetchall()[0][0]
        cursor.execute("INSERT INTO foods (city_id,name,description) VALUES(?, ?, ?)",
                       (city_id, name, description))
        conn.commit()
        update_foods()


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
    if cities:
        current_city.set(cities[0])
    else:
        cities.append('Select A City')
        current_city.set(cities[0])
    current_city.trace('w', update_data)
    optMenu = OptionMenu(city_container, current_city, *cities)
    optMenu.pack(pady=10)

    # Add City
    add_container = Frame(city_container)
    add_container.pack()
    new_city = Entry(add_container)
    new_city.pack(side=LEFT, padx=10)
    add = tk.Button(add_container, text="Add City", command=lambda: add_city(new_city.get()))
    add.pack(side=RIGHT, padx=10)

    # songs list container
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

    # photos list container
    photos = Listbox(photo_container)
    photos.pack()
    photos.bind("<<ListboxSelect>>", change_photo)
    insert_photos(photos, current_city.get())
    # photo display container
    photo_display_label = Label(photo_container)
    def_photo = Image.open('default.jpg')
    def_photo_resized = def_photo.resize((200, 200), Image.ANTIALIAS)
    def_photo_conv = ImageTk.PhotoImage(def_photo_resized)
    photo_display_label.configure(image=def_photo_conv)
    photo_display_label.pack()
    # add photo container
    add_photo_container = Frame(photo_container, bg="lightgray")
    add_photo_container.pack()
    photo_name_label = Label(add_photo_container, text="Name")
    photo_name_label.grid(row=0, column=0)
    photo_name_entry = Entry(add_photo_container)
    photo_name_entry.grid(row=0, column=1)
    add_photo_button = tk.Button(add_photo_container, text="Browse", command=browse_photos)
    add_photo_button.grid(row=1, column=0, pady=10)
    photo_label = Label(add_photo_container, text="Choose your photo")
    photo_label.grid(row=1, column=1, pady=10)
    upload_photo_button = Button(add_photo_container, text="Upload", command=upload_photo)
    upload_photo_button.grid(row=2, column=0, pady=10)

    # foods list container
    foods = Listbox(food_container)
    foods.pack()
    foods.bind("<<ListboxSelect>>", change_food)
    # Description
    food_description = Label(food_container, text="Food Description")
    food_description.pack()
    # Add Food Container
    add_food_container = Frame(food_container, bg="lightgrey")
    add_food_container.pack(pady=100)
    food_name_label = Label(add_food_container, text="Name")
    food_name_label.grid(row=0, column=0, pady=10)
    food_name_entry = Entry(add_food_container)
    food_name_entry.grid(row=0, column=1)
    food_description_label = Label(add_food_container, text="Description")
    food_description_label.grid(row=1, column=0, pady=10)
    food_description_text = Text(add_food_container, width=26, height=3)
    food_description_text.grid(row=1, column=1)
    add_food_button = Button(add_food_container, text="Add", width=10, command=add_food)
    add_food_button.grid(row=2, column=1, pady=10)


    root.mainloop()