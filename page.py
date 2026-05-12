from tkinter import *

main_page = Tk()
main_page.geometry("1050x700")
#r.attributes("-fullscreen", True)
main_page.title('Moodify')

main_page.focus_force()

main_frame = PanedWindow(main_page, orient=HORIZONTAL, bd=0, bg="#5f5f5f", sashwidth=10)
main_frame.pack(fill=BOTH,expand=1)

#Left panel ----------------------------------------------------------------------------------------
left_panel = Frame(main_frame, bg="#1C1C1C")
main_frame.add(left_panel)

header = Label(left_panel, text="Moodify", font="Ariel 50 bold")  #  3^01
header.pack(anchor='w')

description = Label(left_panel,
                    text="Describe your mood and get personalized recomendations", 
                    font="Ariel 15 normal",
                    fg="#7E7E7E")  #  3^01
description.pack(anchor='w')

text_label = Label(left_panel,
                   text="Your mood (English or Turkish)",
                   font="Ariel 20 bold",
                   foreground="#1DB954")  #  3^01

text_label.pack(anchor='w')

input_area = Text(left_panel, bg="#363636")
input_area.pack(anchor='w')

genre_label = Label(left_panel, text="Genre", foreground="#1DB954" )  #  3^01
genre_label.pack(anchor='w')

genres = ["Determine from text", "Pop", "Rock", "Jazz", "Classical", "Hip Hop", "Electronic"]  
opt_genre = StringVar(value="Determine from text")

genre_box = OptionMenu(left_panel, opt_genre, *genres)
genre_box.pack(anchor='w')

eras = ["50's", "60's", "70's", "80's", "90's", "2000's", "2010's", "2020's"]
opt_era = StringVar(value="2020's")



#Right panel ----------------------------------------------------------------------------------------
right_panel = Frame(main_frame)
main_frame.add(right_panel)

l1 = Label(right_panel, text="deneme", font="Ariel 50 bold", )
l1.pack(anchor="w")

main_page.mainloop()