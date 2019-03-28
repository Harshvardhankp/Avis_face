#!/usr/bin/env python2
import time
import cv2
import os
import pickle
import sys
from operator import itemgetter
import numpy as np
np.set_printoptions(precision=2)
import pandas as pd
import openface
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
#from sklearn.mixture import GMM
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from ginilib import datalib as d
import face_recognition
from ginilib.db import dbops
import shutil
from datetime import date,time,datetime
from ginilib.communication import communication
#from ginilib.preprocess import preproc

#start = time.time()


class facerec:
    def __init__(self):
        self.fileDir = os.path.dirname(os.path.realpath(__file__))
        self.modelDir = os.path.join(self.fileDir, 'openface/models')
        self.dlibModelDir = os.path.join(self.modelDir, 'dlib')
        self.openfaceModelDir = os.path.join(self.modelDir, 'openface')
        self.dlibFacePredictor = os.path.join(self.dlibModelDir, "shape_predictor_68_face_landmarks.dat")
        self.networkModel = os.path.join(self.openfaceModelDir, 'nn4.small2.v1.t7')
        self.workDir = os.path.join(self.fileDir, 'openface/generated-embeddings')
        self.WDInputImage = os.path.join(self.fileDir, 'openface/training-images')
        self.WDAlignedImages = os.path.join(self.fileDir, 'openface/aligned-images')
        self.WDutils = os.path.join(self.fileDir, 'openface/util')
        self.WDembeddings = os.path.join(self.fileDir, 'openface/generated-embeddings')
        self.WDbatchrepresent = os.path.join(self.fileDir, 'openface/batch-represent/main.lua')
        self.imgDim = 96
        self.cuda = False
        self.verbose = False
        self.ldaDim = -1
        self.classifier = 'LinearSvm'  # GridSearchSvm,GMM,RadialSvm,DecisionTree,GaussianNB,DBN
        self.inferParser = "infer"  # Predict who an image contains from a trained classifier.
        self.classifierModel = os.path.join(self.fileDir,'openface/generated-embeddings/classifier.pkl')
        multi = False  # -Infer multiple faces in image"
        self.dbs=dbops()
        self.mode = "infer"
        self.face_cascade = cv2.CascadeClassifier('./models/haarcascades/haarcascade_frontalface_default.xml')
        #self.x = preproc()


        #start = time.time()

        if self.verbose:
            print("Argument parsing and import libraries took {} seconds.".format(
                time.time() - self.start))

        if self.mode == 'infer' and self.classifierModel.endswith(".t7"):
            raise Exception("""Use `--networkModel` to set a non-standard Torch network model.""")

        self.align = openface.AlignDlib(self.dlibFacePredictor)
        self.net = openface.TorchNeuralNet(self.networkModel, imgDim=self.imgDim,
                                      cuda=self.cuda)
        #Open classifier model
        if os.path.exists(self.classifierModel):
            with open(self.classifierModel, 'rb') as f:
                if sys.version_info[0] < 3:
                    (self.le, self.clf) = pickle.load(f)
                else:
                    (self.le, self.clf) = pickle.load(f, encoding='latin1')

    def getRep(self,img, multiple=False):
        start = time.time()
        bgrImg = img
        if bgrImg is None:
            raise Exception("Unable to load image: {}")

        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
        cv2.imshow("tgbimg",rgbImg)

        if self.verbose:
            print("  + Original size: {}".format(rgbImg.shape))
        if self.verbose:
            print("Loading the image took {} seconds.".format(time.time() - start))

        start = time.time()

        if multiple:
            bbs = self.align.getAllFaceBoundingBoxes(rgbImg)
        else:
            bb1 = self.align.getLargestFaceBoundingBox(rgbImg)
            bbs = [bb1]
        #if len(bbs) == 0 or (not multiple and bb1 is None):
            #raise Exception("Unable to find a face: {}")
        if self.verbose:
            print("Face detection took {} seconds.".format(time.time() - start))

        reps = []
        for bb in bbs:
            start = time.time()
            alignedFace = self.align.align(
                self.imgDim,
                rgbImg,
                bb,
                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            if alignedFace is None:
                #raise Exception("Unable to align image: {}")
                alignedFace=rgbImg
            if self.verbose:
                print("Alignment took {} seconds.".format(time.time() - start))
                print("This bbox is centered at {}, {}".format(bb.center().x, bb.center().y))

            start = time.time()
            rep = self.net.forward(alignedFace)
            if self.verbose:
                print("Neural network forward pass took {} seconds.".format(
                    time.time() - start))
            reps.append((bb.center().x, rep))
        sreps = sorted(reps, key=lambda x: x[0])
        return sreps

    def train(self,name, address, mobile, email, id):
        # Create Input Images
        directory = os.path.join(self.WDInputImage, id)
        directory_old = "./img/users/" + id
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except:
                print ("unable to create directory")
        d.generatedata(directory_old,directory,id,20)
        shutil.rmtree(directory_old)
        # Align Images in Source Directory
        file=self.WDutils + "/" + "align-dlib.py"
        aligndir=file +" " +self.WDInputImage +" "+ "align outerEyesAndNose" + " " + self.WDAlignedImages + " --size 96 "
        print(aligndir)
        try:
            os.system(aligndir)
            print("images are aligned successfully")
        except:
            print("unable to align images")

        #Generate Embeddendings with New User
        path =os.path.join(self.WDAlignedImages, id)
        ids=[]
        faces_encodings=[[]]
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        for imagePath in imagePaths:
            faceImg = face_recognition.load_image_file(imagePath)
            loc=face_recognition.face_locations(faceImg,model="cnn")
            print("loc is here",loc)
            if loc:
                encoding = face_recognition.face_encodings(faceImg,loc)[0]
                self.dbs.Track_user(name, address, mobile, email, id, encoding)
                encoding=np.asanyarray(encoding)
                enc=[]
                for x in encoding:
                    enc.append(float(x))
                faces_encodings.append(enc)
                ids.append(id)

        df=pd.DataFrame(list(map(list,zip(ids,faces_encodings))))
        filename="encode/"+id+".csv"
        filepath=os.path.join(self.WDembeddings, filename)
        np.savetxt(filepath,faces_encodings,delimiter=",",fmt='%s')
        #df.to_csv(filepath,sep='\t')
        print("Embeddings generated  successfully")
        shutil.rmtree(directory)
        aligndir = os.path.join(self.WDAlignedImages, id)
        shutil.rmtree(aligndir)
        self.buildmodel()

    def datapreprocessing(self,path):
        fileDir = os.path.dirname(os.path.realpath(__file__))
        file = fileDir + "/" + "preprocess.py"
        arg1="--input-dir"
        arg2="--output-dir"
        # Create Input Images
        try:
            os.system('%s %s %s %s %s %s' % (sys.executable, file, arg1, path, arg2, self.WDInputImage))
            print("images are aligned successfully")
        except:
            print("unable to align images")

        fnames = os.listdir(self.WDInputImage)
        for fname in fnames:
            dpath = os.path.join(self.WDInputImage, fname)
            directory = os.path.join(self.WDAlignedImages, fname)
            directory_old = dpath
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except:
                    print ("unable to create directory")
            d.generatedata(directory_old, directory, fname, 2)


    def train_All(self,path):
        self.datapreprocessing(path)
        #Generate Embeddendings with New User

        dirnames=os.listdir(self.WDAlignedImages)
        for dname in dirnames:
            path =os.path.join(self.WDAlignedImages, dname)
            ids=[]
            faces_encodings=[[]]
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            userid = str(datetime.now().strftime("%d%H%M%S"))
            for imagePath in imagePaths:
                faceImg = face_recognition.load_image_file(imagePath)
                loc = face_recognition.face_locations(faceImg,model="cnn")
                locflag=False
                print(loc)
                if loc:
                    locflag=True
                else:
                    faceImg = cv2.imread(imagePath)
                    rgb = faceImg[:, :, ::-1]
                    gray = cv2.cvtColor(faceImg, cv2.COLOR_BGR2GRAY)
                    faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
                    for (x, y, w, h) in faces:
                        cv2.rectangle(faceImg, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        norm_image2 = faceImg[y:y + h, x:x + w]
                        rgb = norm_image2[:, :, ::-1]
                        loc=face_recognition.face_locations(rgb,model="cnn")
                        print(loc)
                        if loc:
                            locflag=True

                if locflag==True:
                    encoding = face_recognition.face_encodings(faceImg,loc)[0]
                    self.dbs.Track_user(dname, "", "", "", userid, encoding)
                    encoding=np.asanyarray(encoding)
                    enc=[]
                    for x in encoding:
                        enc.append(float(x))
                        faces_encodings.append(enc)
                        ids.append(userid)

            shutil.rmtree(os.path.join(self.WDInputImage,dname))
            shutil.rmtree(os.path.join(self.WDAlignedImages,dname))
        print("Embeddings generated  successfully")
        self.buildmodel()

    def buildmodel(self):
        #This Module consists of code specific to Developing modle from db
        #Train SVM with new details
        print("Loading embeddings.")
        classifier=self.classifier
        ldaDim=self.ldaDim
        label,name,embeddings=self.dbs.get_Track_user_list()
        labels=np.asarray(label,dtype=int)
        embeddings=np.asarray(embeddings,dtype=float)
        print(embeddings)
        print(labels)
        workDir=self.workDir
        le = LabelEncoder().fit(labels)
        labelsNum = le.transform(labels)
        nClasses = len(le.classes_)
        print("Training for {} classes.".format(nClasses))

        if classifier == 'LinearSvm':
            clf = SVC(C=1, kernel='linear', probability=True)
        elif classifier == 'GridSearchSvm':
            print("""
            Warning: In our experiences, using a grid search over SVM hyper-parameters only
            gives marginally better performance than a linear SVM with C=1 and
            is not worth the extra computations of performing a grid search.
            """)
            param_grid = [
                {'C': [1, 10, 100, 1000],
                 'kernel': ['linear']},
                {'C': [1, 10, 100, 1000],
                 'gamma': [0.001, 0.0001],
                 'kernel': ['rbf']}
            ]
            clf = GridSearchCV(SVC(C=1, probability=True), param_grid, cv=5)
       # elif classifier == 'GMM':  # Doesn't work best
           # clf = GMM(n_components=nClasses)

        # ref:
        # http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html#example-classification-plot-classifier-comparison-py
        elif classifier == 'RadialSvm':  # Radial Basis Function kernel
            # works better with C = 1 and gamma = 2
            clf = SVC(C=1, kernel='rbf', probability=True, gamma=2)
        elif classifier == 'DecisionTree':  # Doesn't work best
            clf = DecisionTreeClassifier(max_depth=20)
        elif classifier == 'GaussianNB':
            clf = GaussianNB()

        # ref: https://jessesw.com/Deep-Learning/
        clf.fit(embeddings, labelsNum)

        fName = "{}/classifier.pkl".format(workDir)
        print("Saving classifier to '{}'".format(fName))
        with open(fName, 'wb') as f:
            pickle.dump((le, clf), f)

    def updatemodel(self):
        # Create Input Images
        path= "./img/updateusers/"
        processed="./img/processed"
        fnames=os.listdir(path)
        for fname in fnames:
            dpath=os.path.join(path,fname)
            directory = os.path.join(self.WDInputImage, fname)
            directory_old = dpath
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except:
                    print ("unable to create directory")
            d.generatedata(directory_old,directory,fname,5)

        # Align Images in Source Directory
        file=self.WDutils + "/" + "align-dlib.py"
        aligndir=file +" " +self.WDInputImage +" "+ "align outerEyesAndNose" + " " + self.WDAlignedImages + " --size 96 "
        print(aligndir)
        try:
            os.system(aligndir)
            print("images are aligned successfully")
        except:
            print("unable to align images")

        #Generate Embeddendings with New User
        dirnames=os.listdir(self.WDInputImage)
        for dname in dirnames:
            path =os.path.join(self.WDInputImage, dname)
            ids=[]
            faces_encodings=[[]]
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            userid = dname
            for imagePath in imagePaths:
                faceImg = face_recognition.load_image_file(imagePath)
                loc = face_recognition.face_locations(faceImg)
                locflag=False
                if loc:
                    locflag=True
                else:
                    faceImg = cv2.imread(imagePath)
                    rgb = faceImg[:, :, ::-1]
                    gray = cv2.cvtColor(faceImg, cv2.COLOR_BGR2GRAY)
                    faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
                    for (x, y, w, h) in faces:
                        cv2.rectangle(faceImg, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        norm_image2 = faceImg[y:y + h, x:x + w]
                        rgb = norm_image2[:, :, ::-1]
                        loc=face_recognition.face_locations(rgb,model="cnn")
                        print(loc)
                        if loc:
                            locflag=True

                if locflag==True:
                    encoding = face_recognition.face_encodings(faceImg,loc)[0]
                    self.dbs.Track_user(dname, "", "", "", userid, encoding)
                    encoding=np.asanyarray(encoding)
                    enc=[]
                    for x in encoding:
                        enc.append(float(x))
                        faces_encodings.append(enc)
                        ids.append(userid)

            shutil.rmtree(path)
            shutil.rmtree(os.path.join(self.WDAlignedImages,dname))
        print("Embeddings generated  successfully")
        self.buildmodel()


