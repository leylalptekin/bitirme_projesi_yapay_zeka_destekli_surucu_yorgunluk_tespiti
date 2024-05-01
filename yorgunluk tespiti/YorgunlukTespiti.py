import dlib
import sys
import cv2
import time
import numpy as np
from scipy.spatial import distance as dist
from threading import Thread
import playsound
import queue
import chime
from imutils import face_utils


FACE_DOWNSAMPLE_RATIO = 1.5
RESIZE_HEIGHT = 460

thresh = 0.27
modelPath = "models/shape_predictor_70_face_landmarks.dat"
sound_path = "alarm.wav"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(modelPath)

leftEyeIndex = [36, 37, 38, 39, 40, 41]
rightEyeIndex = [42, 43, 44, 45, 46, 47]

blinkCount = 0
yorgunluk = 0
state = 0
blinkTime = 0.15 #150ms
yorgunlukzamani = 1.5  #1500ms
ALARM_ON = False
GAMMA = 1.5
threadStatusQ = queue.Queue()

invGamma = 1.0/GAMMA
table = np.array([((i / 255.0) ** invGamma) * 255 for i in range(0, 256)]).astype("uint8")

def gamma_correction(image):
    return cv2.LUT(image, table)

def histogram_equalization(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.equalizeHist(gray) 

def soundAlert(path, threadStatusQ):
    while True:
        if not threadStatusQ.empty():
            FINISHED = threadStatusQ.get()
            if FINISHED:
                break
        playsound.playsound(path)

def eye_aspect_ratio(eye): #iki nokta arasındaki mesafeyi bulmak için
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)

    return ear
# =============================================================================
# ağız açıklığı mesafe hesaplama
# =============================================================================
def lip_distance(shape):
    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))

    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))

    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)

    distance = abs(top_mean[1] - low_mean[1])
    return distance
# ağızın açıklık mesafesi
YAWN_THRESH = 20
i=0
esneme_sayisi=0
detector2 = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml") 


def checkEyeStatus(landmarks):
    mask = np.zeros(frame.shape[:2], dtype = np.float32)
    
    hullLeftEye = []
    for i in range(0, len(leftEyeIndex)):
        hullLeftEye.append((landmarks[leftEyeIndex[i]][0], landmarks[leftEyeIndex[i]][1]))

    cv2.fillConvexPoly(mask, np.int32(hullLeftEye), 255)

    hullRightEye = []
    for i in range(0, len(rightEyeIndex)):
        hullRightEye.append((landmarks[rightEyeIndex[i]][0], landmarks[rightEyeIndex[i]][1]))


    cv2.fillConvexPoly(mask, np.int32(hullRightEye), 255)

 
    leftEAR = eye_aspect_ratio(hullLeftEye)
    rightEAR = eye_aspect_ratio(hullRightEye)

    ear = (leftEAR + rightEAR) / 2.0


    eyeStatus = 1          # 1 -> Açık, 0 -> Kapalı
    if (ear < thresh):
        eyeStatus = 0

    return eyeStatus  

def checkBlinkStatus(eyeStatus):
    global state, blinkCount, yorgunluk
    if(state >= 0 and state <= falseBlinkLimit):
        if(eyeStatus):
            state = 0

        else:
            state += 1

    elif(state >= falseBlinkLimit and state < drowsyLimit):
        if(eyeStatus):
            blinkCount += 1 
            state = 0

        else:
            state += 1


    else:
        if(eyeStatus):
            state = 0
            yorgunluk = 1
            blinkCount += 1

        else:
            yorgunluk = 1

def getLandmarks(im):
    imSmall = cv2.resize(im, None, 
                            fx = 1.0/FACE_DOWNSAMPLE_RATIO, 
                            fy = 1.0/FACE_DOWNSAMPLE_RATIO, 
                            interpolation = cv2.INTER_LINEAR)

    rects = detector(imSmall, 0)
    if len(rects) == 0:
        return 0

    newRect = dlib.rectangle(int(rects[0].left() * FACE_DOWNSAMPLE_RATIO),
                            int(rects[0].top() * FACE_DOWNSAMPLE_RATIO),
                            int(rects[0].right() * FACE_DOWNSAMPLE_RATIO),
                            int(rects[0].bottom() * FACE_DOWNSAMPLE_RATIO))

    points = []
    [points.append((p.x, p.y)) for p in predictor(im, newRect).parts()]
    return points

capture = cv2.VideoCapture(0)

for i in range(10):
    ret, frame = capture.read()

totalTime = 0.0
validFrames = 0
dummyFrames = 100

print("Kalibrasyon Sürüyor!")
while(validFrames < dummyFrames):
    validFrames += 1
    t = time.time()
    ret, frame = capture.read()
    height, width = frame.shape[:2]
    IMAGE_RESIZE = np.float32(height)/RESIZE_HEIGHT
    frame = cv2.resize(frame, None, 
                        fx = 1/IMAGE_RESIZE, 
                        fy = 1/IMAGE_RESIZE, 
                        interpolation = cv2.INTER_LINEAR)

    
    adjusted = histogram_equalization(frame)

    landmarks = getLandmarks(adjusted)
    timeLandmarks = time.time() - t

    if landmarks == 0:
        validFrames -= 1
        cv2.putText(frame, "Yuz algilanamiyor, Lutfen uygun aydinlatmayi kontrol edin", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "veya azaltin ", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("Yorgunluk Tespiti", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            sys.exit()

    else:
        totalTime += timeLandmarks
        
       

print("KALİBRASYON TAMAMLANDI!")

spf = totalTime/dummyFrames
print("Current SPF (seconds per frame) is {:.2f} ms".format(spf * 1000))

drowsyLimit = yorgunlukzamani/spf
falseBlinkLimit = blinkTime/spf
print("drowsy limit: {}, false blink limit: {}".format(drowsyLimit, falseBlinkLimit))
#video kayıt
if __name__ == "__main__":
    print('main')
    vid_writer = cv2.VideoWriter('video.kaydi.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))
    while True:
        try:
            
            t = time.time()
            ret, frame = capture.read()
            height, width = frame.shape[:2]
            IMAGE_RESIZE = np.float32(height)/RESIZE_HEIGHT
            frame = cv2.resize(frame, None, 
                                fx = 1/IMAGE_RESIZE, 
                                fy = 1/IMAGE_RESIZE, 
                                interpolation = cv2.INTER_LINEAR)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

          
            adjusted = histogram_equalization(frame)

            landmarks = getLandmarks(adjusted)
            if landmarks == 0:
                validFrames -= 1
                cv2.putText(frame, "Yuz Algilanamiyor, lutfen isigi acin ", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, "veya azaltin ", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow("Yorgunluk Tesipiti", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                continue

            eyeStatus = checkEyeStatus(landmarks)
            checkBlinkStatus(eyeStatus)
# =============================================================================
#             Esneme Yeri
# =============================================================================
            rects = detector2.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            for (x, y, w, h) in rects:
                rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
        
                distance = lip_distance(shape)
        
                lip = shape[48:60]
                cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)
                if (distance > YAWN_THRESH):
                    i+=1
                    print(i)
                    if(i%20==0):
                        esneme_sayisi+=1
                    cv2.putText(frame, "   !  ! Esniyorsunuz ! !", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


            for i in range(0, len(leftEyeIndex)):
                cv2.circle(frame, (landmarks[leftEyeIndex[i]][0], landmarks[leftEyeIndex[i]][1]), 1, (0, 0, 255), -1, lineType=cv2.LINE_AA)

            for i in range(0, len(rightEyeIndex)):
                cv2.circle(frame, (landmarks[rightEyeIndex[i]][0], landmarks[rightEyeIndex[i]][1]), 1, (0, 0, 255), -1, lineType=cv2.LINE_AA)

            if yorgunluk:
                cv2.putText(frame, "! ! ! YORGUNLUK ALARMI ! ! !", (70, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                chime.error()
                print("Uyanın")

            else:
                cv2.putText(frame, "Kirpma : {}".format(blinkCount), (460, 80), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,255), 2, cv2.LINE_AA)
                # (0, 400)
                ALARM_ON = False
                


            cv2.imshow("Yorgunluk Tesipiti", frame)
            vid_writer.write(frame)

            k = cv2.waitKey(1) 
            if k == ord('r'):
                state = 0
                yorgunluk = 0
                ALARM_ON = False
                threadStatusQ.put(not ALARM_ON)

            elif k == 27:
                break

          

        except Exception as e:
            print("excep")

    capture.release()
    vid_writer.release()
    cv2.destroyAllWindows()
