import cv2,os
import numpy as np
from PIL import Image
import pickle
import sqlite3

rec=cv2.createLBPHFaceRecognizer();
rec.load("Main/recognizer/trainningData.yml")
faceDetect=cv2.CascadeClassifier("Main/haarcascade_frontalface_default.xml");
path = 'Main/DataSet'

def getProfile(id):
    conn = sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

    
cam = cv2.VideoCapture(0);
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
while True:
    ret, img =cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        id, conf=rec.predict(gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.cv.PutText(cv2.cv.fromarray(img),str(id),(x,y+h),font,255);
        profile=getProfile(id)
        if(profile!=None):
            cv2.cv.PutText(cv2.cv.fromarray(img),"Name:"+str(profile[1]), (x,y+h+30), font, 255)
            cv2.cv.PutText(cv2.cv.fromarray(img),"Age:"+str(profile[2]), (x,y+h+60), font, 255)
            cv2.cv.PutText(cv2.cv.fromarray(img),"Gender"+str(profile[3]), (x,y+h+90), font, 255)
            cv2.cv.PutText(cv2.cv.fromarray(img),"Criminal"+str(profile[4]), (x,y+h+120), font, 255)
    cv2.imshow("Face",img)
    cv2.waitKey(10)
    

