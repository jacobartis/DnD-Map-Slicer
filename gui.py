import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import ImageTk, Image
import cv2 as cv
import dnd_map_cutter

MAX_IMG_WIDTH = 400
MAX_IMG_HEIGHT = 400

#Splits the map using the dnd_map_cutter script
def convert_map():
    map_img = dnd_map_cutter.load_map(MapPath)
    try:
        dnd_map_cutter.generate_printable_map(map_img,int(map_width.get()),int(map_height.get()),grid_val.get(),orientaion_pick.get()=="Horizontal")
    except Exception as e:
        print(e)
        return

def update_img():
    try:
        print(MapPath)
    except:
        print("no map")
        return
    #Uses PIL to open and resize the img
    map_img = dnd_map_cutter.load_map(MapPath)
    if grid_val.get():
        dnd_map_cutter.grid(map_img,[0,0,0],3,int(map_width.get()),int(map_height.get()))

    if cut_val.get() and orientaion_pick.get()=="Horizontal":
        dnd_map_cutter.grid(map_img,[255,0,0],5,int(map_width.get())/float(cut_height_val.get()),int(map_height.get())/float(cut_width_val.get()))
    elif cut_val.get():
        dnd_map_cutter.grid(map_img,[255,0,0],5,int(map_width.get())/float(cut_width_val.get()),int(map_height.get())/float(cut_height_val.get()))

    img = cv.cvtColor(map_img, cv.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img)
    ratio = min(MAX_IMG_WIDTH/pil_img.size[0], MAX_IMG_HEIGHT/pil_img.size[1])
    map_preview = ImageTk.PhotoImage(pil_img.resize((int(pil_img.size[0]*ratio),int(pil_img.size[1]*ratio))))
    map_display.config(image=map_preview)
    map_display.photo = map_preview

#Allows the user to select an img path from their folder
def get_new_map():

    temp_file = askopenfilename()
    print(type(dnd_map_cutter.load_map(temp_file)))
    if dnd_map_cutter.load_map(temp_file) is None:
        messagebox.showerror("Error loading img","The selected img can't be loaded")
        return
    
    #Creates a global variable with the path
    global MapPath 
    MapPath = temp_file

    update_img()

    #Show the current file name
    name = MapPath.split("/")
    map_label.config(text=name[len(name)-1])

ui = tk.Tk()
ui.minsize(250,300)
ui.config(bg="maroon") 
ui.title("DnD map slicer")

title = tk.Label(ui,text="DnD Map Slicer")
title.grid(row=0, column=0, padx=10, pady=5)

map_frame = tk.Frame(ui, width=200, height=400, bg='grey')
map_frame.grid(row=1, column=1, padx=10, pady=5)

#Map selector
map_button = tk.Button(map_frame,text="Select Map",command=get_new_map)
map_button.grid(row=0, column=0, padx=10, pady=5)


map_label = tk.Label(map_frame,text="")
map_label.grid(row=1, column=0, padx=10, pady=5)

map_display = tk.Label(map_frame,image=None)
map_display.grid(row=2, column=0, padx=10, pady=5)


settings_frame = tk.Frame(ui, width=200, height=500, bg='grey')
settings_frame.grid(row=1, column=0, padx=10, pady=5)

#Map dimensions

#Frame setup
grid_frame = tk.Frame(settings_frame)
grid_frame.grid(row=2, column=0, padx=10, pady=5)

#Label 
grid_dim_label = tk.Label(grid_frame,text="Grid Dimensions")
grid_dim_label.grid(row=0, column=0, padx=10, pady=5)

#Frame for width and height 
grid_dim_frame = tk.Frame(grid_frame)
grid_dim_frame.grid(row=1, column=0, padx=10, pady=5)

width_label = tk.Label(grid_dim_frame,text="Width: ")
width_label.grid(row=0, column=0, padx=10, pady=5)
map_width = tk.Spinbox(grid_dim_frame,command=update_img,from_=1, to=1000)
map_width.grid(row=0, column=1, padx=10, pady=5)

height_label = tk.Label(grid_dim_frame,text="Height: ")
height_label.grid(row=0, column=2, padx=10, pady=5)
map_height = tk.Spinbox(grid_dim_frame,command=update_img,from_=1, to=1000)
map_height.grid(row=0, column=3, padx=10, pady=5)

#Toggle button for grid
grid_show_frame = tk.Frame(grid_frame)
grid_show_frame.grid(row=2, column=0)
grid_val = tk.BooleanVar()
grid_label = tk.Label(grid_show_frame,text="Draw Grid: ")
grid_label.grid(row=2, column=0, padx=10, pady=5)
grid_toggle = tk.Checkbutton(grid_show_frame,variable=grid_val,command=update_img)
grid_toggle.grid(row=2, column=1, padx=10, pady=5)

#Cut lines

#Frame setup
cut_frame = tk.Frame(settings_frame)
cut_frame.grid(row=3, column=0, padx=10, pady=5)

#Label 
cut_dim_label = tk.Label(cut_frame,text="Cut Dimensions")
cut_dim_label.grid(row=0, column=0, padx=10, pady=5)

#Frame for width and height 
cut_dim_frame = tk.Frame(cut_frame)
cut_dim_frame.grid(row=1, column=0, padx=10, pady=5)

cut_width_label = tk.Label(cut_dim_frame,text="Width: ")
cut_width_label.grid(row=0, column=0, padx=10, pady=5)
cut_width_val = tk.DoubleVar()
cut_width_val.set(8)
cut_width = tk.Spinbox(cut_dim_frame,command=update_img,from_=1, to=1000, increment=.5,textvariable=cut_width_val)
cut_width.grid(row=0, column=1, padx=10, pady=5)

cut_height_label = tk.Label(cut_dim_frame,text="Height: ")
cut_height_label.grid(row=0, column=2, padx=10, pady=5)
cut_height_val = tk.DoubleVar()
cut_height_val.set(11.5)
cut_height = tk.Spinbox(cut_dim_frame,command=update_img,from_=1, to=1000, increment=.5,textvariable=cut_height_val)
cut_height.grid(row=0, column=3, padx=10, pady=5)

#Toggle button for grid
cut_show_frame = tk.Frame(cut_frame)
cut_show_frame.grid(row=2, column=0)
cut_val = tk.BooleanVar()
cut_label = tk.Label(cut_show_frame,text="Show cutting lines")
cut_label.grid(row=3, column=0, padx=10, pady=5)
cut_toggle = tk.Checkbutton(cut_show_frame,variable=cut_val,command=update_img)
cut_toggle.grid(row=3, column=1, padx=10, pady=5)

#Settings toggles

orientation_frame = tk.Frame(settings_frame)
orientation_frame.grid(row=5, column=0)
orientation_label = tk.Label(orientation_frame,text="Orientation")
orientation_label.grid(row=0, column=0, padx=10, pady=5)
orientaion_pick = ttk.Combobox(orientation_frame,values=["Horizontal", "Virtical"])
orientaion_pick.current(0)
orientaion_pick.bind("<<ComboboxSelected>>",lambda _: update_img())
orientaion_pick.grid(row=0, column=1, padx=10, pady=5)

#Start button
go_button = tk.Button(settings_frame,text="go!",command=convert_map)
go_button.grid(row=6, column=1, padx=10, pady=5)

ui.mainloop()