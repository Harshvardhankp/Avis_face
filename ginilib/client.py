import cv2
import numpy as np
import os
from cv2 import face
from PIL import Image
#from ginilib.Search import ColorDescriptor
#from ginilib import faceutil
#import imutils
#import dlib
#import urllib2
import sqlite3
from ginilib.users import users

class client:
	def __init__(self):
		self.face_cascade = cv2.CascadeClassifier('./models/haarcascades/haarcascade_frontalface_default.xml')
		self.font= cv2.FONT_HERSHEY_SIMPLEX
		self.user=users()
 
	def enroll_user(self):
		cap = cv2.VideoCapture(0)
		samplenum=0
		ids=None
		faces=[]
		Face=[]
		while(True):
		# Capture frame-by-frame
			ret,img=cap.read()
			cv2.imshow("Face", img)

		# Our operations on the frame come here
			gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			# Show faces
			faces=self.face_cascade.detectMultiScale(img,1.3,5,minSize=(30,30))
			id=-1
			for(x,y,w,h) in faces:
				x = x+ (0.10*w)
				w = 0.8* w
				h = 0.95*h
				x= int(x)
				w=int(w)
				h=int(h)
				samplenum = samplenum +1
				image = gray[y:y+h,x:x+w]
				dst = np.zeros(shape=(5,2))
				norm_image = cv2.normalize(image,dst,0,255,cv2.NORM_MINMAX)
				norm_image=image
				Face.append(norm_image)
				cv2.putText(img,"Learning Face....",(x+20,y),self.font,0.8,(0,0,255))
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				cv2.waitKey(100)
				cv2.imshow("Face",img)			

			cv2.waitKey(1)
			if(samplenum == 30):
				break
		
		self.user.enroll_user(Face,"kaka","btmresidency",9900410923,"Home",123456789)
		

		cap.release()
		cv2.destroyAllWindows() 
		return

	
