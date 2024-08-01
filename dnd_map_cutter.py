import cv2 as cv
import numpy as np
import datetime as dt
import math as m

WIDTH = 1
HEIGHT = 0

#Squares per A4 page
PAGE_SQ_X = 8
PAGE_SQ_Y = 11.5

#Draws a vertical
def vertical_line(img:cv.Mat, colour:np.array, pos:int, size:int):
    img[:img.shape[HEIGHT],pos:pos+size] = colour

def horizontal_line(img:cv.Mat, colour:np.array, pos:int, size:int):
    img[pos:pos+size,:img.shape[WIDTH]] = colour

def grid(img:cv.Mat, colour:np.array, size:int, x_offset:int, y_offset:int, x_gap:int=1, y_gap:int=1):
    for x in range(int(img.shape[WIDTH]/x_gap)):
        vertical_line(img,colour,int(x*x_gap)+x_offset,size)
    for y in range(int(img.shape[HEIGHT]/y_gap)):
        horizontal_line(img,colour,int(y*y_gap)+y_offset,size)

#Copies a map to a new object
def copy_img(img:cv.typing.MatLike) -> cv.typing.MatLike:
    new_img = np.zeros((img.shape[HEIGHT],img.shape[WIDTH],3),np.uint8)
    new_img[:,:] = img[:,:]
    return new_img


#Generates an A4 Printable section
def new_print_page(img:cv.typing.MatLike,x_start,y_start,sw:int=0,sh:int=0,horizontal=False) -> cv.typing.MatLike:
    #Generates dimensions of a4 paper
    w = int(sw*PAGE_SQ_X)
    h = int(sh*PAGE_SQ_Y)
    
    #Generates blank img with a4 dimensions
    new_img = np.zeros([h,w,3],np.uint8)
    if horizontal:
        new_img = np.zeros([w,h,3],np.uint8)
    #Makes background white
    new_img[:,:] = 255

    #Converts start to pixels
    x_start = int(x_start*sw)
    y_start = int(y_start*sh)

    #Creates the area being copied
    copy_area = copy_area = img[y_start:y_start+h,x_start:x_start+w]
    if horizontal :
        copy_area = img[x_start:x_start+w,y_start:y_start+h]
        
    #Modifies the new img with the coppied area
    new_img[:copy_area.shape[HEIGHT],:copy_area.shape[WIDTH]] = copy_area

    #Returns the new img
    return new_img

#Gets valid map
img = None
while img is None:
    map_path = input("Map file: ")
    #Generates img obj reading from file
    try:
        img = cv.imread(cv.samples.findFile("{}".format(map_path)))
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


#Generates the amount of pixels to a square
square_dim = np.zeros(2) 
square_dim[WIDTH] = img.shape[WIDTH]/img_squares[WIDTH]
square_dim[HEIGHT] = img.shape[HEIGHT]/img_squares[HEIGHT]

#Generates a new copy of the img.
new_img = copy_img(img)

#Puts an inch grid over the img.
if grid_input:
    grid(new_img,np.array([0,0,0]),1,0,0,x_gap=square_dim[WIDTH],y_gap=square_dim[HEIGHT])

#Displays the imgs
cv.imshow("Original",img)
cv.imshow("New",new_img)

#Calculates how many pages to print
print_quant = [0,0]
print_quant[WIDTH] = m.ceil(img_squares[WIDTH]/PAGE_SQ_X)
print_quant[HEIGHT] = m.ceil(img_squares[HEIGHT]/PAGE_SQ_Y)
if horiz_input:
    print_quant[WIDTH] = m.ceil(img_squares[WIDTH]/PAGE_SQ_Y)
    print_quant[HEIGHT] = m.ceil(img_squares[HEIGHT]/PAGE_SQ_X)

print("Pages to print ",print_quant)

for y in range(print_quant[HEIGHT]):
    for x in range(print_quant[WIDTH]):
        cur = new_print_page(new_img,x_start=x*PAGE_SQ_X,y_start=y*PAGE_SQ_Y,sw=square_dim[WIDTH],sh=square_dim[HEIGHT],horizontal=horiz_input)
        try:   
            cv.imwrite("{}_{}.png".format(x,y),cur)
            cv.imshow("{}_{}.png".format(x,y),cur)
        except:
            pass


#Allows for updated img in window
while True:
    #Waits untill key is pressed
    k = cv.waitKey(1)
    cv.imshow("New",new_img)
    if k == ord("s"):
        cv.imwrite("new_img.png",new_img)
        break
    if k == ord("p"):
        break

