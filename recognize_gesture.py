import cv2
import mediapipe as mp
import time

class GestureRecognizer:
    def __init__(self, swipe_threshold=150, cooldown=1.5):
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, 
                                         min_tracking_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

        
        self.gesture_start_x = 0
        self.last_action_time = 0
        self.SWIPE_THRESHOLD = swipe_threshold
        self.COOLDOWN_SECONDS = cooldown

    def detect_gesture(self, image):
     
        
      
        action = "NONE"
        gesture_detected = False
        
    
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                self.mp_draw.draw_landmarks(image, hand_landmarks, 
                                            self.mp_hands.HAND_CONNECTIONS)
                
               
                index_tip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                index_base_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y
                middle_tip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                middle_base_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

                is_pointing = (index_tip_y < index_base_y) and (middle_tip_y > middle_base_y)
                
                if is_pointing:
                    gesture_detected = True
                    current_x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image.shape[1])
                    cv2.circle(image, (current_x, int(index_tip_y * image.shape[0])), 10, (0, 255, 0), -1)

                    if self.gesture_start_x == 0:
                        self.gesture_start_x = current_x
                        
                    
                    if (time.time() - self.last_action_time) > self.COOLDOWN_SECONDS:
                       
                        if (current_x - self.gesture_start_x) > self.SWIPE_THRESHOLD:
                            action = "PREV" 
                            self.last_action_time = time.time()
                            self.gesture_start_x = 0
                            
                    
                        elif (self.gesture_start_x - current_x) > self.SWIPE_THRESHOLD:
                            action = "NEXT"
                            self.last_action_time = time.time()
                            self.gesture_start_x = 0

        if not gesture_detected:
            self.gesture_start_x = 0

        return action, image