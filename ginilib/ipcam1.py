# Using Android IP Webcam video .jpg stream (tested) in Python2 OpenCV3

import urllib
import cv2
import numpy as np
import time
import requests
import threading
from threading import Thread, Event, ThreadError
from ginilib.FaceUtil import faces



# Replace the URL with your own IPwebcam shot.jpg IP:port
#url='http://192.168.1.104:8080/shot.jpg'

class camera():
	def __init__(self,camid,cam_type):
		self.Ctype=cam_type
		self.fc=faces()
		if self.Ctype=="Nonipcam": 
			self.ur=int(camid)
        		self.video = cv2.VideoCapture(self.ur)

		elif self.Ctype=="ipcam":
			self.ur=camid
			self.imgResp= urllib.urlopen(self.ur)
			self.imgResp= requests.get(self.ur,stream=True,verify=True) 

		else:
			camera = PiCamera()
			rawCapture = PiRGBArray(camera)
 			# allow the camera to warmup
			time.sleep(0.1)
		self.thread_cancel=False
		self.thread=Thread(target=self.run)
		self.thread.setDaemon(True)
		self._is_running=True
		print self.Ctype +"_Camera initialized"
	

	def start(self):
		self.thread.start()
		print self.Ctype +"_Camera Started"

	def run(self):
		#print url
		while (self._is_running): 
			try:
				if self.Ctype=="Nonipcam":
        				success, img = self.video.read()

				elif self.Ctype=="ipcam":
					imgResp = urllib.urlopen(self.ur)
        				imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
      					img = cv2.imdecode(imgNp,-1)
	
				else:
					camera.capture(rawCapture, format="bgr")
					img = rawCapture.array

    				# put the image on screen
	        		cv2.waitKey(100)
				img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
				img=self.fc.detect(img)
    				cv2.imshow(self.Ctype,img)


                                #self.out.write(img) 
	        		cv2.waitKey(100)    
    		   		# Quit if q is pressed
    				if cv2.waitKey(1) & 0xFF == ord('q'):
        				break
			except ThreadError:
        			self.thread_cancelled = True

 		print("exiting")
			

	def stop(self):
		cv2.destroyAllWindows()
		self._is_running =False
		#self.thread_cancelled = True
		print self.Ctype +"_Camera  closed"
