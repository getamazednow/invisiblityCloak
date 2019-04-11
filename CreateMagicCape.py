#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Derived from SubhadityaMukherjee/invisiblityCloak github work and enhanced by me
# Duane Gomes - getamazednow
# USAGE: This is where you create the MAGIC CAPE. This program will give you the tools

# We could supply a Scene Image as the background but the color tones wont be correct.
# as video with many frames allows for averaging out the frame brighton much like HDR
# supply only ONE immage if you are using an Image as your scene.
# (python) range-detector --filter RGB --image /path/to/image.png
# or We can use a video clip from a video camera, default is inbuilt laptop cam
# (python) range-detector --filter HSV --webcam

# This is the configuration program to capture the video background that will
# become the scene for the Invisible act. This needs to be a Pickle serialisation 
# a few minutes so as to capture the background correctly in proper lighting.
# it can also be used to identify the COLOR for the MASK to create the Cloak.
##

# we want the open CV2 Visual cognition Library and its functions
import cv2
# We want to have the ability to parse command line arguments given at run time
import argparse
# We want to ensure we have bitwise XOR operator for the MASK function
from operator import xor
# We need the Pickle serialisation library to go from object to bit stream 
# and vice versa if required, much like JSON is serialisation for the web. 
import pickle

# This function allows recursive callback of the function in which it is placed until a waitkey is pressed
# and then it returns the value of the key to determine if any action is required or the call back continues
def callback(value):
    pass

# Set up the Color Masker picker dialog and sliders for us to continiually select the best bask that 
# excludes everything other than the MASK object from view. So that we can make a note of the color required

def setup_trackbars(range_filter):
# create the windows window that will contain the UI

    cv2.namedWindow("Trackbars", 0)
# Determin the bounded values and ensure u stay within the bounds
    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

# Actually start the UI and stay operational until the wait key is pressed, continually adjusting the 
# HSV or RGB palette as required until the user has configured the right mask.
        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)

# Fetch and process the arguments present at the Command line during instantiation of the program
def get_arguments():
    # parse the command linee and add the key value pairs of arguments for decision making
    ap = argparse.ArgumentParser()
    # Does the user want to use the RGB or HSV Palette of color detection
    ap.add_argument('-f', '--filter', required=True,
                    help='Range filter. RGB or HSV')
    # Does the user want to use the IMAGE method of supplying the Scene
    ap.add_argument('-i', '--image', required=False,
                    help='Path to the image')
    # Does the user want to use the WEBCAM and live video feed as the scene 
    ap.add_argument('-w', '--webcam', required=True,
                    help='Use webcam', action='store_true')
    # Does the user want a LIVE preview of the Mask creation process.
    ap.add_argument('-p', '--preview', required=True,
                    help='Show a preview of the image after applying the mask',
                    action='store_true')
    args = vars(ap.parse_args())

# Check to see that we have a valid scene source value or abort on error
    if not xor(bool(args['image']), bool(args['webcam'])):
        ap.error("Please specify only one image source")
# Check to see if we have the right color palette argument if not abort with an error
    if not args['filter'].upper() in ['RGB', 'HSV']:
        ap.error("Please speciy a correct filter.")

    return args

# Activate the MASK Creation tool UI and stay active until the user terminates
# Constantly returning the values the user selected
def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)

    return values

# This is where the execution of the code will start.
def main():
    args = get_arguments()
# Convert the filter argument to upper case for use
    range_filter = args['filter'].upper()

# check if the user wants to use an image
    if args['image']:
        image = cv2.imread(args['image'])

# check if the RGB paletter is selected, if so use the image which by default is RGB
        if range_filter == 'RGB':
            frame_to_thresh = image.copy()
        else:
# if HSV, then convert the image into the HSV format for better color range for mask detection
# We need to have the best color range to be able to mask edging and shadows properly in the real world
            frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    else:

# Attempt to capture the video feed from the camera a video was selected
        camera = cv2.VideoCapture(1)
# if a feed is active and available continue capturing 
        if camera.read()[0] == False:
            camera = cv2.VideoCapture(0)

# Call up the MASK configuration UI so that the mask setting can be done.
    setup_trackbars(range_filter)

    while True:
        if args['webcam']:
            ret, image = camera.read()

            if not ret:
                break

            if range_filter == 'RGB':
                frame_to_thresh = image.copy()
            else:
                frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# Put the colors from the Sliderbars into the variables we intend to use for the mask
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)
        #v1_min, v2_min, v3_min = [0,98,107]
        #v1_max, v2_max, v3_max = [0,255,253]

# Create the range for the mask
        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
        #thresh = cv2.inRange(frame_to_thresh, (lower_red), (upper_red))
# if a preview is requested then SHOW a live preview of the masking occuring
        if args['preview']:
            preview = cv2.bitwise_and(image, image, mask=thresh)
            cv2.imshow("Preview", preview)
        else:
# if no preview requested then dont show the masking occuring
            cv2.imshow("Original", image)
            cv2.imshow("Thresh", thresh)

# if a wait key is detected CTRL C or the designated key q in this case then clean up and quit
        if cv2.waitKey(1) & 0xFF is ord('q'):
            t =  (v1_min, v2_min, v3_min, v1_max, v2_max, v3_max)
            #t =  (lower_red,upper_red)
        # clear the buffer serialisation  of the data stream in memory
            with open("range.pickle", "wb") as f:
                pickle.dump(t,f)
            break

# Actually start the MAIN sequence
if __name__ == '__main__':
    main()