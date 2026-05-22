import platform
from tkinter import *
import geminiAI
import Lastfm
import Pollunation
import trackUtils
import genreStyles
import saveUtils
import webbrowser
from PIL import ImageTk


if platform.system() == 'Darwin':  # macOS ise
    try:
        from tkmacosx import Button
    except ImportError:
        from tkinter import Button
else:  # Windows veya Linux ise
    from tkinter import Button
    
def focus_out(event):
    main_page.focus_set()


#region Colors ----------------------------------------------------------------------
spotify_green = "#1DB954"
button_pressed = "#199845"
background_color = "#1C1C1C"
input_area_color = "#363636"
#endregion

#region Main page ----------------------------------------------------------------------
main_page = Tk()
main_page.geometry("1050x700")
#r.attributes("-fullscreen", True)
main_page.title('Moodify')
main_page.focus_force()

main_frame = PanedWindow(main_page, orient=HORIZONTAL, bd=0, bg="#5f5f5f", sashwidth=10)
main_frame.pack(fill=BOTH,expand=1)
main_frame.bind("<Button-1>", focus_out)
#endregion

#region Left panel ----------------------------------------------------------------------------------------
left_panel = Frame(main_frame, bg = background_color)
main_frame.add(left_panel)
left_panel.bind("<Button-1>", focus_out)

#region texts

header = Label(left_panel, text="Moodify", font="Ariel 50 bold")  #  3^01
header.pack(padx=10,
            anchor='w')

description = Label(left_panel,
                    text="Describe your mood and get personalized recomendations", 
                    font="Ariel 15 normal",
                    fg="#7E7E7E")  #  3^01
description.pack(padx=10,
                 anchor='w')

text_label = Label(left_panel,
                   text="Your mood (English or Turkish)",
                   font="Ariel 20 bold",
                   foreground=spotify_green)  #  3^01

text_label.pack(padx=10,
                anchor='w')

input_area = Text(left_panel,
                  height= 10,
                  bg = "#363636",
                  highlightthickness=0)
input_area.pack(padx=10,
                pady=10,
                anchor='w',
                fill=BOTH)
#endregion

#region option menus
option_Menus = Frame(left_panel, bg = background_color)
option_Menus.pack(padx=10,
                  anchor='n',
                  fill='x')

genre_frame = Frame(option_Menus, bg = background_color)
genre_frame.pack(side=LEFT, expand=True, fill='both')

era_frame = Frame(option_Menus, bg = background_color)
era_frame.pack(side=LEFT, expand=True, fill='both')

count_frame = Frame(option_Menus, bg = background_color, highlightthickness=0)
count_frame.pack(side=LEFT, expand=True, fill='both')

#region--- Genres 
genre_label = Label(genre_frame, text="Genre", foreground = spotify_green)  #  3^01
genre_label.pack(anchor='w')
genres = ["Determine from text", "Pop", "Rock", "Jazz", "Classical", "Hip Hop", "Electronic"]  
opt_genre = StringVar(value="Determine from text")
genre_box = OptionMenu(genre_frame, opt_genre, *genres)
genre_box.pack(anchor='w')
#endregion 

#region--- Eras 
era_label = Label(era_frame, text="Era", foreground = spotify_green)  #  3^01
era_label.pack(anchor='n')
eras = ["50's", "60's", "70's", "80's", "90's", "2000's", "2010's", "2020's"]
opt_era = StringVar(value="2020's")
era_box = OptionMenu(era_frame, opt_era, *eras)
era_box.pack(anchor='n')
#endregion

#region--- Count 
count_label = Label(count_frame, text="Track Count", foreground = spotify_green)
count_label.pack(anchor='e')
count_box = Spinbox(count_frame, from_ = 0, to = 10, width= 7)
count_box.pack(anchor='e')
#endregion

#endregion

#region generate button 

generate_button = Button(left_panel,
                         text="Generate",
                         font="Ariel 30 bold",
                         bg=spotify_green,
                         activebackground=button_pressed,
                         activeforeground='black')
# removed focuscolor=''
generate_button.pack(padx=10,
                     pady=10,
                     side=TOP, fill='x')
#endregion

#endregion

#region Right panel ----------------------------------------------------------------------------------------
right_panel = Frame(main_frame)
main_frame.add(right_panel)

right_panel.config(bg="#121212")

tracklist_title = Label(
    right_panel,
    text="Generated Tracklist",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#121212"
)
tracklist_title.pack(anchor="w", padx=20, pady=(20, 10))

tracks_container = Frame(right_panel, bg="#121212")
tracks_container.pack(fill="both", expand=True, padx=20)
#endregion
def open_track_url(url):
    if url:
        webbrowser.open(url)


def clear_tracks():
    for widget in tracks_container.winfo_children():
        widget.destroy()


def display_tracks(tracks):
    clear_tracks()

    for index, track in enumerate(tracks, start=1):
        row = Frame(tracks_container, bg="#181818")
        row.pack(fill="x", pady=4)

        number_label = Label(row, text=str(index), width=3, fg="#B3B3B3", bg="#181818")
        number_label.pack(side=LEFT, padx=8)

        info_frame = Frame(row, bg="#181818")
        info_frame.pack(side=LEFT, fill="x", expand=True)

        song_label = Label(
            info_frame,
            text=track["name"],
            fg="white",
            bg="#181818",
            font=("Arial", 11, "bold")
        )
        song_label.pack(anchor="w")

        artist_label = Label(
            info_frame,
            text=track["artist"],
            fg="#B3B3B3",
            bg="#181818",
            font=("Arial", 10)
        )
        artist_label.pack(anchor="w")

        listen_button = Button(
            row,
            text="Listen",
            bg=spotify_green,
            activebackground=button_pressed,
            command=lambda url=track["url"]: open_track_url(url)
        )
        listen_button.pack(side=RIGHT, padx=8)

test_tracks = [
    {
        "name": "crying lightning",
        "artist": "Arctic Monkeys",
        "url": "https://www.last.fm/music/Arctic+Monkeys"
    },
    {
        "name": "blond",
        "artist": "Frank Ocean",
        "url": "https://www.last.fm/music/Frank+Ocean"
    },
    {
        "name": "hileli",
        "artist": "Manifest",
        "url": "https://www.last.fm/music/Manifest"
    }
]

display_tracks(test_tracks)
        

def on_generate():

    journal = input_area.get("1.0", END).strip()
    genre = opt_genre.get()
    era = opt_era.get()
    track_count = count_box.get()

    status_label.config(text="Gemini is thinking...")

    result = geminiAI.generate_album_data(
        journal,
        genre,
        era,
        track_count
    )

    if not result:
        status_label.config(text="Gemini failed")
        return

    status_label.config(text="Album generated!")
    print(result)

generate_button.config(command=on_generate)

status_label = Label(left_panel, text="", fg="white", bg="#1C1C1C")
status_label.pack()


main_page.mainloop()