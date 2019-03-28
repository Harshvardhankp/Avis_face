import cv2
import numpy as np
import os
#from cv2 import face
from PIL import Image
#from ginilib.Search import ColorDescriptor
#from ginilib import FaceUtil
from ginilib.db import dbops
#import imutils
import sqlite3
import os.path
#from ginilib.preprocessing import DA



class users:

	def __init__(self):
		self.face_cascade = cv2.CascadeClassifier('./models/haarcascades/haarcascade_frontalface_default.xml')
		self.firsttime=True
		if os.path.isfile("./models/gini/trainingData.yml"): 
			#self.recognizer.load("./models/gini/trainingData.yml")
			self.firsttime=False
		#self.recognizer.setThreshold(100)
		self.font= cv2.FONT_HERSHEY_SIMPLEX
		self.dbaction=dbops()      

	
	def enroll_user(self,faces,Username,address,mobile,Type,Nationalid):
		ids=[]
		id=-1
		knownface=False;		
		samplenum=0
		for face in faces:
			ids.append(Nationalid)
			samplenum+=1
			if self.firsttime==False:
				id,conf=self.recognizer.predict(face)
			
			if id > 0:
				knownface=True
			else:
				cv2.imwrite("img/users/" + str(Nationalid) + "." + str(samplenum) + ".jpg" , face)
			cv2.imshow("Recorded faces",face)
			cv2.waitKey(100)		

		if self.recognizer==None:
			self.train()
			self.dbaction.Add_user (Username,address,mobile,Type,Nationalid)
		else:

			if id==-1 :
				print (id)
				self.train()
				self.dbaction.Add_user (Username,address,mobile,Type,Nationalid)
		
			else:
				print ("known face")
				print (id)
				

	def train(self):
		#dataproc=DA()
		path="img/users/"
		dest="img/processed/"
		imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
		faces=[]
		ids=[]
		counter=0
		for imagePath in imagePaths:
			faceImg=Image.open(imagePath).convert('L');
			#faceprocessed= dataproc.CropFace(faceImg, eye_left=(252,364), eye_right=(420,366), offset_pct=(0.1,0.1), dest_sz=(200,200))
			faceNP=np.array(faceImg,"uint8")
			id= int(os.path.split(imagePath)[-1].split('.')[0])
			print (id)
			#faceprocessed.save(dest+str(id)+"."+str(counter)+".jpg") #NOt working
			counter+=1
			faces.append(faceNP)
			ids.append(id)
			cv2.imshow("Training", faceNP)
			cv2.waitKey(20)
		if self.recognizer==None :
			self.recognizer.train(faces,np.array(ids))
		else:
			self.recognizer.update(faces,np.array(ids))
		
		self.recognizer.save("models/gini/trainingData.yml")
		self.recognizer.load("./models/gini/trainingData.yml")
		self.recognizer_local.train(faces,np.array(ids))
		modelname="models/gini/" + str(id)+".yml"
		self.recognizer_local.save(modelname)
		cv2.destroyAllWindows	
		return

