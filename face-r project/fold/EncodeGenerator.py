import cv2
import face_recognition
import pickle
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://face-48233-default-rtdb.firebaseio.com/",
    'storageBucket' : "face-48233.appspot.com"
})


def encoding():
    folderPath = 'old'
    pathList = os.listdir(folderPath)
    print(pathList)
    imgList = []
    StudentId = []
    for path in pathList:
        imgList.append(cv2.imread(os.path.join(folderPath,path)))
        # print(path)
        # print(os.path.splitext(path)[0])
        
        StudentId.append(os.path.splitext(path)[0])
        """
    # adding image ke storage database
        fileName = f'{folderPath}/{path}'
        bucket = storage.bucket()
        blob = bucket.blob(fileName)
        blob.upload_from_filename(fileName)
"""
    print(StudentId)
    def findEncodings(imagesList):
        c=0
        encodeList = []
        for img in imagesList:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            try:
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
                print("face found in the image.",c)
                c+=1
            except IndexError:
                print("No face found in the image.",c)
                c+=1
        return encodeList

    print("Encoding started")
    encodeListKnown = findEncodings(imgList)
    encodeListKnownWithIds = [encodeListKnown, StudentId]
    #print(encodeListKnown)
    print(("Encoding closed"))

    file = open("EncodeFile.p", "wb")
    pickle.dump(encodeListKnownWithIds, file)
    file.close()
    print("File close")


#encoding()