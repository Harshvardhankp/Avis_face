import urllib
import cv2
import numpy as np
import time
import threading
from threading import Thread, Event, ThreadError
import os
#from cv2 import face
#from PIL import Image
from ginilib.db import dbops
from datetime import date


# Replace the URL with your own IPwebcam shot.jpg IP:port
#url='http://192.168.1.104:8080/shot.jpg'

class camera(threading.Thread):
	def __init__(self,ids,threadid):#CAmera ID to be provided
		threading.Thread.__init__(self)
		self.threadID = threadid
		self.face_cascade = cv2.CascadeClassifier('./models/haarcascades/haarcascade_frontalface_default.xml')
		#self.recognizer=cv2.face.LBPHFaceRecognizer_create()
		#self.recognizer.read("./models/gini/trainingData.yml")
		self.font= cv2.FONT_HERSHEY_SIMPLEX
		dbs=dbops()
		#Getting camera details
		camdetails= dbs.get_Camera_details(ids)
		self.camname=camdetails[0].upper()
		camid=camdetails[1]
		print(camid)
		self.camlocation=camdetails[2].upper()
		cam_type=camdetails[3]
		print(cam_type)
		self.Camtype=cam_type

	
		if self.Camtype=="nonipcam": 
			self.ur=int(camid)
			self.video = cv2.VideoCapture(self.ur)

		elif self.Camtype=="ipcam":
			self.ur=camid
			self.imgResp= urllib.urlopen(self.ur)
			#self.imgResp= requests.get(self.ur,stream=True,verify=True) 

		else:
			#camera = PiCamera()
			#rawCapture = PiRGBArray(camera)
 			# allow the camera to warmup
			time.sleep(0.1)

		self.thread_cancel=False
		#self.thread=Thread(target=self.run)
		self.thread.setDaemon(True)
		self._is_running=True
		print (self.Camtype +"_camera initialized")
	

	def start(self):
		self.thread.start()
		print (self.Camtype +"_Camera Started")

	def run(self):
		#print url
		
		while (self._is_running): 
			try:
				if self.Camtype=="nonipcam":
					success, img = self.video.read()

				elif self.Camtype=="ipcam":
					imgResp = urllib.urlopen(self.ur)
					imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
					img = cv2.imdecode(imgNp,-1)
	
				else:
					#camera.capture(rawCapture, format="bgr")
					#img = rawCapture.array
					time.sleep(0.1)

				# put the image on screen
				cv2.waitKey(100)
				gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
				cv2.putText(img,"TENSOR LABS BANGALORE",(100,40),self.font,0.8,(100,255,0))
				
				datefield ="Date:" + str(date.today())
				cv2.putText(img,datefield,(500,40),self.font,0.4,(255,255,255))
				cv2.putText(img,self.camname +":"+self.camlocation,(500,60),self.font,0.35,(0,255,255))
				
				# Show faces
				faces=self.face_cascade.detectMultiScale(gray,1.3,5,minSize=(30,30))
				for(x,y,w,h) in faces:
					x = x+ (0.1*w)
					w = 0.8* w
					w1=w/2	
					h = 0.95*h
					x= int(x)
					w=int(w)
					h=int(h)

					cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
					dst = np.zeros(shape=(5,2))
					norm_image1 = cv2.normalize(gray[y:y+h,x:x+w],dst,0,255,cv2.NORM_MINMAX)
					#id,conf=self.recognizer.predict(norm_image1)
					id=-1
					print (id)
					if id==-1 :
						cv2.putText(img,"unknown",(x+w,y),self.font,0.4,255)	
					else:
						content=self.dbs.get_user_details(str(id))
						txt=content[0].upper() + "(" +content[2].upper()+")"
						cv2.putText(img,txt,(x+w+10,y),self.font,0.4,(0,0,255))
						cv2.putText(img,str(content[1]),(x+w+10,y+20),self.font,0.4,(0,0,255))
						

				
					cv2.waitKey(100)
					cv2.imshow("Face",img)
					id=0
				key=cv2.waitKey(1) & 0xFF
				if key == ord("q"):
					break

			except ThreadError:
					print(ThreadError)
					self.thread_cancelled = True

		print("exiting")
			

	def stop(self):
		cv2.destroyAllWindows()
		self._is_running =False
		self.thread_cancelled = True
		print (self.Camtype +"_camera  closed")
