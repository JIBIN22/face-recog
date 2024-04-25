import cv2
import cvzone
import os
import pickle
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

import warnings
def main_prog():
    warnings.filterwarnings("ignore", category=DeprecationWarning) 

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred,{
        'databaseURL':"https://face-48233-default-rtdb.firebaseio.com/",
        'storageBucket' : "face-48233.appspot.com"
    })

    bucket = storage.bucket()

    #cap = cv2.VideoCapture('http://192.168.29.201:4747/video')
    cap = cv2.VideoCapture(0)

    cap.set(3, 640)
    cap.set(4, 480)

    imgBackground=cv2.imread('Resources/background.png')
    folderModePath ='Resources/Modes'
    modePathList=os.listdir(folderModePath)
    imgModeList=[]
    for path in modePathList:
        imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))


    file=open('EncodeFile.p','rb')
    encodeListKnownWithIds=pickle.load(file)
    file.close()
    encodeListKnown,studentIds=encodeListKnownWithIds
    #print(studentIds)

    modeType=0
    counter=0
    id=-1
    imgStudent=[]
    while True:
        success,img=cap.read()
        imgS=cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame=face_recognition.face_locations(imgS)
        encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)

        imgBackground[162:162+480 ,55:55+640]=img
        imgBackground[44:44+633 ,808:808+414]=imgModeList[modeType]

        
        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                #print("matches", matches)
                #print("faceDis", faceDis)
                matchIndex = np.argmin(faceDis)
                #print("Match index", matchIndex)
                if matches[matchIndex]:
                        # print("Know pic")
                        #print (studentIds[matchIndex])
                        y1, x2, y2, x1 = faceLoc
                        
                        y1, x2, y2, x1 =  y1*4, x2*4, y2*4, x1*4
                        bbox = 55+x1, 162+y1, x2-x1, y2 - y1
                        imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                        
                        id = studentIds[matchIndex]
                        if counter == 0:
                            cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                            #cv2.imshow('face attendance', imgBackground)
                            #cv2.waitKey(1)
                            counter = 1
                            modeType = 1
                if counter!=0:
                    if counter==1:
                        studentInfo=db.reference(f'Students/{id}').get()
                        #print(studentInfo)
                        
                        blob = bucket.get_blob(f'old/{id}.png')
                        array= np.frombuffer(blob.download_as_string(),np.uint8)
                        imgStudent= cv2.imdecode(array , cv2.COLOR_BGRA2BGR)

                        datetimeobj=datetime.strptime(studentInfo['last_attendance_time'],"%Y-%m-%d %H:%M:%S")
                        sec=(datetime.now() - datetimeobj).total_seconds()
                        #print(sec)

                        if sec > 30:               
                            ref=db.reference(f'Students/{id}')
                            studentInfo['total_attendance']=int(studentInfo['total_attendance'])+1
                            ref.child('total_attendance').set(studentInfo['total_attendance'])
                            ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        
                        else:
                            modeType=4
                            counter=0
                            imgBackground[44:44+633 ,808:808+414]=imgModeList[modeType]




                    #if modeType!=3:
                    if 10<counter<20:
                        modeType=2

                    imgBackground[44:44+633 ,808:808+414]=imgModeList[modeType]
                    if counter<=10:
                        cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)      
                        cv2.putText(imgBackground,str(studentInfo['branch']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                        cv2.putText(imgBackground,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                        cv2.putText(imgBackground,str(studentInfo['status']),(900,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                        cv2.putText(imgBackground,str(studentInfo['year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                        cv2.putText(imgBackground,str(studentInfo['starting_year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                            
                        (w,h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX , 1 , 1)
                        offset =(414-w)//2
                        cv2.putText(imgBackground,str(studentInfo['name']),(808+offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)

                        if imgStudent.shape[:2] != (240, 240):
                            imgStudent = cv2.resize(imgStudent, (240, 240))
                        #print(imgStudent.shape[:2])
                        imgBackground[163:163+240, 895:895+240] = imgStudent#top-down  , left-right


                        
                        counter+=1
                        if(counter>=30):
                            counter=0
                            modeType=0
                            studentInfo=[]
                            imgStudent=[]
                            imgBackground[44:44+633 ,808:808+414]=imgModeList[modeType]
                    
                    
                    
        else:
            counter=0
            modeType=0                  
                        

        #cv2.imshow("fac",img)
        cv2.imshow("Face Attendence",imgBackground)
        key=cv2.waitKey(1)
        if key == ord('q'):
            break     
        
        

    cv2.destroyAllWindows()

main_prog()