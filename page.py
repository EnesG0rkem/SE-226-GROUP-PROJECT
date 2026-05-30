import platform
import traceback
from tkinter import *
import geminiAI
import Pollunation
import historyUtils
import trackUtils
import saveUtils
import webbrowser
from PIL import ImageTk
import threading
from tkinter import filedialog
import favoritesUtils


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
background_color = "#121212"
input_area_color = "#363636"
#endregion

#region Main page ----------------------------------------------------------------------
main_page = Tk()
main_page.geometry("1300x700")
main_page.minsize(1300, 700)
#r.attributes("-fullscreen", True)
main_page.title('Moodify')
main_page.focus_force()

main_frame = PanedWindow(main_page, orient=HORIZONTAL, bd=0, bg="#5f5f5f", sashwidth=10)
main_frame.pack(fill=BOTH,expand=1)
main_frame.bind("<Button-1>", focus_out)
#endregion

#region Left panel ----------------------------------------------------------------------------------------
left_panel = Frame(main_frame, bg = "#1C1C1C")
main_frame.add(left_panel)
main_frame.paneconfig(left_panel, minsize=500)
left_panel.bind("<Button-1>", focus_out)

#region texts

header = Label(left_panel, text="Moodify", font="Ariel 50 bold", bg = "#1C1C1C")
header.pack(padx=10,
            anchor='w')

description = Label(left_panel,
                    text="Describe your mood and get personalized recomendations", 
                    font="Ariel 15 normal",
                    fg="#7E7E7E", bg = "#1C1C1C")
description.pack(padx=10,
                 anchor='w')

text_label = Label(left_panel,
                   text="Your mood (English or Turkish)",
                   font="Ariel 20 bold",
                   foreground=spotify_green, bg = "#1C1C1C")

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
option_Menus = Frame(left_panel, bg = "#1C1C1C")
option_Menus.pack(padx=10,
                  anchor='n',
                  fill='x')

genre_frame = Frame(option_Menus, bg = "#1C1C1C")
genre_frame.pack(side=LEFT, expand=True, fill='both')

era_frame = Frame(option_Menus, bg = "#1C1C1C")
era_frame.pack(side=LEFT, expand=True, fill='both')

count_frame = Frame(option_Menus, bg = "#1C1C1C", highlightthickness=0)
count_frame.pack(side=LEFT, expand=True, fill='both')

#region--- Genres 
genre_label = Label(genre_frame, text="Genre", foreground = spotify_green, bg = "#1C1C1C")  #  3^01
genre_label.pack(anchor='w')
genres = ["Determine from text", "Pop", "Rock", "Jazz", "Classical", "Hip Hop", "Electronic",
          "Rap", "Indie", "R&B", "Soul", "Metal", "Turkish Pop"]  
opt_genre = StringVar(value="Determine from text")
genre_box = OptionMenu(genre_frame, opt_genre, *genres)
genre_box.pack(anchor='w')
#endregion 

#region--- Eras 
era_label = Label(era_frame, text="Era", foreground = spotify_green, bg = "#1C1C1C")  #  3^01
era_label.pack(anchor='n')
eras = ["All time", "2020's", "2010's", "2000's", "90's", "80's", "70's",]
opt_era = StringVar(value="All time")
era_box = OptionMenu(era_frame, opt_era, *eras)
era_box.pack(anchor='n')
#endregion

#region--- Count 
count_label = Label(count_frame, text="Track Count", foreground = spotify_green, bg = "#1C1C1C")
count_label.pack(anchor='e')
count_box = Spinbox(count_frame, from_ = 6, to = 14, width= 7)
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
main_frame.paneconfig(right_panel, minsize=800)
right_panel.config( bg = background_color)

# Cover image label
cover_label = Label(right_panel,  bg = background_color)
cover_label.pack(pady=(20, 5))

# Album name
album_title_label = Label(
    right_panel,
    text="Album Name",
    font=("Arial", 16, "bold"),
    fg="white",
     bg = background_color
)
album_title_label.pack()

# Artist name
artist_label_display = Label(
    right_panel,
    text="Artist Name",
    font=("Arial", 12),
    fg="#B3B3B3",
     bg = background_color
)
artist_label_display.pack()

tracklist_title = Label(
    right_panel,
    text="Generated Tracklist",
    font=("Arial", 18, "bold"),
    fg="white",
     bg = background_color
)
tracklist_title.pack(anchor="w", padx=20, pady=(20, 10))

tracks_frame_wrapper = Frame(right_panel, bg="#121212")
tracks_frame_wrapper.pack(fill=BOTH, expand=True, padx=20)

tracks_canvas = Canvas(tracks_frame_wrapper, bg="#121212", highlightthickness=0)
tracks_canvas.pack(side=LEFT, fill=BOTH, expand=True)

tracks_scrollbar = Scrollbar(
    tracks_frame_wrapper,
    orient="vertical",
    command=tracks_canvas.yview
)
tracks_scrollbar.pack(side=RIGHT, fill="y")

tracks_container = Frame(tracks_canvas, bg="#121212")

tracks_container.bind(
    "<Configure>",
    lambda e: tracks_canvas.configure(scrollregion=tracks_canvas.bbox("all"))
)

tracks_canvas_window = tracks_canvas.create_window((0, 0), window=tracks_container, anchor="nw")

def on_canvas_resize(event):
    tracks_canvas.itemconfig(tracks_canvas_window, width=event.width)

tracks_canvas.bind("<Configure>", on_canvas_resize)


tracks_canvas.configure(yscrollcommand=tracks_scrollbar.set)


def on_mousewheel(event):
    tracks_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


tracks_canvas.bind_all("<MouseWheel>", on_mousewheel)

#endregion
def open_track_url(track, journal, genre):

    historyUtils.save_track(track, journal, genre)

    if track["url"]:
        webbrowser.open(track["url"])


def clear_tracks():
    for widget in tracks_container.winfo_children():
        widget.destroy()

def toggle_favorite_ui(track, button):
    is_now_favorite = favoritesUtils.toggle_favorite(track)

    if is_now_favorite:
        button.config(text="♥")
    else:
        button.config(text="♡")


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

        favorite_symbol = "♥" if favoritesUtils.is_favorite(track) else "♡"

        favorite_button = Button(
            row,
            text="♥" if favoritesUtils.is_favorite(track) else "♡",
            font=("Arial", 14),
            bg="#181818",
            fg="red",
            borderwidth=0,
            activebackground="#181818"
        )

        favorite_button.config(
            command=lambda t=track, b=favorite_button: toggle_favorite_ui(t, b)
        )

        favorite_button.pack(side=RIGHT, padx=5)

        listen_button = Button(
            row,
            text="Listen",
            font="Ariel 15 bold",
            bg=spotify_green,
            activebackground=button_pressed,
            command=lambda t=track: open_track_url(t, current_journal, current_genre)
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

current_cover_image = None  # keep a reference so it's not garbage collected
current_journal = ""
current_genre = ""

current_cover_image = None
current_album_data = None
current_tracks = None
current_cover = None

def finish_generation(album_data, tracks, cover_image):
    global current_cover_image
    global current_album_data
    global current_tracks
    global current_cover

    current_album_data = album_data
    current_tracks = tracks
    current_cover = cover_image
        
    # 1. Show cover image
    img_resized = cover_image.resize((250, 250))
    current_cover_image = ImageTk.PhotoImage(img_resized)
    cover_label.config(text="", image="")
    cover_label.config(image=current_cover_image)
        
    # 2. Show album metadata
    album_title_label.config(text=album_data["album_name"])
    artist_label_display.config(text=album_data["artist_name"])

    tracklist_title.config(text="Generated Tracklist")
        
    # 3. Show tracklist
    display_tracks(tracks)
        
    # 4. Re-enable button
    generate_button.config(state=NORMAL)
    status_label.config(text="Done!")

def save_album():

    global current_album_data
    global current_tracks
    global current_cover

    if not current_album_data:
        status_label.config(text="Nothing to save")
        return

    folder = filedialog.askdirectory()

    if not folder:
        return

    saveUtils.save_album_json(
        folder,
        current_album_data,
        current_tracks
    )

    saveUtils.save_cover_png(
        folder,
        current_cover
    )

    status_label.config(text="Album saved!")

def show_favorites_album():

    favorites = favoritesUtils.load_favorites()

    clear_tracks()

    # Change titles
    tracklist_title.config(text="Favorites List")

    album_title_label.config(
        text="♥ Favorites Album"
    )

    artist_label_display.config(
        text="Your liked songs"
    )

    # Show heart instead of AI cover
    cover_label.config(
        image="",
        text="♥",
        fg="red",
        bg="#121212",
        font=("Arial", 120, "bold")
    )

    if not favorites:
        status_label.config(text="No favorite songs yet")
        return

    status_label.config(text="Showing favorites")

    display_tracks(favorites)
        

def on_generate():
    global current_journal
    global current_genre

    journal = input_area.get("1.0", END).strip()
    genre = opt_genre.get()
    era = opt_era.get()
    track_count = int(count_box.get())

    if not journal and genre == "Determine from text":
        status_label.config(text="Please enter a mood or journal text.")
        return

    current_journal = journal
    current_genre = genre

    status_label.config(text="Gemini is thinking...")
    generate_button.config(state=DISABLED)

    def background_task():
        try:
            result = geminiAI.generate_album_data(journal, genre, era, track_count)

            if not result:
                main_page.after(0, lambda: status_label.config(text="Gemini failed"))
                main_page.after(0, lambda: generate_button.config(state=NORMAL))
                return
        
            main_page.after(0, lambda: status_label.config(text="Fetching tracks..."))
            tracks = trackUtils.collect_tracks_from_tags(
                result["lastfm_tags"],
                track_count,
                journal,
                genre
            )
        
            main_page.after(0, lambda: status_label.config(text="Generating cover..."))
            cover_image = Pollunation.generate_cover(result["cover_prompt"])
        
            main_page.after(0, lambda: finish_generation(result, tracks, cover_image))


        except Exception as e:

            print("Generation error:")

            traceback.print_exc()
    
    threading.Thread(target=background_task, daemon=True).start()

generate_button.config(command=on_generate)

save_button = Button(
    left_panel,
    text="Save Album",
    font="Ariel 18 bold",
    bg="#444444",
    fg="white",
    command=save_album
)

save_button.pack(
    padx=10,
    pady=5,
    fill='x'
)

favorites_button = Button(
    left_panel,
    text="Favorites Album",
    font="Ariel 18 bold",
    bg="#444444",
    fg="white",
    command=show_favorites_album
)

favorites_button.pack(
    padx=10,
    pady=5,
    fill='x'
)

status_label = Label(left_panel, text="", fg="white", bg="#1C1C1C")
status_label.pack()


main_page.mainloop()