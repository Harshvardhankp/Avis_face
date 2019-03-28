import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,QMessageBox
from ui.mainwindow import Ui_MainWindow
from ui.addcamera import Ui_AddCamera
from ui.trackuser import Ui_trackuser
from ui.viewcamera import Ui_ViewCamera
import numpy as np
import cv2
from ginilib.db import dbops
import urllib
from datetime import date,time,datetime
import os
import shutil
from ginilib.facerec_adapter import facerec
from ginilib.db import dbops
import pickle
import face_recognition
from datetime import datetime, timedelta
import time


class MyApp(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MyApp, self).__init__(parent)
        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.trackuser_obj = MyApp_trackuser()
        self.addcamera_obj = MyApp_AddCamera()
        self.viewcamera_obj= MyApp_ViewCamera()
        self.ui.viewuser.setVisible(False)
        self.ui.VisitorLog.setVisible(False)
        self.dbs=dbops()

        self.ui.trackuser.clicked.connect(self.show_trackuser)
        self.ui.addcamera.clicked.connect(self.show_addcamera)
        self.ui.viewcamera.clicked.connect(self.show_viewcamera)
        self.ui.attendence.clicked.connect(self.generatereport)
        #self.ui.adduser.setDisabled(True)
        #self.ui.viewuser.setDisabled(True)


    def generatereport(self):
        today = datetime.now().date()
        start = today - timedelta(days=today.weekday())
        startday=start.day
        end = start + timedelta(days=6)
        endday=end.day
        now=datetime.now()
        month=now.month
        year=now.year
        self.dbs.generate_report(startday,endday,month,year)



    def show_trackuser(self):
        self.trackuser_obj.show()

    def show_addcamera(self):
        self.addcamera_obj.show()

    def show_viewcamera(self):
        self.viewcamera_obj.show()

class returnfaces(QThread):
    changePixmap = pyqtSignal(QPixmap)
    def __init__(self,url,length,height,type,framenos,parent=None):
        self.type=type
        self.framenos=int(framenos)
        self.url=url
        self.length=int(length)
        self.height=int(height)

        if self.type == "webcam":
            id=int(self.url)
            self.video = cv2.VideoCapture(id)

        elif self.type == "rtsp":
            id = self.url
            self.video = cv2.VideoCapture(id)

        elif self.type == "http":
            id=self.url
            #self.imgResp = urllib.urlopen(self.url)
            #self.imgResp = requests.get(self.ur, stream=True, verify=True)

        self.face_cascade = cv2.CascadeClassifier('./models/haarcascades/haarcascade_frontalface_default.xml')
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        QThread.__init__(self, parent)

    def run(self):

        connectport=self.url
        print (connectport)
        dbs = dbops()
        ids = 11  # this is camera id
        # Getting camera details
        camdetails = dbs.get_Camera_details(ids)
        camname = camdetails[0].upper()
        camid = camdetails[1]
        camlocation = camdetails[2].upper()
        cam_type = camdetails[3]
        Camtype = cam_type

        # Load Model
        fileDir = os.path.dirname(os.path.realpath(__file__))
        unknownusers_dir = os.path.join(fileDir, "img/unknownusers/tmp")
        if not os.path.exists(unknownusers_dir):
            try:
                os.makedirs(unknownusers_dir)
            except:
                print ("unable to create directory")
        root = "./videos/" + camname + "/live"
        counter = 0
        samplenum = 0
        files = []
        readframe=False
        #Left to Right
        while counter<=20:
            try:
                if self.type == "webcam":
                    success, img = self.video.read()
                elif self.type == "rtsp":
                    success, img = self.video.read()

                elif self.type == "http":
                    imgResp = urllib.urlopen(connectport)
                    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
                    img = cv2.imdecode(imgNp, -1)

                else:
                    # camera.capture(rawCapture, format="bgr")
                    # img = rawCapture.array
                    time.sleep(0.1)
                # put the image on screene
                time.sleep(0.4)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Show faces
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
                if len(faces)>1:
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w + 10, y + h + 10), (0, 0, 255), 2)
                        cv2.putText(img, "Multiple Faces --Invalid Recording", (x + w + 12, y - 10), self.font, 0.6, 255)

                else:
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w + 10, y + h + 10), (0, 255, 255), 2)
                        cv2.putText(img, "Recording", (x + w + 12, y - 10), self.font, 0.4, 255)
                        userid = "U" + str(counter) + ".jpg"
                        saveunknownto = os.path.join(unknownusers_dir, userid)
                        cv2.imwrite(saveunknownto, img[y:y + h + 10, x:x + w + 10])
                        files.append(saveunknownto)
                        counter += 1


                rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                p = convertToQtFormat.scaled(self.length, self.height, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


            except:
                print("unable to get feeds")

        cv2.destroyAllWindows()
        self.video.release()

        return

    def join(self):
        QThread.join(self)
        return self._return

class getcamfeed(QThread):
    changePixmap = pyqtSignal(QPixmap)

    def __init__(self, url, length, height, type, framenos, parent=None):
        self.type = type
        self.framenos = int(framenos)
        self.url = url
        self.length = int(length)
        self.height = int(height)

        if self.type == "webcam":
            id = int(self.url)
            self.video = cv2.VideoCapture(id)

        elif self.type == "rtsp":
            id = self.url
            self.video = cv2.VideoCapture(id)

        elif self.type == "http":
            id = self.url
            self.imgResp = urllib.request(self.ur)
            # self.imgResp = requests.get(self.ur, stream=True, verify=True)

        self.face_cascade = cv2.CascadeClassifier('./models/haarcascades/haarcascade_frontalface_default.xml')
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        QThread.__init__(self, parent)

    def run(self):
        connectport = self.url
        print (connectport)
        dbs = dbops()
        ids = 9  # this is camera id
        # Getting camera details
        camdetails = dbs.get_Camera_details(ids)
        camname = camdetails[0].upper()
        camid = camdetails[1]
        camlocation = camdetails[2].upper()
        cam_type = camdetails[3]
        Camtype = cam_type

        # Load Model
        fileDir = os.path.dirname(os.path.realpath(__file__))
        while (True):
            try:
                if self.type == "webcam":
                    success, img = self.video.read()

                elif self.type == "rtsp":
                    success, img = self.video.read()

                elif self.type == "http":
                    imgResp = urllib.urlopen(connectport)
                    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
                    img = cv2.imdecode(imgNp, -1)

                else:
                    # camera.capture(rawCapture, format="bgr")
                    # img = rawCapture.array
                    time.sleep(0.1)
                # put the image on screen
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.putText(img, "TENSOR LABS BANGALORE", (100, 40), self.font, 0.9, (0, 0, 150))
                datefield = "Date:" + str(date.today())
                cv2.putText(img, datefield, (700, 40), self.font, 0.6, (0, 0, 150))
                cv2.putText(img, camname + ":" + camlocation, (700, 60), self.font, 0.6, (0, 0, 150))


                rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                p = convertToQtFormat.scaled(self.length, self.height, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

            except:
                print("unable to get feeds")

        cv2.destroyAllWindows()
        return

    def join(self):
        QThread.join(self)
        return self._return


class MyApp_trackuser(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super( MyApp_trackuser, self).__init__(parent)
        # Set up the user interface from Designer.
        self.dbs = dbops()
        self.ui = Ui_trackuser()
        self.ui.setupUi(self)
        self.ui.record.setVisible(False)
        self.ui.record.clicked.connect(self.selectimage)
        self.ui.save.clicked.connect(self.savetracker)
        self.ui.cancel.clicked.connect(self.canceltracker)
        self.ui.recorduser.clicked.connect(self.recordimages)



    def selectimage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileNames, _ =QFileDialog.getOpenFileNames(self, "Open Image", "","All Files (*);;Python Files (*.py)",options=options)

        if self.fileNames:
            print(self.fileNames)
        pixmap = QPixmap(self.fileNames[0])
        pixmap=pixmap.scaled(151,151)
        self.ui.video.setPixmap(pixmap)
        print("completed")

    def recordimages(self):
        threads = []
        camname = "WebCam"
        res = self.dbs.get_Camera_details_byname(str(camname))
        Type = "webcam"
        print(Type)
        IP = 0

        if (IP != ""):
            self.th = returnfaces(url=IP, length=331, height=280, type=Type, framenos=100)
            self.th.changePixmap.connect(self.ui.video.setPixmap)
            self.th.start()
        else:
            print("IP value is blank please enter value")

        fileDir = os.path.dirname(os.path.realpath(__file__))
        unknownusers_dir = os.path.join(fileDir, "img/unknownusers/tmp")
        self.fileNames = [os.path.join(unknownusers_dir, f) for f in os.listdir(unknownusers_dir)]
        print self.fileNames

    def savetracker(self):
        filename=str(datetime.now().strftime("%d%H%M%S"))
        frc=facerec()
        name = self.ui.name.toPlainText()
        address = self.ui.address.toPlainText()
        mobile = int(self.ui.mobile.toPlainText())
        email = self.ui.email.toPlainText()
        nationalid =filename # int(self.ui.nationalid.toPlainText())
        directory="./ginilib/openface/training-images/" + filename
        directory_old="./img/users/" + filename

        if not os.path.exists(directory_old):
            try:
                os.makedirs(directory_old)
            except:
                print ("unable to create directory")
        i=0
        for file in self.fileNames:
            imagename = directory_old +"/"+ filename + "_" + str(i) + ".jpg"
            shutil.copyfile(file,imagename)
            i+=1
            print(imagename)
            print("file copied to source directory")

        frc.train(name, address, mobile, email, nationalid)
        print("saved successfully")
        self.canceltracker()

    def canceltracker(self):
        self.ui.name.clear()
        self.ui.address.clear()
        self.ui.mobile.clear()
        self.ui.email.clear()
        self.ui.nationalid.clear()
        self.close()

class MyApp_AddCamera(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super( MyApp_AddCamera, self).__init__(parent)
        self.dbs = dbops()
        # Set up the user interface from Designer.
        self.ui = Ui_AddCamera()
        self.ui.setupUi(self)
        self.ui.save.clicked.connect(self.savecamera)
        self.ui.cancel.clicked.connect(self.closecamera)
        self.ui.record.clicked.connect(self.testcamera)

    def savecamera(self):
        CamName=self.ui.camname.toPlainText()
        IP=self.ui.ip.toPlainText()
        address=self.ui.address.toPlainText()
        Location=self.ui.location.toPlainText()
        Type=self.ui.camtype.currentText()
        if (CamName != "") and (IP != "") and (address != "") and (Location != "") and (Type != ""):
            self.dbs.Add_Camera(CamName, IP, address, Location, Type)
            print ("Db values updated")
        else:
            print ("Suply Missing values")

    def closecamera(self):
        self.ui.camname.clear()
        self.ui.ip.clear()
        self.ui.address.clear()
        self.ui.location.clear()
        self.close()

    def testcamera(self):
        threads = []
        IP=str(self.ui.ip.toPlainText())
        Type=self.ui.camtype.currentText()
        try:
            if (IP != ""):
                if (Type == "Non IP Camera"):
                    IP=int(IP)
                else:
                    IP=IP
                self.th = getcamfeed(url=IP,length=211,height=140,type=Type,framenos=20)
                self.th.changePixmap.connect(self.ui.video.setPixmap)
                self.th.start()
            else:
                print("IP value is blank please enter value")
        except:
            print("Camera Type is incorrect")

class MyApp_ViewCamera(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super( MyApp_ViewCamera, self).__init__(parent)
        # Set up the user interface from Designer.
        self.ui = Ui_ViewCamera()
        self.ui.setupUi(self)
        self.dbs = dbops()
        camlist=list(self.dbs.get_Camera_list())
        names=[]
        for cam in camlist:
            names.append(str(cam[1]))
        print (names)
        self.ui.viewcameralist.addItems(names)
        self.ui.View.clicked.connect(self.showvideo)

    def showvideo(self):
        threads = []
        camname = self.ui.viewcameralist.currentText()
        res=self.dbs.get_Camera_details_byname(str(camname))
        Type = str(res[3])
        print(Type)
        IP=str(res[1])
        if (IP != ""):
            if (Type == "Non IP Camera"):
                print(IP)
                IP = IP
            else:
                print (IP)
                IP = IP
            self.th = getcamfeed(url=IP,length=491,height=371,type=Type,framenos=100)
            self.th.changePixmap.connect(self.ui.video.setPixmap)
            self.th.start()
        else:
            print("IP value is blank please enter value")


if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        window = MyApp()
        window.show()
        sys.exit(app.exec_())