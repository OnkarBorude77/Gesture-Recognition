import cv2
import pyautogui
from recognize_gesture import GestureRecognizer


print("Starting...")
cap = cv2.VideoCapture(0)

recognizer = GestureRecognizer()

print("Gesture Controller Started. Open your presentation! Press 'Esc' to quit.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    
    image = cv2.flip(image, 1)
    
   
    action, annotated_image = recognizer.detect_gesture(image)
    
 
    if action == "NEXT":
        print("ACTION: Next Slide")
        pyautogui.press('right')

    elif action == "PREV":
        print("ACTION: Previous Slide")
        pyautogui.press('left')

    cv2.imshow('AI Gesture Controller', annotated_image)
    if cv2.waitKey(5) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
print("Webcam closed.")