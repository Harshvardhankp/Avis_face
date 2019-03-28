import cv2
import time
import numpy as np
import argparse
import os
from PIL import Image
from skimage.io import imread
import shutil
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import threading
import time
import urllib
import threading
from threading import Thread, Event, ThreadError
from ginilib.db import dbops
import face_recognition
import sys , os
import pickle
from datetime import time,timedelta,date,datetime
from imutils.video import WebcamVideoStream ,VideoStream,FileVideoStream
from imutils.video import FPS
#import pyttsx
import imutils
import mysql.connector
from mysql.connector import Error,MySQLConnection
from ginilib.db import dbops 
import mysql.connector 
from Functions.Face import facelib
from datetime import datetime


flib=facelib()
dbs=dbops()
counter=0
i=0
count=0
fourcc = cv2.VideoWriter_fourcc("M", "J", "P", "G")



while (True):
    if len(os.listdir('./Input')) == 0:
        print("Directory is empty")
	#time.sleep(72000)#for 30min in seconds
		#time.sleep(1)
    else:
		print("Directory is not empty")
		files=os.listdir("./Input")
		print len(files)
		for filename in files :
			capture=None
			print(filename)
           		capture = cv2.VideoCapture('./Input/'+filename)
			fileout="./output_video/"+filename   
			out = cv2.VideoWriter(fileout,fourcc, 26.0, (320, 240)) 
			colors = [tuple(255 * np.random.rand(3)) for i in range(7)]
			while (capture.isOpened()):
    				#stime = time.time()
    				ret, frame = capture.read()
    				#cv2.line(frame,(850,750),(1800,850),(0,0,255),5)
    				if ret:
  					frame = flib.facerec(frame)   # Do the face prediction
  					frame=flib.Track_user(frame)
					out.write(frame)
					root="./videos_proc/live"
					saveto =root +"/live"+ str(count) + ".jpg"
					if count >= 3:
						count = 0
					else:
						count += 1
					#create directory if not exist
					
					cv2.imwrite(saveto, frame)
					print(saveto)
					#dbs.Add_Alerts("false","false","flase","false")	
 
					frame=cv2.resize(frame,(800,600))
					#cv2.imshow('frame', frame)
        				#print('FPS {:.1f}'.format(1 / (time.time() - stime)))
        				if cv2.waitKey(1) & 0xFF == ord('q'):
            					break
    				else:
        				capture.release()
        				cv2.destroyAllWindows()
        				break
			out.release()
			shutil.move("./Input/"+str(filename), "./processed/" + str(filename))	
cv2.destroyAllWindows()
