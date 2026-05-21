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
                         activeforeground='black',
                         focuscolor='')
generate_button.pack(padx=10,
                     pady=10,
                     side=TOP, fill='x')
#endregion

#endregion

#region Right panel ----------------------------------------------------------------------------------------
right_panel = Frame(main_frame)
main_frame.add(right_panel)

l1 = Label(right_panel, text="deneme", font="Ariel 50 bold", )
l1.pack(anchor="w")
#endregion
main_page.mainloop()
