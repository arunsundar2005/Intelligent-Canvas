import cv2
import numpy as np
import time
import os
import handTracking as HT

folderpath = "UI_props"
path_list = os.listdir(folderpath)
# print(path_list)
img_list = []

for imPath in path_list:
    image = cv2.imread(f"{folderpath}/{imPath}")
    img_list.append(image)
# print(len(img_list))
header = img_list[0]

cap = cv2.VideoCapture(0)
cap.set(3, 1280) # width
cap.set(4, 720) # height


# actual_width = int(cap.get(3))
# actual_height = int(cap.get(4))
# print(f"Camera resolution: {actual_width}x{actual_height}")

detector = HT.handDetector(detectionCon=0.85)

# Create Drawing Canvas
canvas = np.zeros((720, 1280, 3), np.uint8)



# User_variables
# 1. Color Declaration 

pen_color = (225, 105, 65)
pencil_color = (0, 0, 0)
draw_color = (255, 255, 255)

# 2. Pen Settings

stroke = 15
xp, yp = 0, 0

while True:

    
    """
    Steps  Involved:
    1. Import Headers
    2. Find hand landmarks
    3. Check which fingers are up
    4. Selection Mode : 2 fingers up
    5. Drawing mode : 1 finger up
    """




    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Step 2:
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)

    
    cv2.rectangle(img, (50, 200), (200, 250), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, "Clear", (55,240), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.rectangle(img, (950, 200), (1230, 250), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, "Ask MAVIS", (955,240), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255), 1, cv2.LINE_AA)
    if len(lmlist[0])!=0:
        # print(lmlist[0])
        

        # Finding the landmarks of index and middle finger
        x1, y1 = lmlist[0][8][1:] # 8 -> Index Finger
        x2, y2 = lmlist[0][12][1:] # 12 -> Middle Finger
    

        # # Step 3:
        fingers = detector.fingersUp()
        # print(fingers)

        # Step 4:
        
        if fingers[1] and fingers[2]:
            cv2.rectangle(img, (x1, y1-25), (x2, y2+25), pen_color, cv2.FILLED)
            # print("Selection Mode")
            # Selecting Drawing tool
            if y1< 160: # The finger in selection mode is inside the header for chosing the tool
                if 505<x1<550 :
                    header = img_list[1]
                    print(f"Selected Pen")
                    draw_color = pen_color
                if 620<x1<690 :
                    header = img_list[2]
                    print("Selected Pencil")
                    draw_color = pencil_color
                if 735<x1<845 :
                    header = img_list[3]
                    print("Selected Eraser")
                    draw_color = (0,0,0)
            if 50<x1<200 and 200<y1<250:
                print("Cleared All")
                canvas = np.zeros((720, 1280, 3), np.uint8)
            if 950<x1<1230 and 200<y1<250:
                print("Asking LLM ...")
                cv2.imwrite("img_to_ask.png", canvas)
        # print(f"[{x1},{y2}]")
       
                     


        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1,y1), 15, draw_color, cv2.FILLED)
            # print("Drawing Mode")

            # Drawing
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            cv2.line(img, (xp, yp), (x1, y1), draw_color, stroke)
            cv2.line(canvas, (xp, yp), (x1, y1), draw_color, stroke)
        xp, yp = x1, y1
    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, canvas)
    
    img[0:160, 0:1280] = header # Step 1
    # img = cv2.addWeighted(img, 0.5, canvas,0.5, 0)

    cv2.imshow("Canvas", img)
    # cv2.imshow("Drawing Canvas", canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 