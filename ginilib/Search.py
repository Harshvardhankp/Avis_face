#from ginilib import faceutil
import cv2
import numpy as np
import os
from PIL import Image
import csv
import math
import imutils
#import dlib
#import urllib2


class ColorDescriptor:
	def __init__(self):
		self.bins=(8,12,3)
		self.indexPath = "models/gini/index.csv"

	def describenew(self,shapes):
		datapath="models/gini/hogface/shape_predictor_68_face_landmarks.dat"
		#detector = dlib.get_frontal_face_detector() - uncomment for facial landmark
		#predictor = dlib.shape_predictor(datapath)
		
		# Show faces
		#rects = detector(imgs, 1)
                #shapes = predictor(imgs, rect)
		res=[]
		for (x,y) in shapes:
			res.append(math.atan(y/x))
		return res
		
 
	def describe(self, img):
		# convert the image to the HSV color space and initialize
		# the features used to quantify the image
		cv2.imshow("indescribe", img)
		#cv2.waitKey(1500)

		image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		features = []
 
		# grab the dimensions and compute the center of the image
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5))

		# divide the image into four rectangles/segments (top-left,
		# top-right, bottom-right, bottom-left)
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),(0, cX, cY, h)]
 
		# construct an elliptical mask representing the center of the
		# image
		(axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
 
		# loop over the segments
		for (startX, endX, startY, endY) in segments:
			# construct a mask for each corner of the image, subtracting
			# the elliptical center from it
			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			cornerMask = cv2.subtract(cornerMask, ellipMask)
 
			# extract a color histogram from the image, then update the
			# feature vector
			hist = self.histogram(image, cornerMask)
			features.extend(hist)
 
		# extract a color histogram from the elliptical region and
		# update the feature vector
		hist = self.histogram(image, ellipMask)
		features.extend(hist)
		cv2.destroyAllWindows	
		# return the feature vector
		return features

	def histogram(self, image, mask):
		# extract a 3D color histogram from the masked region of the
		# image, using the supplied number of bins per channel; then
		# normalize the histogram
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
			[0, 180, 0, 256, 0, 256])
		hist = cv2.normalize(hist,hist).flatten()
                #print hist
		# return the histogram
		return hist



	def index(self):
		path="img/users/"
		imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
		faces=[]
		ids=[]
		output = open("models/gini/index.csv", "w")
		
		for imagePath in imagePaths:
			faceImg=Image.open(imagePath)#.convert('L');
			faceNP=np.array(faceImg,"uint8")
                        #cv2.imshow("Training", faceNP)
			id= int(os.path.split(imagePath)[-1].split('.')[0])
                	#print imagePath
			features = self.describe(faceNP)
			# write the features to file
			features = [str(f) for f in features]
			output.write("%s,%s\n" % (id, ",".join(features)))
			cv2.imshow("Training", faceNP)
			cv2.waitKey(20)
	
		output.close()
		cv2.destroyAllWindows	
		return 


	def search(self, image, limit = 10):
		queryFeatures= self.describe(image)
		results = {}
				
		# open the index file for reading
		with open(self.indexPath) as f:	
			reader = csv.reader(f)
			for row in reader:
				features = [float(x) for x in row[1:]]
				d = self.chi2_distance(features, queryFeatures)
				results[row[0]] = d
			f.close()

		results = sorted([(v, k) for (k, v) in results.items()])		
		return results[:limit]

	def chi2_distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])
 
		# return the chi-squared distance
		return d	

