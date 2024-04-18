import cv2 as cv
import numpy as np
from PIL import Image
import time

def detect_color(color_name):
    color = color_name
    cap = cv.VideoCapture(1)

    # Define color ranges in HSV format
    color_ranges = {
        'blue': ([110, 50, 50], [130, 255, 255]),
        'red': ([0, 50, 50], [60, 255, 255]),
        'green': ([40, 40, 40], [80, 255, 255]),
        'black': ([0, 0, 0], [179, 50, 30]),
    }

    # Check if the provided color name is in the dictionary
    if color_name.lower() not in color_ranges:
        print("Color not recognized.")
        return 0

    while True:
        # Take each frame
        _, frame = cap.read()

        if color == 'blue': frame = frame[270:390,410:620]
        if color == 'green': frame = frame[160:360,10:120]
        if color == 'black': frame = frame[360:470,120:310]
        # Convert BGR to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Define lower and upper limits for the specified color
        lower_limit, upper_limit = color_ranges[color_name.lower()]

        # Threshold the HSV image to get only the specified color
        mask = cv.inRange(hsv, np.array(lower_limit), np.array(upper_limit))

        # Bitwise-AND mask and original image
        res = cv.bitwise_and(frame, frame, mask=mask)

        # Count the number of non-zero pixels in the mask
        pixel_count = res.sum()

        # If pixels are detected, print the color name
        if "blue" in color.lower():
            if pixel_count > 100000:
                print(f"Detected color: {color_name}")
                return 1
            else:
                print("Finding your color")
                return 0 
        elif "red" in color.lower():
            if pixel_count > 10000:
                print(f"Detected color: {color_name}")
                return 1
            else:
                print("Finding your color")
                return 0
        elif "green" in color.lower():
            if pixel_count > 40000:
                print(f"Detected color: {color_name}")
                return 1
            else:
                print("Finding your color")
                return 0
        elif "black" in color.lower():
            if pixel_count > 7000:
                print(f"Detected color: {color_name}")
                return 1
            else:
                print("Finding your color")
                return 0

        # Display the original frame, mask, and result
        cv.imshow('frame', frame)
        cv.imshow('mask', mask)
        cv.imshow('res', res)

        # Convert mask to PIL Image to get bounding box
        mask_ = Image.fromarray(mask)
        bbox = mask_.getbbox()

        if bbox is not None:
            x1, y1, x2, y2 = bbox
            frame = cv.rectangle(frame, (x1, y1), (x2, y2), (255, 192, 203), 2)
            cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

# Example usage:
#color = input('color you are looking for: ')
color = 'blue'
print('we are looking for ', color)
detect_color(color)  
