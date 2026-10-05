import cv2

cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_faces(frame):

    gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY    )

    faces = cascade.detectMultiScale(gray,  scaleFactor=1.2,  minNeighbors=5,  minSize=(80,80)    )

    if len(faces) == 0:
        return "No Face", []

    elif len(faces) == 1:
        return "One Face", faces.tolist()

    else:
        return "Multiple Faces", faces.tolist()