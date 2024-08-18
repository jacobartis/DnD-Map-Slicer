import cv2 as cv
import numpy as np
import datetime as dt
import math as m

WIDTH = 1
HEIGHT = 0

#Squares per A4 page
PAGE_SQ_X = 8
PAGE_SQ_Y = 11.5

def load_map(path) -> list:
    try:
        return cv.imread(cv.samples.findFile("{}".format(path)))
    except:
        return []

def calculate_grid_size(img,width:int,height:int):
    #Generates the amount of pixels to a square
    square_dim = np.zeros(2) 
    square_dim[WIDTH] = img.shape[WIDTH]/width
    square_dim[HEIGHT] = img.shape[HEIGHT]/height
    return square_dim

#Draws a vertical
def vertical_line(img:cv.Mat, colour:np.array, pos:int, size:int):
    img[:img.shape[HEIGHT],pos:pos+size] = colour

def horizontal_line(img:cv.Mat, colour:np.array, pos:int, size:int):
    img[pos:pos+size,:img.shape[WIDTH]] = colour

def grid(img:cv.Mat, colour:np.array, size:int, width, height):
    square_dim = calculate_grid_size(img,width,height)
    for x in range(m.ceil(img.shape[WIDTH]/square_dim[WIDTH])):
        vertical_line(img,colour,int(x*int(square_dim[WIDTH])),size)
    for y in range(m.ceil(img.shape[HEIGHT]/square_dim[HEIGHT])):
        horizontal_line(img,colour,int(y*int(square_dim[HEIGHT])),size)

#Copies a map to a new object
def copy_img(img:cv.typing.MatLike) -> cv.typing.MatLike:
    new_img = np.zeros((img.shape[HEIGHT],img.shape[WIDTH],3),np.uint8)
    new_img[:,:] = img[:,:]
    return new_img

#Generates an A4 Printable section
def new_print_page(img:cv.typing.MatLike,x_start,y_start,sw:int=0,sh:int=0,horizontal=False,page_width=PAGE_SQ_X,page_height=PAGE_SQ_Y) -> cv.typing.MatLike:
    #Generates dimensions of a4 paper
    w = int(sw*page_width)
    h = int(sh*page_height)
    print("w:{},h:{}".format(page_width,page_height))
    #Generates blank img with a4 dimensions
    new_img = np.zeros([h,w,3],np.uint8)
    if horizontal:
        new_img = np.zeros([w,h,3],np.uint8)
    #Makes background white
    new_img[:,:] = 255

    #Converts start to pixels
    x_start = int(x_start*sw)
    y_start = int(y_start*sh)
    print("s_x:{},s_y:{}".format(x_start,y_start))

    #Creates the area being copied
    copy_area = copy_area = img[y_start:y_start+h,x_start:x_start+w]
    if horizontal :
        copy_area = img[x_start:x_start+w,y_start:y_start+h]
        
    #Modifies the new img with the coppied area
    new_img[:copy_area.shape[HEIGHT],:copy_area.shape[WIDTH]] = copy_area

    #Returns the new img
    return new_img

#TODO Make it form and return an array of the maps
#Add save to different path option
def generate_printable_map(img, width:float, height:float, add_grid:bool=True, horizontal:bool=False, show:bool=False, page_width=PAGE_SQ_X, page_height=PAGE_SQ_Y):

    #Generates a new copy of the img.
    new_img = copy_img(img)
    square_dim = calculate_grid_size(new_img,width,height)
    #Puts an inch grid over the img.
    if add_grid:
        grid(new_img,np.array([0,0,0]),1,width,height)

    #Displays the imgs
    if show:
        cv.imshow("Original",img)
        cv.imshow("New",new_img)

    #Calculates how many pages to print
    print_quant = [0,0]
    print_quant[WIDTH] = m.ceil(width/page_width)
    print_quant[HEIGHT] = m.ceil(height/page_height)
    if horizontal:
        print_quant[WIDTH] = m.ceil(width/page_height)
        print_quant[HEIGHT] = m.ceil(height/page_width)

    print("Pages to print ",print_quant)

    for y in range(print_quant[HEIGHT]):
        for x in range(print_quant[WIDTH]):
            print("x:{},y:{}".format(x,y))
            cur = new_print_page(new_img,x_start=x*page_width,y_start=y*page_height,sw=square_dim[WIDTH],
                                 sh=square_dim[HEIGHT],horizontal=horizontal, page_width=page_width, page_height=page_height)
            try:   
                cv.imwrite("{}_{}.png".format(x,y),cur)
                if show:
                    cv.imshow("{}_{}.png".format(x,y),cur)
            except Exception as e:
                print(e)
                pass
    cv.imwrite("new_img.png",new_img)

def main():
    #Gets valid map
    img = None
    while img is None:
        map_path = input("Map file: ")
        #Generates img obj reading from file
        try:
            img = load_map(map_path)
            print("Img dim",img.shape)
        except:
            print("map not found.")

    #User input for map size in squares
    img_squares = np.zeros(2)
    while not img_squares[WIDTH]:
        x_squares = input("Enter img width in squares.")
        try:
            assert int(x_squares)>0
            img_squares[WIDTH] = int(x_squares)
            break
        except:
            print("Please enter a valid number.")

    while not img_squares[HEIGHT]:
        y_squares = input("Enter img height in squares.")
        try:
            assert int(y_squares)>0
            img_squares[HEIGHT] = int(y_squares)
            print("Img square dim",img_squares)
            break
        except:
            print("Please enter a valid number.")

    #User input for drawing extra grid
    grid_input = None

    while not grid_input:
        g_in = input("Add grid to pages? (y/n)").capitalize()
        try:
            assert g_in == "Y" or g_in == "N"
            grid_input = g_in == "Y"
            print("Add grid: ",grid_input)
            break
        except:
            print("Please enter y or n")

    #User input for creating horizontal images
    horiz_input = None

    while not horiz_input:
        h_in = input("Horrizontal pages? (y/n)").capitalize()
        try:
            assert h_in == "Y" or h_in == "N"
            horiz_input = h_in == "Y"
            print("Horizontal pages: ",grid_input)
            break
        except:
            print("Please enter y or n")

    generate_printable_map(img, img_squares[WIDTH],img_squares[HEIGHT],grid_input,horiz_input)

if __name__ == "__main__":
    main()