import time
import urllib
import cv2
import numpy as np
import time
from ginilib.db import dbops
import sys , os
import pickle
from datetime import time,timedelta,date,datetime
from imutils.video import WebcamVideoStream ,VideoStream,FileVideoStream
from imutils.video import FPS
import imutils
from darkflow.net.build import TFNet
from lib.lp_preproc import lppreproc
import numpy as np
import argparse
import pytesseract
from PIL import Image
from skimage.io import imread
import shutil
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import mysql.connector
from mysql.connector import Error,MySQLConnection
from ginilib.db import dbops 
from lib.alertimg import Alert
from lib.genrep import report


dbs=dbops()
alt=Alert()
r=report()
counter=0 

class Atmlib():
	def __init__(self):
		option = {'model': './cfg/yolo-voc.2.0.cfg','load': './cfg/yolo-voc_final.weights','threshold': 0.15,'gpu': 1.0}
		self.tfnet = TFNet(option)	
		self.colors = [tuple(255 * np.random.rand(3)) for i in range(7)]

	def Atm(self,frame):
		results = self.tfnet.return_predict(frame)
		mask=False
		tampered=False
		fire=False
		weapon=False
		helmet=False 
        	for color, result in zip(self.colors, results):
            		tl = (result['topleft']['x'], result['topleft']['y'])
            		br = (result['bottomright']['x'], result['bottomright']['y'])
            		label = result['label']
			if label == "ATMNormal":
                        	color = (0, 255, 0)
                        elif label == "ATMTampered":
                        	color = (0, 0, 255)
				tampered=True
                        elif label == "FIRE":
                            	color = (255, 0, 0)
				fire=True
                        elif label == "Helmets":
                            	color = (255, 255, 0)
				helmet=True
                        elif label == "MASK":
                            	color = (255, 165, 0)
				mask=True
                        elif label == "WEAPON":
                            	color = (0, 0, 128)
				weapon=True                        			
                        else:
                            	color = (0, 0, 0)

            	        x=tl[0]
            		y=tl[1]
            		x1=br[0]
            		y1=br[1]  
	    		frame = cv2.rectangle(frame, tl, br, color, 2)
            		frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),2)
		if tampered==True or fire==True or mask==True or weapon==True  :
			Alert_text=label		
			dbs.Add_Alerts("ATM1234",tampered,weapon,helmet,fire,mask)
			fn="./evidences/"+str(counter)+".jpg"
			cv2.imwrite(fn,frame)
			r.generate_report(Alert_text,"121A2","BANGLORE","23/01/2019",fn)								
		frame=cv2.resize(frame,(800,600))
		width=800
		font=cv2.FONT_HERSHEY_SIMPLEX
		frame=cv2.putText(frame, "TENSOR LABS - BANGALORE", (int(width /3.5), 60),font, 0.9, (0, 255, 255),thickness=2)
		frame=alt.image_gen(frame,mask,tampered,fire,weapon,helmet)
		return frame





	
