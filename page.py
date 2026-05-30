import platform
import threading
import webbrowser
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
import geminiAI
import Pollunation
import historyUtils
import trackUtils
import saveUtils
import favoritesUtils

# Platform-specific imports
if platform.system() == 'Darwin':  # macOS
    try:
        from tkmacosx import Button
    except ImportError:
        from tkinter import Button
else:  # Windows or Linux
    from tkinter import Button
    

def focus_out(event):
    """Clear focus from other elements when clicking on main window."""
    main_page.focus_set()


# region Color Palette
SPOTIFY_GREEN = "#1DB954"
BUTTON_PRESSED = "#199845"
BACKGROUND_COLOR = "#121212"
INPUT_AREA_COLOR = "#363636"
SIDEBAR_COLOR = "#1C1C1C"
DARKER_BACKGROUND = "#181818"
SECONDARY_TEXT_COLOR = "#B3B3B3"
SECONDARY_TEXT_LIGHTER = "#7E7E7E"
PANEL_SEPARATOR = "#5f5f5f"
# endregion

# region Window Configuration
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 700
WINDOW_TITLE = 'Moodify'
# endregion

# region Font Sizes
MAIN_HEADER_FONT = ("Arial", 50, "bold")
DESCRIPTION_FONT = ("Arial", 15)
LABEL_FONT = ("Arial", 20, "bold")
BUTTON_FONT = ("Arial", 30, "bold")
SMALL_BUTTON_FONT = ("Arial", 18, "bold")
TRACKLIST_HEADER_FONT = ("Arial", 18, "bold")
TRACK_TITLE_FONT = ("Arial", 11, "bold")
TRACK_ARTIST_FONT = ("Arial", 10)
METADATA_FONT = ("Arial", 16, "bold")
METADATA_ARTIST_FONT = ("Arial", 12)
HEART_ICON_FONT = ("Arial", 120, "bold")
FAVORITE_BUTTON_FONT = ("Arial", 14)
LISTEN_BUTTON_FONT = ("Arial", 15, "bold")
# endregion

# region UI Dimensions
LEFT_PANEL_MIN_SIZE = 500
RIGHT_PANEL_MIN_SIZE = 800
COVER_IMAGE_SIZE = 250
TRACK_COUNT_MIN = 6
TRACK_COUNT_MAX = 14
TEXT_AREA_HEIGHT = 10
SPINBOX_WIDTH = 7
TRACK_ROW_PADDING = 4
CANVAS_PADDING_X = 20
CANVAS_PADDING_Y = 20
# endregion

# region Main Window Setup
main_page = Tk()
main_page.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
main_page.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
main_page.title(WINDOW_TITLE)
main_page.focus_force()

main_frame = PanedWindow(main_page, orient=HORIZONTAL, bd=0, bg=PANEL_SEPARATOR, sashwidth=10)
main_frame.pack(fill=BOTH, expand=1)
main_frame.bind("<Button-1>", focus_out)
# endregion

# region Left Panel
left_panel = Frame(main_frame, bg=SIDEBAR_COLOR)
main_frame.add(left_panel)
main_frame.paneconfig(left_panel, minsize=LEFT_PANEL_MIN_SIZE)
left_panel.bind("<Button-1>", focus_out)
# endregion

# region Left Panel - Headers
header = Label(left_panel, text=WINDOW_TITLE, font=MAIN_HEADER_FONT, bg=SIDEBAR_COLOR)
header.pack(padx=10, anchor='w')

description = Label(
    left_panel,
    text="Describe your mood and get personalized recommendations",
    font=DESCRIPTION_FONT,
    fg=SECONDARY_TEXT_LIGHTER,
    bg=SIDEBAR_COLOR
)
description.pack(padx=10, anchor='w')

text_label = Label(
    left_panel,
    text="Your mood (English or Turkish)",
    font=LABEL_FONT,
    foreground=SPOTIFY_GREEN,
    bg=SIDEBAR_COLOR
)
text_label.pack(padx=10, anchor='w')
# endregion

# region Left Panel - Input Area
input_area = Text(
    left_panel,
    height=TEXT_AREA_HEIGHT,
    bg=INPUT_AREA_COLOR,
    highlightthickness=0
)
input_area.pack(padx=10, pady=10, anchor='w', fill=BOTH)
# endregion

# region Left Panel - Option Menus
option_menus = Frame(left_panel, bg=SIDEBAR_COLOR)
option_menus.pack(padx=10, anchor='n', fill='x')

# Genre Selection
genre_frame = Frame(option_menus, bg=SIDEBAR_COLOR)
genre_frame.pack(side=LEFT, expand=True, fill='both')

genre_label = Label(genre_frame, text="Genre", foreground=SPOTIFY_GREEN, bg=SIDEBAR_COLOR)
genre_label.pack(anchor='w')

genres = [
    "Determine from text", "Pop", "Rock", "Jazz", "Classical", "Hip Hop",
    "Electronic", "Rap", "Indie", "R&B", "Soul", "Metal", "Turkish Pop"
]
opt_genre = StringVar(value="Determine from text")
genre_box = OptionMenu(genre_frame, opt_genre, *genres)
genre_box.pack(anchor='w')

# Era Selection
era_frame = Frame(option_menus, bg=SIDEBAR_COLOR)
era_frame.pack(side=LEFT, expand=True, fill='both')

era_label = Label(era_frame, text="Era", foreground=SPOTIFY_GREEN, bg=SIDEBAR_COLOR)
era_label.pack(anchor='n')

eras = ["All time", "2020's", "2010's", "2000's", "90's", "80's", "70's"]
opt_era = StringVar(value="All time")
era_box = OptionMenu(era_frame, opt_era, *eras)
era_box.pack(anchor='n')

# Track Count Selection
count_frame = Frame(option_menus, bg=SIDEBAR_COLOR, highlightthickness=0)
count_frame.pack(side=LEFT, expand=True, fill='both')

count_label = Label(count_frame, text="Track Count", foreground=SPOTIFY_GREEN, bg=SIDEBAR_COLOR)
count_label.pack(anchor='e')

count_box = Spinbox(count_frame, from_=TRACK_COUNT_MIN, to=TRACK_COUNT_MAX, width=SPINBOX_WIDTH)
count_box.pack(anchor='e')
# endregion

# region Left Panel - Action Buttons
generate_button = Button(
    left_panel,
    text="Generate",
    font=BUTTON_FONT,
    bg=SPOTIFY_GREEN,
    focuscolor='',
    activebackground=BUTTON_PRESSED,
    activeforeground='black'
)
generate_button.pack(padx=10, pady=10, side=TOP, fill='x')

save_button = Button(
    left_panel,
    text="Save Album",
    font=SMALL_BUTTON_FONT,
    focuscolor='',
    activebackground='#2c2c2c',
    bg="#444444",
    fg="white"
)
save_button.pack(padx=10, pady=5, fill='x')

favorites_button = Button(
    left_panel,
    text="Favorites Album",
    font=SMALL_BUTTON_FONT,
    activebackground='#2c2c2c',
    focuscolor='',
    bg="#444444",
    fg="white"
)
favorites_button.pack(padx=10, pady=5, fill='x')

status_label = Label(left_panel, text="", fg="white", bg=SIDEBAR_COLOR)
status_label.pack()
# endregion

# region Right Panel - Main Setup
right_panel = Frame(main_frame, bg=BACKGROUND_COLOR)
main_frame.add(right_panel)
main_frame.paneconfig(right_panel, minsize=RIGHT_PANEL_MIN_SIZE)
# endregion

# region Right Panel - Album Metadata
cover_label = Label(right_panel, bg=BACKGROUND_COLOR)
cover_label.pack(pady=(20, 5))

album_title_label = Label(
    right_panel,
    text="Album Name",
    font=METADATA_FONT,
    fg="white",
    bg=BACKGROUND_COLOR
)
album_title_label.pack()

artist_label_display = Label(
    right_panel,
    text="Artist Name",
    font=METADATA_ARTIST_FONT,
    fg=SECONDARY_TEXT_COLOR,
    bg=BACKGROUND_COLOR
)
artist_label_display.pack()
# endregion

# region Right Panel - Tracklist Display
tracklist_title = Label(
    right_panel,
    text="Generated Tracklist",
    font=TRACKLIST_HEADER_FONT,
    fg="white",
    bg=BACKGROUND_COLOR
)
tracklist_title.pack(anchor="w", padx=CANVAS_PADDING_X, pady=(CANVAS_PADDING_Y, 10))

tracks_frame_wrapper = Frame(right_panel, bg=DARKER_BACKGROUND)
tracks_frame_wrapper.pack(fill=BOTH, expand=True, padx=CANVAS_PADDING_X)

tracks_canvas = Canvas(tracks_frame_wrapper, bg=BACKGROUND_COLOR, highlightthickness=0)
tracks_canvas.pack(side=LEFT, fill=BOTH, expand=True)

tracks_scrollbar = Scrollbar(
    tracks_frame_wrapper,
    orient="vertical",
    command=tracks_canvas.yview
)
tracks_scrollbar.pack(side=RIGHT, fill="y")

tracks_container = Frame(tracks_canvas, bg=BACKGROUND_COLOR)

tracks_container.bind(
    "<Configure>",
    lambda e: tracks_canvas.configure(scrollregion=tracks_canvas.bbox("all"))
)

tracks_canvas_window = tracks_canvas.create_window((0, 0), window=tracks_container, anchor="nw")

def on_canvas_resize(event):
    """Resize canvas to fit window width."""
    tracks_canvas.itemconfig(tracks_canvas_window, width=event.width)

tracks_canvas.bind("<Configure>", on_canvas_resize)
tracks_canvas.configure(yscrollcommand=tracks_scrollbar.set)

def on_mousewheel(event):
    """Handle mouse wheel scrolling for tracklist."""
    tracks_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

tracks_canvas.bind_all("<MouseWheel>", on_mousewheel)
# endregion

# region Global State Variables
current_cover_image = None  # Reference to prevent garbage collection
current_album_data = None
current_tracks = None
current_cover = None
current_journal = ""
current_genre = ""
# endregion

# region Business Logic Methods
def open_track_url(track, journal, genre):
    """
    Open track URL in browser and save to history.
    
    Args:
        track (dict): Track data containing URL
        journal (str): User's mood description
        genre (str): Selected genre
    """
    historyUtils.save_track(track, journal, genre)
    if track["url"]:
        webbrowser.open(track["url"])


def clear_tracks():
    """Remove all track widgets from the display container."""
    for widget in tracks_container.winfo_children():
        widget.destroy()


def toggle_favorite_ui(track, button):
    """
    Toggle favorite status for a track and update button UI.
    
    Args:
        track (dict): Track data
        button (Button): Favorite button widget to update
    """
    is_now_favorite = favoritesUtils.toggle_favorite(track)
    button.config(text="♥" if is_now_favorite else "♡")


def display_tracks(tracks):
    """
    Display list of tracks in the tracklist container.
    
    Args:
        tracks (list): List of track dictionaries to display
    """
    clear_tracks()

    for index, track in enumerate(tracks, start=1):
        row = Frame(tracks_container, bg=DARKER_BACKGROUND)
        row.pack(fill="x", pady=TRACK_ROW_PADDING)

        # Track number
        number_label = Label(
            row,
            text=str(index),
            width=3,
            fg=SECONDARY_TEXT_COLOR,
            bg=DARKER_BACKGROUND
        )
        number_label.pack(side=LEFT, padx=8)

        # Track info section
        info_frame = Frame(row, bg=DARKER_BACKGROUND)
        info_frame.pack(side=LEFT, fill="x", expand=True)

        song_label = Label(
            info_frame,
            text=track["name"],
            fg="white",
            bg=DARKER_BACKGROUND,
            font=TRACK_TITLE_FONT
        )
        song_label.pack(anchor="w")

        artist_label = Label(
            info_frame,
            text=track["artist"],
            fg=SECONDARY_TEXT_COLOR,
            bg=DARKER_BACKGROUND,
            font=TRACK_ARTIST_FONT
        )
        artist_label.pack(anchor="w")

        # Favorite button
        favorite_button = Button(
            row,
            text="♥" if favoritesUtils.is_favorite(track) else "♡",
            font=FAVORITE_BUTTON_FONT,
            bg=DARKER_BACKGROUND,
            fg="red",
            borderwidth=0,
            focuscolor='',
            activebackground=DARKER_BACKGROUND,
            command=lambda t=track, b=None: toggle_favorite_ui(t, b)
        )
        favorite_button.config(command=lambda t=track, b=favorite_button: toggle_favorite_ui(t, b))
        favorite_button.pack(side=RIGHT, padx=5)

        # Listen button
        listen_button = Button(
            row,
            text="Listen",
            font=LISTEN_BUTTON_FONT,
            bg=SPOTIFY_GREEN,
            activebackground=BUTTON_PRESSED,
            activeforeground='black',
            focuscolor='',
            command=lambda t=track: open_track_url(t, current_journal, current_genre)
        )
        listen_button.pack(side=RIGHT, padx=8)


def finish_generation(album_data, tracks, cover_image):
    """
    Display generation results in UI.
    
    Args:
        album_data (dict): Album metadata
        tracks (list): Generated tracklist
        cover_image: PIL Image for album cover
    """
    global current_cover_image, current_album_data, current_tracks, current_cover

    current_album_data = album_data
    current_tracks = tracks
    current_cover = cover_image

    # Update cover image
    img_resized = cover_image.resize((COVER_IMAGE_SIZE, COVER_IMAGE_SIZE))
    current_cover_image = ImageTk.PhotoImage(img_resized)
    cover_label.config(text="", image="")
    cover_label.config(image=current_cover_image)

    # Update metadata
    album_title_label.config(text=album_data["album_name"])
    artist_label_display.config(text=album_data["artist_name"])
    tracklist_title.config(text="Generated Tracklist")

    # Display tracklist
    display_tracks(tracks)

    # Re-enable button
    generate_button.config(state=NORMAL)
    status_label.config(text="Done!")


def save_album():
    """Save current album (metadata and cover image) to selected directory."""
    global current_album_data, current_tracks, current_cover

    if not current_album_data:
        status_label.config(text="Nothing to save")
        return

    folder = filedialog.askdirectory()
    if not folder:
        return

    saveUtils.save_album_json(folder, current_album_data, current_tracks)
    saveUtils.save_cover_png(folder, current_cover)
    status_label.config(text="Album saved!")


def show_favorites_album():
    """Display the user's favorite tracks."""
    favorites = favoritesUtils.load_favorites()
    clear_tracks()

    # Update UI labels
    tracklist_title.config(text="Favorites List")
    album_title_label.config(text="♥ Favorites Album")
    artist_label_display.config(text="Your liked songs")

    # Show heart icon instead of cover
    cover_label.config(
        image="",
        text="♥",
        fg="red",
        bg=BACKGROUND_COLOR,
        font=HEART_ICON_FONT
    )

    if not favorites:
        status_label.config(text="No favorite songs yet")
        return

    status_label.config(text="Showing favorites")
    display_tracks(favorites)


def on_generate():
    """Handle generation button click - trigger mood-based playlist generation."""
    global current_journal, current_genre

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
        """Asynchronous task: generate playlist, fetch tracks, and create cover."""
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
            print("Generation error:", e)
            main_page.after(0, lambda: status_label.config(text="Something went wrong"))
            main_page.after(0, lambda: generate_button.config(state=NORMAL))

    threading.Thread(target=background_task, daemon=True).start()
# endregion

# region Button Command Bindings
generate_button.config(command=on_generate)
save_button.config(command=save_album)
favorites_button.config(command=show_favorites_album)
# endregion

# Initialize with favorites on startup
show_favorites_album()

# Start the application
main_page.mainloop()
# endregion