#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Derived from SubhadityaMukherjee/invisiblityCloak github work and enhanced by me
# Duane Gomes - getamazednow
# USAGE: This program will access you LAPTOP CAMERA and stream a video feed to a WINDOW.
# You can then go INVISIBLE using a RED CAPE and become magical.

# We need the Open CV 2 Library
import cv2
# we need the time module to be able to slice frames
import time
# we need the numpy module to work with python code
import numpy as np
# We need the pickle module to do object serialisation for the web
import pickle

# Set up the serialisation module and the variable arrays required for the mask
with open('range.pickle','rb') as f:
    t = pickle.load(f)

#Mask variables
lower_red = np.array([t[0],t[1],t[2]])
upper_red = np.array([t[3],t[4],t[5]])

# Commence Video Capture
cap = cv2.VideoCapture(0)
# Create a delay so it can be seen
time.sleep(3)
background = 0



#initial capture of scene background to ensure it can match the mask and scene during configuration

for i in range(50):
    ret,background = cap.read()

background = np.flip(background,axis = 1)

# Then continue until interrupted by the user.
while True:
    # Capture the video feed
    ret,img = cap.read()
    # grab the video frame
    img = np.flip(img,axis=1)
    # Convert to the HSV mask
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # Locate the MASK object
    mask1 = cv2.inRange(hsv,lower_red,upper_red)

    # Apply 2 alogrithms from the Open CV2 library that are good at creating the morph
    # We need to morph the scene with the MASK there by obliterating the MASK with the scene
    # Thus creating the invisible illusion
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    # apply the mask to the video frame grabbed pass 1 
    mask2 = cv2.bitwise_not(mask1)
    # apply the mask to the video frame grabbed pass 2
    res1 = cv2.bitwise_and(img,img,mask=mask2)
    # apply and flatten the morphed image with the scene
    res2 = cv2.bitwise_and(background,background,mask=mask1)
    # Compose the output frame
    final = cv2.addWeighted(res1,1,res2,1,0)
    # Display the final magic in the output feed
    cv2.imshow("Duanes Harry Potter Magic",final)
    # Keey doing this until the user terminates
    cv2.waitKey(1)
