import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import random


cap = cv2.VideoCapture(1)

cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)

timer = 0
start_game = False
state_results = False
txt=''

scores = [0,0] #[ai, you]

color = None

while True:
    img_bg = cv2.imread('Resources/BG.png')
    ret, img = cap.read()
    img_scaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    img_scaled = img_scaled[:,80:480]

    hands, img = detector.findHands(img_scaled) 

    #txt= ''
    ai_win = False
    you_win = False
    draw = False

    #print(hands)

    if start_game:

        if state_results is False:
            timer = time.time() - initial_time
            cv2.putText(img_bg, str(int(timer)), (605,435), cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 4)
            
            if timer > 3:
                state_results = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    
                    fingers_count = fingers.count(1)
                    
                    player_move = None
                    if fingers_count == 0:
                        player_move = 1

                    if fingers_count == 5:
                        player_move = 2

                    if fingers_count == 2:
                        player_move = 3
                    
                    random_num = random.randint(1,3)
                    img_ai = cv2.imread(f"Resources/{random_num}.png", cv2.IMREAD_UNCHANGED)
                    img_bg = cvzone.overlayPNG(img_bg, img_ai, (149, 310))


                    if (player_move==1 and random_num ==3) or (player_move==2 and random_num==1) or (player_move==3 and random_num==2):
                        scores[1]+=1
                        txt='WIN'
                        color = (0,255,0)

                    elif (player_move==3 and random_num ==1) or (player_move==1 and random_num==2) or (player_move==2 and random_num==3):
                        scores[0]+=1

                        txt='LOSE'
                        color = (0,0,255)

                    else:
                        txt= 'DRAW'
                        color = (255,0,0)


                    

    if state_results:
        img_bg = cvzone.overlayPNG(img_bg, img_ai, (149, 310))

    cv2.putText(img_bg, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(img_bg, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(img_bg,f'{txt}',(550,215),cv2.FONT_HERSHEY_PLAIN, 4, color, 6)

    img_bg[234:654, 795:1195] = img_scaled
    cv2.imshow('bg', img_bg)


    key = cv2.waitKey(1)

    if key == ord('s'):
        start_game = True
        initial_time = time.time()
        state_results = False
        
        



