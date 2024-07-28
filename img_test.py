import cv2 as cv
import numpy as np

#Draws a vertical
def vertical_line(img:cv.Mat, colour:np.array, pos:int, size:int):
    img[0:img.shape[0],pos:pos+size] = colour

def horizontal_line(img:cv.Mat, colour:np.array, pos:int, size:int):
    img[pos:pos+size,0:img.shape[1]] = colour

#Generates img obj reading from file
img = cv.imread(cv.samples.findFile("test_img.png"))

#Exits if img is invalid
if img is None:
    quit()
size = img.shape[:2]
print(size)
vertical_line(img,np.array([255,0,0]),int(size[0]/2),5)
horizontal_line(img,np.array([255,0,0]),int(size[1]/2),5)

#Displays the img
cv.imshow("Display window",img)

#Waits untill key is pressed
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("test_img.png")
