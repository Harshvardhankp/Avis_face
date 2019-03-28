import cv2
import urllib
import numpy as np
import time
import requests
import threading
from threading import Thread, Event, ThreadError
import math
#from picamera import PiCamera
#from picamera.array import PiRGBArray
from FaceUtil import faces
import time


#cam_type  value is either "Nonipcam" or "ipcam"  or "picam"
# camid is number if it is webcam and url if it is ip camera  ex 192.168.1.1:8000
class cam(object):
    def __init__(self,camid,cam_type):
	self.Ctype=cam_type
	self.fc=faces()
	if self.Ctype=="Nonipcam": 
		self.cam=int(camid)
        	self.video = cv2.VideoCapture(self.cam)

	elif self.Ctype=="ipcam":
		self.cam=camid

	else:
		camera = PiCamera()
		rawCapture = PiRGBArray(camera)
 		# allow the camera to warmup
		time.sleep(0.1)


    def __del__(self):
        self.video.release()
    

    def get_frame(self):
	if self.Ctype=="Nonipcam":
        	success, img = self.video.read()

	elif self.Ctype=="ipcam":
		imgResp = urllib.urlopen(self.cam)
        	imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
      		img = cv2.imdecode(imgNp,-1)
	
	else:
		camera.capture(rawCapture, format="bgr")
		img = rawCapture.array
	
	img=self.fc.detect(img)

	#cv2.waitKey(100)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg

