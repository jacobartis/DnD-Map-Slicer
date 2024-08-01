import tkinter as tk
from tkinter.filedialog import askopenfilename
import dnd_map_cutter

def convert_map():
    print(MapPath)
    map_img = dnd_map_cutter.load_map(MapPath)
    try:
        dnd_map_cutter.generate_printable_map(map_img,23,16,True,True)
    except:
        return

def get_new_map():
    global MapPath 
    MapPath = askopenfilename()

ui = tk.Tk()
ui.title("DnD map slicer")

title = tk.Label(ui,text="Test")
title.pack()

map_button = tk.Button(ui,text="Select Map",command=get_new_map)
map_button.pack()

grid_val = tk.BooleanVar()
grid_toggle = tk.Checkbutton(ui,text="Draw Grid",variable=grid_val)
grid_toggle.pack()

horiz_val = tk.BooleanVar()
horiz_toggle = tk.Checkbutton(ui,text="Horizontal",variable=horiz_val)
horiz_toggle.pack()

go_button = tk.Button(ui,text="go!",command=convert_map)
go_button.pack()

ui.mainloop()