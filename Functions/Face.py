import time
import urllib
import cv2
import numpy as np
import time
from ginilib.db import dbops
import face_recognition
import sys , os
import pickle
from datetime import time,timedelta,date,datetime
from imutils.video import WebcamVideoStream ,VideoStream,FileVideoStream
from imutils.video import FPS
#import pyttsx
import imutils

class facelib():
	def __init__(self):
		self.face_cascade = cv2.CascadeClassifier('./models/haarcascades/haarcascade_frontalface_default.xml')
		self.font= cv2.FONT_HERSHEY_SIMPLEX
		self.fileDir = os.path.dirname(os.path.realpath(__file__))
		print ("directory path",self.fileDir)
		#self.unknownusers_dir = os.path.join(self.fileDir, "img/unknownusers")
		self.classifierModel = os.path.join('./models/classifier.pkl')
		if os.path.exists(self.classifierModel):
			with open(self.classifierModel, 'rb') as f:
				if sys.version_info[0] < 3:
					(self.le, self.clf) = pickle.load(f)
				else:
					(self.le, self.clf) = pickle.load(f, encoding='latin1')




	def facerec(self,img):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# Show faces
		faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(5 , 5))
		for (x, y, w, h) in faces:
			#id = -1
			cv2.rectangle(img, (x, y), (x + w + 10, y + h + 10), (0, 255, 255),thickness=3)
			norm_image2 = img[y:y + h, x:x + w]
			norm_image2 = cv2.resize(norm_image2, (96, 96))
			rgb = norm_image2[:, :, ::-1]
			facelocations = face_recognition.face_locations(rgb, model="cnn")
			#print(facelocations)
			if facelocations:
				faceencodes = face_recognition.face_encodings(rgb, facelocations)
				predictions = self.clf.predict_proba(faceencodes).ravel()
				maxI = np.argmax(predictions)
				maxvalue=np.max(predictions)
				print(predictions)
				print(maxvalue)
				print(maxI)
				id = self.le.inverse_transform(maxI)
				confidence = predictions[maxI]
				if confidence < 0.95 :
					id = -1
				if maxvalue <= 0.95:
					id = -1
			else:
				id = -1
				confidence = 0
			print(id)

			if id >= 1:
				content = dbs.get_user_details(str(id))
				if content:
					cv2.putText(img, "ID:"+str(id), (x , y - 30), self.font, 0.4, (0, 0, 255),)
					txt = content[0].upper()
					cv2.putText(img, txt, (x, y-10), self.font, 0.4, (0, 0, 255))
					dbs.Add_log(id)

					if id in 19215626:
						message = [ 'Honourable Minister', 'Mr. Ravishankar Prasad ']
						
					else:
						msg="Hello" + content[0].upper()
						
				id=-1
			else:
				cv2.putText(img, "UNKNOWN", (x, y-10), self.font, 0.4, (0,0,255))
				face = img[y:y + h + 10, x:x + w + 10]
				face = cv2.resize(face, (138, 138))
				
			id = 0
		return img
	
	def Track_user(self,img):
		dbs=dbops()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# Show faces
		faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
		for (x, y, w, h) in faces:
			#id = -1
			img=cv2.rectangle(img, (x, y), (x + w + 10, y + h + 10), (0, 255, 255),thickness=3)
			norm_image2 = img[y:y + h, x:x + w]
			norm_image2 = cv2.resize(norm_image2, (96, 96))
			rgb = norm_image2[:, :, ::-1]
			facelocations = face_recognition.face_locations(rgb, model="cnn")
			print(facelocations)

			if facelocations:
				faceencodes = face_recognition.face_encodings(rgb, facelocations)
				predictions = self.clf.predict_proba(faceencodes).ravel()
				maxI = np.argmax(predictions)
				maxvalue=np.max(predictions)
				print(predictions)
				print(maxvalue)
				print("maxI values are here",maxI)
				uid = self.le.inverse_transform(maxI)
				confidence = predictions[maxI]
				if confidence < 0.95 :
					uid = -1
				if maxvalue <= 0.95:
					uid = -1
			else:
				uid = -1
				confidence = 0
			print("uid is here",uid)
			#getting track id's from get_Transactions_id db	
                        ids=dbs.get_Transactions_id()
			print(ids)
                        for r in ids:
				print(r)
           	        	if uid==r[0]:
				    print("cam name",self.camname)	
  				    dbs.update_Transactions(uid,'Found','call',self.camname)
			
		return img
	def createdir(self,path):
		if not os.path.exists(path):
			try:
				os.makedirs(path)
			except:
				print ("unable to create directory", path)

