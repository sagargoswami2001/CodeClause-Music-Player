# Music Player in Python.
from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
from tkinter import ttk
import random
import os

root = Tk()
root.title("Sagar's Music Player")
root.geometry("500x400")

# Initialize pygame mixer
pygame.mixer.init()


# Song Length Info
def play_time():
    if stopped:
        return
    curr_time = pygame.mixer.music.get_pos() // 1000
    song = song_box.get(ACTIVE)
    song = f'{head}/{song}.mp3'
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    if int(my_slider.get()) == int(song_length):
        song_no = song_box.curselection()[0] + 1
        if song_no == song_box.size():
            song_no = 0
        song = song_box.get(song_no)
        song = f'{head}/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        song_box.selection_clear(ACTIVE)
        song_box.selection_set(song_no)
        slide(0)

    elif paused:
        pass
    elif int(my_slider.get()) == curr_time:
        slider_pos = int(song_length)
        my_slider.config(to=slider_pos, value=curr_time)
    else:
        slider_pos = int(song_length)
        my_slider.config(to=slider_pos, value=int(my_slider.get()))

        new_time = int(my_slider.get()) + 1
        my_slider.config(value=new_time)

    s_len = time.strftime('%M:%S', time.gmtime(song_length))
    new_time = time.strftime('%M:%S', time.gmtime(my_slider.get()))
    slider_label.config(text=f'{new_time} / {s_len}')

    status_bar.after(1000, play_time)


# add song func
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audios/', title="Choose...", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        global head
        global tail
        head, tail = os.path.split(song)
        song_box.insert(END, tail[:-4])


# play
def play():
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'{head}/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    my_slider.config(value=0)
    play_time()

global paused
paused = False

# pause
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

# Forward
def next_song():
    slider_label.config(text='00:00 / 00:00')
    my_slider.config(value=0)

    # current song number tuple
    next_one = song_box.curselection()[0] + 1
    if next_one == song_box.size():
        next_one = 0
    song = song_box.get(next_one)
    song = f'{head}/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Alter Active Bar
    song_box.selection_clear(0, END)
    song_box.selection_set(next_one, last=None)
    song_box.activate(next_one)

# Backward
def prev_song():
    slider_label.config(text='00:00 / 00:00')
    my_slider.config(value=0)
    # current song number tuple
    prev_one = song_box.curselection()[0] - 1
    if prev_one == -1:
        prev_one = song_box.size()-1
    song = song_box.get(prev_one)
    song = f'{head}/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Alter Active Bar
    song_box.selection_clear(0, END)
    song_box.selection_set(prev_one, last=None)
    song_box.activate(prev_one)

global stopped
stopped = False

def stop():
    slider_label.config(text='00:00 / 00:00')
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text='')

    global stopped
    stopped = True

# Delete A Song
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

# Delete All Songs
def delete_songs():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()

# Slider function
def slide(val):

    my_slider.config(value=val)
    s_len = time.strftime('%M:%S', time.gmtime(song_length))
    new_time = time.strftime('%M:%S', time.gmtime(my_slider.get()))
    slider_label.config(text=f'{new_time} / {s_len}')
    pygame.mixer.music.play(-1, my_slider.get())

# Volume
def volume(vol):
    pygame.mixer.music.set_volume(vol_slider.get())
    curr_vol = pygame.mixer.music.get_volume()
    vol_label.config(text=int(curr_vol*100))

# Shuffle
def shuffle():
    active_song = song_box.get(ACTIVE)

    songs_list = list(song_box.get(0, END))
    song_box.delete(0, END)
    random.shuffle(songs_list)

    for i, song in enumerate(songs_list):
        song_box.insert(i, song)

        if song == active_song:
            song_box.selection_set(i)
            song_box.activate(i)

    song_box.update()

# Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)
# Playlist box
song_box = Listbox(master_frame, bg="gray", fg="white", width=65, height=12,
                   selectbackground="black", selectforeground="white")
song_box.grid(row=0, column=0)

# Player Control Buttons Images
play_img = PhotoImage(file="icons/1play.png")
back_img = PhotoImage(file="icons/2back.png")
pause_img = PhotoImage(file="icons/3pause.png")
forward_img = PhotoImage(file="icons/4forward.png")
shuffle_img = PhotoImage(file="icons/5shuffle.png")

# Frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=3, column=0)

# Volume Frame
vol_frame = LabelFrame(master_frame, text='Volume')
vol_frame.grid(row=0, column=1, padx=6)

# Player Control Buttons
play_btn = Button(controls_frame, image=play_img, borderwidth=0, command=play)
back_btn = Button(controls_frame, image=back_img, borderwidth=0, command=prev_song)
pause_btn = Button(controls_frame, image=pause_img, borderwidth=0, command=lambda: pause(paused))
forward_btn = Button(controls_frame, image=forward_img, borderwidth=0, command=next_song)
shuffle_btn = Button(controls_frame, image=shuffle_img, borderwidth=0, command=shuffle)

play_btn.grid(row=0, column=2, padx=10)
back_btn.grid(row=0, column=0, padx=10)
pause_btn.grid(row=0, column=3, padx=10)
forward_btn.grid(row=0, column=1, padx=10)
shuffle_btn.grid(row=0, column=4, padx=10)

# Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add To Playlist", command=add_many_songs)

# Delete Song Menu
delete_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=delete_song_menu)
delete_song_menu.add_command(label="Remove Current", command=delete_song)
delete_song_menu.add_command(label="Remove All", command=delete_songs)

# Status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL,
                      value=0, command=slide, length=380, cursor="hand2")
my_slider.grid(row=2, column=0)
slider_label = Label(master_frame)
slider_label.grid(row=1, column=0, pady=10)
slider_label.config(text='00:00 / 00:00')

# Volume Slider
vol_slider = ttk.Scale(vol_frame, from_=1, to=0, orient=VERTICAL, value=1,
                       command=volume, length=147, cursor="hand2")
vol_slider.pack(pady=5)

# Volume Label
vol_label = Label(vol_frame, text='100')
vol_label.pack()

root.mainloop()
