import tkinter as tk
from tkinter.filedialog import askopenfilename
import dnd_map_cutter

#Splits the map using the dnd_map_cutter script
def convert_map():
    map_img = dnd_map_cutter.load_map(MapPath)
    try:
        dnd_map_cutter.generate_printable_map(map_img,int(map_width.get()),int(map_height.get()),grid_val.get(),horiz_val.get(),show_val.get())
    except Exception as e:
        print(e)
        return

#Allows the user to select an img path from their folder
def get_new_map():
    #Creates a global variable with the path
    global MapPath 
    MapPath = askopenfilename()

    #Show the current file name
    name = MapPath.split("/")
    map_label.config(text=name[len(name)-1])

ui = tk.Tk()
ui.title("DnD map slicer")

title = tk.Label(ui,text="Test")
title.pack()

#Map selector
map_button = tk.Button(ui,text="Select Map",command=get_new_map)
map_button.pack()

map_label = tk.Label(ui,text="")
map_label.pack()

#Map dimensions
map_width = tk.Spinbox(ui,text="Width",from_=1, to=1000)
map_width.pack()

map_height = tk.Spinbox(ui,text="Height",from_=1, to=1000)
map_height.pack()

#Settings toggles
grid_val = tk.BooleanVar()
grid_toggle = tk.Checkbutton(ui,text="Draw Grid",variable=grid_val)
grid_toggle.pack()

horiz_val = tk.BooleanVar()
horiz_toggle = tk.Checkbutton(ui,text="Horizontal",variable=horiz_val)
horiz_toggle.pack()

show_val = tk.BooleanVar()
show_toggle = tk.Checkbutton(ui,text="Show output",variable=show_val)
show_toggle.pack()

#Start button
go_button = tk.Button(ui,text="go!",command=convert_map)
go_button.pack()

ui.mainloop()