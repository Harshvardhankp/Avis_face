import cv2
import numpy as np
import os
from cv2 import face
from PIL import Image
#from ginilib.Search import ColorDescriptor
#from ginilib import FaceUtil
from ginilib.db import dbops
#import imutils
import sqlite3
import os.path



class users:

	def __init__(self):
		self.face_cascade = cv2.CascadeClassifier('./models/haarcascades/haarcascade_frontalface_default.xml')
		self.recognizer=cv2.face.createLBPHFaceRecognizer()
		self.recognizer_local=cv2.face.createLBPHFaceRecognizer()
		self.firsttime=True
		if os.path.isfile("./models/gini/trainingData.yml"): 
			self.recognizer.load("./models/gini/trainingData.yml")
			self.firsttime=False
		
		self.font= cv2.FONT_HERSHEY_SIMPLEX
		self.dbaction=dbops()      

	
	def enroll_user(self,faces,Username,address,mobile,Type,Nationalid):
		ids=[]
		id=-1
		knownface=False;
		self.recognizer.setThreshold(100)
		samplenum=0
		for face in faces:
			ids.append(Nationalid)
			cv2.imwrite("img/users/" + str(Nationalid) + "." + str(samplenum) + ".jpg" , face)
			samplenum+=1
			id,conf=self.recognizer.predict(face)
			cv2.imshow("Recorded faces",face)
			cv2.waitKey(100)
			if id > 0:
				knownface=True
		

		if self.recognizer()=None:
			self.dbaction.Add_user (Username,address,mobile,Type,Nationalid)
			self.train()
		else:

			if knownface==False :
				print (id)
				self.dbaction.Add_user (Username,address,mobile,Type,Nationalid)
				self.train()
		
			else:
				print ("known face")
				print (id)
				

	def train(self):
		path="img/users/"
		imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
		faces=[]
		ids=[]
		for imagePath in imagePaths:
			faceImg=Image.open(imagePath).convert('L');
			faceNP=np.array(faceImg,"uint8")
			id= int(os.path.split(imagePath)[-1].split('.')[0])
			print (id)
			faces.append(faceNP)
			ids.append(id)
			cv2.imshow("Training", faceNP)
			cv2.waitKey(20)
		if self.recognizer==None :
			self.recognizer.train(faces,np.array(ids))
		else:
			self.recognizer.update(faces,np.array(ids))
		
		self.recognizer.write("models/gini/trainingData.yml")
		self.recognizer.write("models/gini/trainingData.yml")
		self.recognizer.read("./models/gini/trainingData.yml")
		self.recognizer_local.train(faces,np.array(ids))
		self.recognizer_local.save(modelname)
		cv2.destroyAllWindows	
		return

