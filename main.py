import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
import webbrowser
 
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
 
detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/" , "BSP"],
        ["GGL", "YTB", "CLR", "EXT"]]
finalText = ""
 
keyboard = Controller()
 
 
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        # Fit text for Google, YouTube, Clear, Exit
        if button.text in ["GGL", "YTB", "CLR", "EXT", "BSP"]:
            font_scale = 2
            text_size = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, font_scale, 4)[0]
            text_x = x + (w - text_size[0]) // 2
            text_y = y + (h + text_size[1]) // 2
            cv2.putText(img, button.text, (text_x, text_y),
                        cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 255, 255), 4)
        else:
            cv2.putText(img, button.text, (x + 20, y + 65),
                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img
 
#
# def drawAll(img, buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#         x, y = button.pos
#         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
#                           20, rt=0)
#         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
#                       (255, 0, 255), cv2.FILLED)
#         cv2.putText(imgNew, button.text, (x + 40, y + 60),
#                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#
#     out = img.copy()
#     alpha = 0.5
#     mask = imgNew.astype(bool)
#     print(mask.shape)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
#     return out
 
 
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
 
 
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

break_program = False
while not break_program:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    lmList, bboxInfo = None, None
    if hands:
        lmList = hands[0]["lmList"]  # List of 21 landmarks
        bboxInfo = hands[0]["bbox"]   # Bounding box info
        # Draw blue box around hand
        x, y, w, h = bboxInfo
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Draw blue points on hand landmarks
        for lm in lmList:
            cv2.circle(img, (lm[0], lm[1]), 8, (255, 0, 0), cv2.FILLED)
    img = drawAll(img, buttonList)
 
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
 
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                if lmList is not None:
                    l, _, _ = detector.findDistance(lmList[4][0:2], lmList[8][0:2], img)
                    print(l)
 
                ## when clicked
                if l < 28:
                    if button.text == "GGL":
                        if finalText.strip():
                            webbrowser.open(f"https://www.google.com/search?q={finalText.strip()}")
                        else:
                            webbrowser.open("https://www.google.com")
                        finalText = ""
                    elif button.text == "YTB":
                        if finalText.strip():
                            webbrowser.open(f"https://www.youtube.com/results?search_query={finalText.strip()}")
                        else:
                            webbrowser.open("https://www.youtube.com")
                        finalText = ""
                    elif button.text == "CLR":
                        finalText = ""
                    elif button.text == "EXT":
                        break_program = True
                        break
                    elif button.text == "BSP":
                        if len(finalText)!=0:
                            finalText=finalText[0:len(finalText)-1]
                    elif button.text == 'BSP':
                        if len(finalText)!=0:
                            finalText=finalText[0:len(finalText)-1]
                    elif button.text=='<':
                        if len(finalText)!=0:
                            finalText=finalText[0:len(finalText)-1]
                    else:
                        finalText += button.text
                    sleep(0.5)
 
    cv2.rectangle(img, (50, 500), (700, 600), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, finalText, (60, 580),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  