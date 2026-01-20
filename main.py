import cv2
import numpy as np
import mss
import pyautogui
import time

# إعدادات متجر ريڤن - نظام التتبع الذكي
SMOOTHING = 7      # كلما زاد الرقم كان التتبع أنعم وأصعب في الكشف
FOV_SIZE = 200     # دائرة البحث وسط الشاشة
LOWER_RED = np.array([0, 150, 150]) 
UPPER_RED = np.array([10, 255, 255])

def raven_engine():
    sct = mss.mss()
    width, height = pyautogui.size()
    monitor = {
        "top": int(height/2 - FOV_SIZE/2),
        "left": int(width/2 - FOV_SIZE/2),
        "width": FOV_SIZE,
        "height": FOV_SIZE
    }
    
    print("نظام ريڤن AI يعمل.. بانتظار الهدف")
    
    while True:
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_RED, UPPER_RED)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 50:
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # تحريك الماوس بنعومة نحو الهدف
                    pyautogui.move((cx - FOV_SIZE/2) / SMOOTHING, (cy - FOV_SIZE/2) / SMOOTHING)
        time.sleep(0.01)

if __name__ == "__main__":
    raven_engine()
