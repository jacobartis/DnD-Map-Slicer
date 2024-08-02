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
        dnd_map_cutter.generate_printable_map(map_img,int(map_width.get()),int(map_height.get()),grid_val.get(),orientaion_pick.get()=="Horizontal",show_val.get())
    except Exception as e:
        print(e)
        return

def update_img():
    if not MapPath:
        print("no map")
        return
    #Uses PIL to open and resize the img
    map_img = dnd_map_cutter.load_map(MapPath)
    if grid_val.get():
        dnd_map_cutter.grid(map_img,[0,0,0],3,int(map_width.get()),int(map_height.get()))
    if orientaion_pick.get()=="Horizontal":
        dnd_map_cutter.grid(map_img,[255,0,0],5,int(map_width.get())/11.5,int(map_height.get())/8)
    else:
        dnd_map_cutter.grid(map_img,[255,0,0],5,int(map_width.get())/8,int(map_height.get())/11.5)

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
width_label = tk.Label(settings_frame,text="Width: ")
width_label.grid(row=0, column=0, padx=10, pady=5)
map_width = tk.Spinbox(settings_frame,command=update_img,from_=1, to=1000)
map_width.grid(row=0, column=1, padx=10, pady=5)

height_label = tk.Label(settings_frame,text="Height: ")
height_label.grid(row=1, column=0, padx=10, pady=5)
map_height = tk.Spinbox(settings_frame,command=update_img,from_=1, to=1000)
map_height.grid(row=1, column=1, padx=10, pady=5)

#Settings toggles
grid_val = tk.BooleanVar()
grid_label = tk.Label(settings_frame,text="Draw Grid: ")
grid_label.grid(row=2, column=0, padx=10, pady=5)
grid_toggle = tk.Checkbutton(settings_frame,variable=grid_val,command=update_img)
grid_toggle.grid(row=2, column=1, padx=10, pady=5)


orientation_label = tk.Label(settings_frame,text="Orientation")
orientation_label.grid(row=3, column=0, padx=10, pady=5)
orientaion_pick = ttk.Combobox(settings_frame,values=["Horizontal", "Virtical"])
orientaion_pick.current(0)
orientaion_pick.bind("<<ComboboxSelected>>",lambda _: update_img())
orientaion_pick.grid(row=3, column=1, padx=10, pady=5)

show_val = tk.BooleanVar()
show_label = tk.Label(settings_frame,text="Show output")
show_label.grid(row=4, column=0, padx=10, pady=5)
show_toggle = tk.Checkbutton(settings_frame,variable=show_val)
show_toggle.grid(row=4, column=1, padx=10, pady=5)

#Start button
go_button = tk.Button(settings_frame,text="go!",command=convert_map)
go_button.grid(row=5, column=1, padx=10, pady=5)

ui.mainloop()