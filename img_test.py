import cv2 as cv
import sys

#Generates img obj reading from file
img = cv.imread(cv.samples.findFile("test_img.png"))

#Exits if img is invalid
if img is None:
    quit()

#Displays the img
cv.imshow("Display window",img)

#Waits untill key is pressed
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("test_img.png")