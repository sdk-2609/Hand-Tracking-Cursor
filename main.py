import time
import cv2
import mediapipe as mp
import pyautogui 
import math

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height=pyautogui.size()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(3, 640)
cap.set(4, 480)

palm_id=[1,5,9,13,17]

deadzone=10
pinchstart=30
def main():
    prev_x, prev_y = screen_width//2, screen_height//2

    with mp_hands.Hands(
        max_num_hands=1,
        #max_tracking_confidence=0.7,
        #max_detection_confidence=0.7,
    ) as hands:

        while True:

            attempt = 0
            success, img = cap.read()

            while not success and attempt < 5:
                time.sleep(0.2)
                success, img = cap.read()
                attempt += 1

            if not success:
                print("failed to read frame")
                break

            img = cv2.flip(img, 1)
            h,w,_=img.shape

            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb)

            if results.multi_hand_landmarks:

                for hand_landmarks in results.multi_hand_landmarks:

                    index_tip=hand_landmarks.landmark[8]
                    thumb_tip=hand_landmarks.landmark[4]

                    #cx= sum(hand_landmarks.landmark[id].x for id in palm_id)/len(palm_id)
                    #cy= sum(hand_landmarks.landmark[id].y for id in palm_id)/len(palm_id)
                    middle_tip = hand_landmarks.landmark[12]

                    screen_x = int(middle_tip.x * screen_width)
                    screen_y = int(middle_tip.y * screen_height)
                    
                    #screen_x= int(cx*screen_width)
                    #screen_y = int(cy*screen_height)

                    dx= screen_x-prev_x
                    dy= screen_y-prev_y

                    if math.hypot(dx, dy)>deadzone:
                        pyautogui.moveTo(
                            screen_x,
                            screen_y,
                            duration=0.1,
                        )
                        prev_x=screen_x
                        prev_y=screen_y

                    ix,iy=int(index_tip.x*w), int(index_tip.y*h)
                    tx, ty = int(thumb_tip.x * w) , int(thumb_tip.y * h)

                    pinchdistance=math.hypot(ix-tx,iy-ty)

                    if pinchdistance<pinchstart:
                        pyautogui.click()

                
            cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()