#from ginilib.ipcam1 import camera
#from ginilib.LPRS import vehicles
import time
#from ginilib.com import communication
from ginilib.db import dbops
from ginilib.FaceUtil import faces
#from ginilib.client import client
from ginilib.watch import camera
import sys
import openface
import cv2
from ginilib.facerec_adapter import facerec
import os
import datetime
import base64



dbs=dbops()
#xyz=dbs.get_camViews_byname("FrontDesk")

#print(xyz)

'''
accountid=4
camdlist = dbs.get_Camera_list_by_userid(str(accountid))
camname=[]
for cam in camdlist:
    print(cam[1].upper())
'''

# create db records for camera
name="cam"
ip="http://192.168.1.144:8080/shot.jpg"
location=4
type="http"
userid=4
id=4

while id<=50:
    fname=name +str(id)
    dbs.Add_Camera(fname,ip,"xyz",location,type,userid)
    id=id+1

print ("record created successfully")
'''
dates=str(datetime.datetime.now())
x=dbs.get_Camera_list_by_userid(4)
#x=dbs.get_Camera_list_sharedtome(4)
print (x)
for s in x:
    print s[1]
    

#dbs.createAccount("harsha","parvatikar","a@b.com","hkp123",dates,dates,dates,True)
#x=dbs.get_Account_details_byname("a@b.com")
#print x[0][0]
#print(base64.b64decode(x[0][4]))
#xyz=dbs.generate_report(5,13,8,2018)
#print(xyz)

fileDir = os.path.dirname(os.path.realpath(__file__))
path=os.path.join(fileDir, 'img/users')
fc=facerec()

#fc.buildmodel()
#fc.train_All(path)
#fc.updatemodel()
#fc.train("harshavardhan","btmresidency",9845552513,"a@b.com",str(10135004))
#fc.updatemodel()

#bgrImg = cv2.imread("04161622_1.jpg")
#id=fc.infer(bgrImg)
#print(id)

#from PyQt5 import QtGui, QtWidgets,uic

#from avisUI import MyApp


app = QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())


#Enroll User

fc=client()
fc.enroll_user()


#View and track

#cam=camera(9)
#cam.start()
#cam.run()
#cam.stop()

fc=faces()
fc.train()

# DB Operation

dbs=dbops()
#dbs.Add_Camera("CamName","IP","address","Location","Type")
#dbs.update_Camera(4,"CamName","NewName")
#res=dbs.get_Camera_details(4)

res=dbs.get_Camera_list()
print (res)

#for row in res:
#	print (row)
#	print ("\n")


#res=dbs.Delete_Camera(4)

#dbs.Add_user ("NAme","#48 BTM Residency",9845552513,"visitor",123456789)
#dbs.update_user (2,"Name","Shreya")
#res=dbs.get_user_details(2)
#for row in res:
#	print(row)
#res=dbs.Delete_user(2)



#UC2 Detect and add Number plates
#vh=vehicles()
#vh.detect_plate()

'''

