#!/usr/bin/python
import threading
import time
import urllib
import cv2
import numpy as np
import time
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

class camera (threading.Thread):
	def __init__(self, camid,camname,camlocation,cam_type,threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

		# Getting camera details
		self.camname = camname
		self.camid = camid
		self.camlocation = camlocation
		cam_type = cam_type

		self.face_cascade = cv2.CascadeClassifier('./models/haarcascades/haarcascade_frontalface_default.xml')
		self.font= cv2.FONT_HERSHEY_SIMPLEX
		self.fileDir = os.path.dirname(os.path.realpath(__file__))
		self.unknownusers_dir = os.path.join(self.fileDir, "img/unknownusers")
		self.classifierModel = os.path.join(self.fileDir, 'ginilib/openface/generated-embeddings/classifier.pkl')
		if os.path.exists(self.classifierModel):
			with open(self.classifierModel, 'rb') as f:
				if sys.version_info[0] < 3:
					(self.le, self.clf) = pickle.load(f)
				else:
					(self.le, self.clf) = pickle.load(f, encoding='latin1')
		dbs=dbops()
		# create a directory for camera
		settingdetails = dbs.get_settingsdetails()
		rootpathprimary = settingdetails[0][2]
		rootpathsecondary = settingdetails[0][3]
		rootpathtertiary = settingdetails[0][4]
		if os.path.exists(rootpathprimary):
			pvideoroot = rootpathprimary
		else:
			self.createdir(rootpathprimary)
			pvideoroot = rootpathprimary

		if os.path.exists(rootpathsecondary):
			svideoroot = rootpathsecondary
		else:
			self.createdir(rootpathsecondary)
			svideoroot = rootpathsecondary

		if os.path.exists(rootpathtertiary):
			tvideoroot = rootpathtertiary
		else:
			self.createdir(rootpathtertiary)
			tvideoroot = rootpathtertiary

		camdir = pvideoroot+"/videos/" + camname
		self.base = pvideoroot+"/videos/"
		self.root = self.base + camname + "/live"
		self.root_hist = self.base + camname + "/hist"
		self.createdir(camdir)
		self.createdir(self.base)
		self.createdir(self.root)
		self.createdir(self.root_hist)

		framerate = 18.0
		self.fps = FPS().start()

		self.Camtype=cam_type
		if self.Camtype=="webcam":
			try:
					ur =int(self.camid)
					self.video = WebcamVideoStream(src=ur).start()
			except Exception as e:
				print(e)
				print("Unable to open",camname)
		elif self.Camtype == "rtsp":
			try:
					ur = self.camid
					self.video = VideoStream(ur).start()
			except Exception as e:
				# print(e)
				print("Unable to open", camname)
		elif self.Camtype=="http":
			try:
				self.ur = camid
				self.imgResp = urllib.request(self.ur)
				# self.imgResp= requests.get(self.ur,stream=True,verify=True)

			except Exception as e:
				#print(e)
				print("Unable to open",camname)
		elif self.Camtype=="pi":
			try:
				# camera = PiCamera()
				# rawCapture = PiRGBArray(camera)
				# allow the camera to warmup
				time.sleep(0.1)
			except Exception as e:
				#print(e)
				print("Unable to open",camname)




	def run(self):
		print ("Starting " + self.name)
		#threadLock.acquire()
		dbs=dbops()
		counter = 0
		self.trids, self.trname, self.trencodes = dbs.get_Track_user_list()
		self.yr = str(date.today().strftime("%Y"))
		self.mn = str(date.today().strftime("%m"))
		self.dy = str(date.today().strftime("%d"))
		self.FYear = self.root_hist + "/" + self.yr
		self.monpath = self.FYear + "/" + self.mn
		self.dypath = self.monpath + "/" + self.dy
		self.createdir(self.FYear)
		self.createdir(self.monpath)
		self.createdir(self.dypath)
		self.start = datetime.now().strftime("%Y%m%d%H%M%S")
		self.delta = timedelta(minutes=10)  # - configuration part
		self.end = datetime.strptime(self.start, "%Y%m%d%H%M%S") + self.delta
		self.filename = self.dypath + "/" + self.start + ".avi"
		# Define the codec and create VideoWriter object
		self.fourcc = cv2.VideoWriter_fourcc("M", "J", "P", "G")
		self.out = cv2.VideoWriter(self.filename, self.fourcc, 26.0, (320, 240))  #0x00000021

		while (True):
			img=None
			try:
				if self.Camtype=="webcam":
					try:
						img = self.video.read()
					except:
						print("Unable to read " + str(self.camname))

				elif self.Camtype == "rtsp":
					try:
						img = self.video.read()
					except:
						print("Unable to read " + str(self.camname))

				elif self.Camtype=="http":
					try:
						imgResp = urllib.urlopen(self.ur)
						imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
						img = cv2.imdecode(imgNp,-1)
					except:
						print("Unable to read "+ str(self.camname))
	
				elif self.Camtype=="pi":
					#camera.capture(rawCapture, format="bgr")
					#img = rawCapture.array
					time.sleep(0.1)

				# put the image on screen
				cv2.waitKey(100)
				if np.all(img == None):
					print("Image value is empty for : " + self.camname)
				else:
					#img = self.facerec(img)   # Do the face prediction
  					img=self.Track_user(img)
					self.fps.update()
					width = 800
					height = 600
					img = cv2.resize(img, (width, height))
					gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					cv2.putText(img, "TENSOR LABS - BANGALORE", (int(width / 3.5), 60), self.font, 0.8, (0, 255, 255),thickness=2)
					datefield = "Date :" + str(date.today().strftime("%d-%m-%Y"))
					cv2.putText(img, datefield, (width - 180, height-40), self.font, 0.5, (255, 255, 255),thickness=2)
					cv2.putText(img, self.camname , ((width - 120), 60), self.font, 0.8,(0, 0, 255),thickness=2)
					# self.out.write(img)
					# cv2.imshow(camname, img)
					#Save Live Image
					saveto = self.root +"/live"+ str(counter) + ".jpg"
					if counter >= 3:
						counter = 0
					else:
						counter += 1
					#create directory if not exist
					cv2.imwrite(saveto, img)
					print(saveto)

					# Save backup

					frame = cv2.resize(img, (320, 240))
					tod=datetime.now().strftime("%Y%m%d%H%M%S")
					tod=datetime.strptime(tod, "%Y%m%d%H%M%S")
					if tod  >= self.end:
						# Reset the directory path
						self.yr = str(date.today().strftime("%Y"))
						self.mn = str(date.today().strftime("%m"))
						self.dy = str(date.today().strftime("%d"))
						self.FYear = self.root_hist + "/" + self.yr
						self.monpath = self.FYear + "/" + self.mn
						self.dypath = self.monpath + "/" + self.dy
						self.createdir(self.FYear)
						self.createdir(self.monpath)
						self.createdir(self.dypath)
						self.start =  datetime.now().strftime("%Y%m%d%H%M%S")
						self.end = datetime.strptime(self.start, "%Y%m%d%H%M%S") + self.delta
						self.filename = self.dypath + "/" +self.start + ".avi"
						print ("creating file")
						print(self.filename)
						self.out.write(frame)
						self.out.release()
						self.out = cv2.VideoWriter(self.filename, self.fourcc, 26.0, (320, 240))  #0x00000021

					else:
						self.out.write(frame)



					#Save Backup ends here
				key = cv2.waitKey(1) & 0xFF
				if key == ord("q"):
					break
				self.fps.stop()

			except ThreadError:
					print(ThreadError)
					self.thread_cancelled = True

		print("exiting")

	def facerec(self,img):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# Show faces
		faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
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
					txt = content[0].upper() #+ "(" + content[2].upper() + ")"
					cv2.putText(img, txt, (x, y-10), self.font, 0.4, (0, 0, 255))
					#cv2.putText(img, str(content[1]), (x + w + 10, y + 20), self.font, 0.4, (0, 0, 255))
					dbs.Add_log(id)

					if id in 19215626:
						message = [ 'Honourable Minister', 'Mr. Ravishankar Prasad ']
						#for msg in message:
						#	self.wish(msg)
					else:
						msg="Hello" + content[0].upper()
						#self.wish(msg)
				id=-1
			else:
				cv2.putText(img, "UNKNOWN", (x, y-10), self.font, 0.4, (0,0,255))
				#cv2.putText(img, "Recording", (x + w + 12, y - 10), self.font, 0.4, 255)
				#userid = "U" + str(datetime.now().strftime("%d%H%M%S")) + ".jpg"
				#saveunknownto = os.path.join(self.unknownusers_dir, userid)
				face = img[y:y + h + 10, x:x + w + 10]
				face = cv2.resize(face, (138, 138))
				#cv2.imwrite(saveunknownto, face)
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



'''
	def wish(self,message):
		engine = pyttsx.init()
		rate = engine.getProperty('rate')
		print(rate)
		engine.setProperty('rate', rate-30)
		engine.setProperty('voice', 'english+f4')
		engine.say(message)
		engine.runAndWait()

'''


if __name__ == '__main__':
	threads = []
	dbs=dbops()
	# Getting camera details
	# Create new threads

	cameras = dbs.get_Camera_list()
	for c in cameras:
		camname = c[1].upper()
		camid = c[2]
		camlocation = c[3].upper()
		cam_type = c[4]
		thread1 = camera(camid,camname,camlocation,cam_type,2,"Thread-1", 1)
		thread1.start()
			# Add threads to thread list
		threads.append(thread1)

	# Wait for all threads to complete
	for t in threads:
		t.join()
		print ("Exiting Main Thread")
