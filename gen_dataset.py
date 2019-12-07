import cv2
import os
import numpy as np

DS_DIR = "dataset"


def main():
    print("""Controls:
        a -> set new background
        s -> start/stop set capture
        esc/q -> quit""")

    
    cap = cv2.VideoCapture(0)
    key = -1
    bg = None
    dirno = 0
    frameno = 0
    bgs = cv2.createBackgroundSubtractorKNN()
    
    if not os.path.exists(DS_DIR):
        os.mkdir(DS_DIR)


    while key != 27 and key != 113: # esc and q
        ret, frame = cap.read()
        frame = cv2.GaussianBlur(frame, (0,0), 2)

        if bg is not None:
            fg = frame.astype(np.int16) - bg.astype(np.int16)
            fg = np.abs(fg).astype(np.uint8)
            fg = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)
            _, fg = cv2.threshold(fg, 10, 255, cv2.THRESH_BINARY)

            fg = bgs.apply(frame)
            
            morph = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,15)), iterations=2)

            cv2.imshow("fg", fg)
            cv2.imshow("morph", morph)

        cv2.imshow("original", frame)

        key = cv2.waitKey(1)


        if key == 97: # a
            bg = frame
            bgs = cv2.createBackgroundSubtractorKNN()
        elif key == 115: # s
            pass
        elif key != -1:
            print(key)


if __name__ == '__main__':
    main()
