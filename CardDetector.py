############## Python-OpenCV Playing Card Detector ###############
#
# Author: Evan Juras
# Date: 9/5/17
# Description: Python script to detect and identify playing cards
# from a PiCamera video feed.
#

# Import necessary packages
import cv2
import numpy as np
import time
import os
import Cards
import VideoStream
import pokerMain
import tkinter as tk


### ---- INITIALIZATION ---- ###
# Define constants and initialize variables

## Camera settings
IM_WIDTH = 1280
IM_HEIGHT = 720
FRAME_RATE = 600  # 300

## Initialize calculated frame rate because it's calculated AFTER the first time it's displayed
frame_rate_calc = 1
freq = cv2.getTickFrequency()

## Define font to use
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize camera object and video feed from the camera. The video stream is set up
# as a seperate thread that constantly grabs frames from the camera feed.
# See VideoStream.py for VideoStream class definition
## IF USING USB CAMERA INSTEAD OF PICAMERA,
## CHANGE THE THIRD ARGUMENT FROM 1 TO 2 IN THE FOLLOWING LINE:
videostream = VideoStream.VideoStream((IM_WIDTH, IM_HEIGHT), FRAME_RATE, 3, 0).start()
time.sleep(1)  # Give the camera time to warm up

# Load the train rank and suit images
path = os.path.dirname(os.path.abspath(__file__))
train_ranks = Cards.load_ranks(path + '/Card_Imgs/')
train_suits = Cards.load_suits(path + '/Card_Imgs/')

### ---- MAIN LOOP ---- ###
# The main loop repeatedly grabs frames from the video stream
# and processes them to find and identify playing cards.

root = tk.Tk()
label1 = tk.Label(root, text="", font=("Helvetica", 40))
label1.pack(pady=40)
label2 = tk.Label(root, text="The Cards Are: ", font=("Helvetica", 30),wraplength=1280)
label2.pack(pady=40)
label4 = tk.Label(root, text=" ", font=("Helvetica", 40),wraplength=1280)
label4.pack(pady=40)
label3 = tk.Label(root, text=" ", font=("Helvetica", 30),wraplength=1280)
label3.pack(pady=40)

root.title("POKER AI")

root.geometry("1280x650")
# Function to update the Tkinter label text
def update_label(check,color):
    label1.config(text="You Should: " + check, fg=color)
    label1.update_idletasks()
    label2.config(text="The Cards Are: " + str(pokerMain.detectedCardList), fg="black")
    label2.update_idletasks()
    label3.config(text= pokerMain.oddsString, fg="black")
    label3.update_idletasks()
    label4.config(text= pokerMain.handString, fg="black")
    label4.update_idletasks()

# Function to check if the Tkinter window is closed
def check_window_closed():
    root.update()
    if not tk._default_root:
        return True
    return False

# Schedule the update_label function every 100 milliseconds
root.after(100, lambda: update_label(" ", "black"))

cam_quit = False  # Loop control variable

while not cam_quit:

    # Grab frame from video stream
    image = videostream.read()

    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    # Pre-process camera image (gray, blur, and threshold it)
    pre_proc = Cards.preprocess_image(image)

    # Find and sort the contours of all cards in the image (query cards)
    cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)

    # If there are no contours, do nothing
    if len(cnts_sort) != 0:

        # Initialize a new "cards" list to assign the card objects.
        # k indexes the newly made array of cards.
        cards = []
        k = 0

        # For each contour detected:
        for i in range(len(cnts_sort)):
            if (cnt_is_card[i] == 1):
                # Create a card object from the contour and append it to the list of cards.
                # preprocess_card function takes the card contour and contour and
                # determines the cards properties (corner points, etc). It generates a
                # flattened 200x300 image of the card, and isolates the card's
                # suit and rank from the image.
                cards.append(Cards.preprocess_card(cnts_sort[i], image))

                # Find the best rank and suit match for the card.
                cards[k].best_rank_match, cards[k].best_suit_match, cards[k].rank_diff, cards[
                    k].suit_diff = Cards.match_card(cards[k], train_ranks, train_suits)

                # Draw center point and match result on the image.
                image = Cards.draw_results(image, cards[k])
                k = k + 1

        # Draw card contours on image (have to do contours all at once or
        # they do not show up properly for some reason)
        if (len(cards) != 0):
            temp_cnts = []
            for i in range(len(cards)):
                temp_cnts.append(cards[i].contour)
            cv2.drawContours(image, temp_cnts, -1, (255, 0, 0), 2)

    # Draw framerate in the corner of the image. Framerate is calculated at the end of the main loop,
    # so the first time this runs, framerate will be shown as 0.
    cv2.putText(image, "FPS: " + str(int(frame_rate_calc)), (10, 26), font, 0.7, (255, 0, 255), 2, cv2.LINE_AA)
    # this is were we will put a function to give the suggestion
    # Finally, display the image with the identified cards
    cv2.imshow("Poker Vision", image)

    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1 #567
    if pokerMain.counter == 2:
        toDo = pokerMain.startHandCheck()
        if toDo == "Buy-In":
            color = "green"
        elif toDo == "Fold or Buy-In if you feel lucky":
            color = "red"
        root.after(1, lambda: update_label(toDo,color))

    if pokerMain.counter == 5:
        toDo = pokerMain.handCheckTwo()
        if toDo == "OK Hand: Check, Call, or Raise":
            color = "green"
        elif toDo == "Check if possible or fold":
            color = "red"
        root.after(1, lambda: update_label(toDo,color))

    if pokerMain.counter == 6:
        toDo = pokerMain.handCheckThree()
        if toDo == "OK Hand: Check or Bluff":
            color = "yellow"
        elif toDo == "GOOD Hand: Check, Call, or Raise":
            color = "green"
        elif toDo == "GREAT Hand: Check, Call or Raise":
            color = "green"
        elif toDo == "BAD Hand: Check if possible or fold":
            color = "red"
        root.after(1, lambda: update_label(toDo, color))

    if pokerMain.counter == 7:
        toDo = pokerMain.finalHandCheck()
        if toDo == "OK Hand: Check or Fold":
            color = "yellow"
        elif "GOOD Hand" in toDo or "GREAT Hand" in toDo:
            color = "green"
        elif toDo == "THE BEST HAND: ALL IN BABY":
            color = "blue"
        elif toDo == "BAD Hand: Check if possible or fold":
            color = "red"
        else:
            color = "black"  # Default color if none of the conditions match
        root.after(1, lambda: update_label(toDo, color))

    if check_window_closed():
        cam_quit = True
    # Poll the keyboard. If 'q' is pressed, exit the main loop.
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = True

# Close all windows and close the PiCamera video stream.
cv2.destroyAllWindows()
videostream.stop()

