#!/usr/bin/env python
from flask import Flask, render_template, Response,flash, redirect,  request, session, abort,send_from_directory,url_for
from ginilib.db import dbops
import os
import datetime
import base64
from moviepy.editor import VideoFileClip, concatenate_videoclips
import shutil
from datetime import date,time,datetime
from ginilib.facerec_adapter import facerec
#paint
import os
import sys
import json
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from flask import Flask, render_template, request

#file upload for track
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug import secure_filename
import shutil
# emulated camera
from camera import camera
from camera_video import camera_video
#from copy import deepcopy
import pandas as pd 
import csv
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera
application = Flask(__name__)





@application.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')

@application.route('/login', methods=['POST'])
def do_admin_login():
    dbs=dbops()
    email=request.form['email']
    print("email_id",email)	
    x = dbs.get_Account_details_byname(str(email))
    if len(x) > 0 :
	pwd=x[0][4]
	print("pwd here",pwd)

        #pwd=base64.b64decode(x[0][4]).decode("utf-8", "ignore")
        if request.form['password'] == pwd :
            session['logged_in'] = True
            session['user']=request.form['email']
            session['userid']=x[0][0]
            user=request.form['email']
            return render_template('index.html',usr=user)

        else:
            return 'wrong password!'
            return render_template('login.html')
    else:
        return 'wrong password!'
        return render_template('login.html')


@application.route('/registration', methods=['POST'])
def do_registration():
       dbs=dbops()
       fname=request.form['firstname']
       lname = request.form['lastname']
       email = request.form['email']
       pwd=request.form['password']
       #pwd = base64.b64encode(bytes(request.form['password'],"utf-8"))
       #pwd = base64.b64encode(request.form['password'])
       active=True

       adate= str(datetime.datetime.now())
       astart=str(datetime.datetime.now())
       aend=str(datetime.datetime.now())

       try:
           dbs.createAccount(fname,lname,email,pwd,adate,astart,aend,active)
           return render_template('login.html')

       except Exception as e:
           print(e)
           return render_template('register.html')

@application.route('/enrolluser', methods=['POST'])
def do_enrollment():
    fc = facerec()
    print("doing enrollment")
    dbs = dbops()
    img = request.form['image']
    print(img)	
    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']
    address = request.form['address']
    nationalid = request.form['nationalid']



    imgs=str(img).split("image/")
    imgs=str(img).split(";base64,")
    print(imgs[1])
    imgbase=base64.b64decode(imgs[1])

    userid = str(datetime.now().strftime("%d%H%M%S"))
    rootDir = os.path.dirname(os.path.realpath(__file__))
    usersRDir= os.path.join(rootDir,"./img/users")
    usersDir=os.path.join(usersRDir,str(userid))
    if not os.path.exists(usersDir):
        try:
            os.makedirs(usersDir)
        except:
            print ("unable to create directory",usersDir)
    filename="user.jpg"
    imgpath=os.path.join(usersDir,filename)
    image_result = open(imgpath, 'wb')
    image_result.write(imgbase)
    image_result.close()
    fc.train(name,address,mobile,email,str(userid))
    return render_template('enrolluser.html')
@application.route('/logout')
def logout():
        session['logged_in'] = False
        return render_template('login.html')

@application.route('/register')
def register():
        return render_template('register.html')

@application.route('/forgotpwd')
def forgotpwd():
        return render_template('forgot-password.html')

@application.route('/mycamera')
def mycamera():
        return render_template('mycamera.html')

@application.route('/enrolluser')
def enrolluser():
        return render_template('enrolluser.html')


@application.route('/trackuser')
def trackuser():
        return render_template('trackuser.html')


photos = UploadSet('photos', IMAGES)
application.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(application, photos)

@application.route('/trackuser', methods=['POST'])
def do_trackuser():
    fc = facerec()
    print("doing Track user")
    dbs = dbops()	
    name = request.form['name']
    print(name)	
    email = request.form['email']
    print(email)		
    mobile = request.form['mobile']
    print(mobile)	
    address = request.form['address'] 
    print(address)
    nationalid = request.form['nationalid']
    print(nationalid)	

    userid = str(datetime.now().strftime("%d%H%M%S"))
    rootDir = os.path.dirname(os.path.realpath(__file__))
    usersRDir= os.path.join(rootDir,"./img/users")
    usersDir=os.path.join(usersRDir,str(userid))
    print(usersDir)

    if not os.path.exists(usersDir):
    	try:
            os.makedirs(usersDir)
        except:
            print ("unable to create directory",usersDir)

    img =photos.save(request.files['photo']) 
    #Files are copy from the static/img	
    source = './static/img/'
    dest = './img/users/'+ str(userid)
    files = os.listdir(source)
    for f in files:
    	shutil.move(source + f,dest)

    SOURCE = './img/users/' +str(userid)
    BACKUP = './img/trackusers/'
    files = os.listdir(SOURCE)
    for f in files:
    	fpath=SOURCE +"/"+f	
    	shutil.copy(fpath,BACKUP)
        #os.rename(user.jpg,userid +'.jpg' )
    dbs.Transactions("null",userid,name,address,email,mobile,nationalid,"Searching","email","cam1")
    fc.train(name,address,mobile,email,str(userid))
    return render_template('trackuser.html')

@application.route('/trackstatus',methods = ['POST', 'GET'])
def trackstatus():
	dbs=dbops()
	data=dbs.get_Transactions()
	print(data)
	return render_template("trackstatus.html",result = data)
        
'''
@application.route('/result',methods = ['POST', 'GET'] )
def result():
   if request.method == 'POST':
      result = request.form
      dbs=dbops()
      data=dbs. get_Transactions()
      print(data)
      return render_template("result.html",result = data)
'''

@application.route('/Vehicletrack')
def Vehicletrack():
        return render_template('Vehicletrack.html')

@application.route('/face.html')
def face():
	#dbs=dbops()
	#data=dbs.get_Alerts()
	#print(data)
        return render_template('face.html',camnm="cam1")

def genv(camera_video):
    """Video streaming generator function."""
    while True:
        frame = camera_video.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@application.route('/video_feed_video/<name>')
def video_feed_video(name):

    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(genv(camera_video(name)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
        

@application.route('/help')
def help():
        return render_template('help.html')

@application.route('/setting')
def setting():
        return render_template('setting.html')

@application.route('/storagesetting')
def storagesetting():
        return render_template('storagesetting.html')

UPLOAD_FOLDER = '/img'
ALLOWED_EXTENSIONS = set(['csv'])
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@application.route('/CamSettings',methods=['GET', 'POST'])
def CamSettings():
	dbs=dbops()
	accountid=session.get('userid')
	accountid=int(accountid)
	if request.method == 'POST':
        	f = request.files['file']
        	filename = f.filename
		path ='./static' 
            	f.save(os.path.join(path, filename))
		f= path + '/' + filename
		input_file = open(f,"r+")
		reader_file = csv.reader(input_file)

		#data = pd.read_csv(f) 
		#row=data.iloc[1]
                for r in list(reader_file):
                	print r[0]
			dbs.Add_Camera(r[0],r[1],r[2],r[3],accountid)
		data=dbs.get_Camera_list()
	        return render_template('CamSettings.html',result = data)
     	if request.method == 'GET':
		data=dbs.get_Camera_list()
		print(data)
		return render_template('CamSettings.html',result = data)
   

@application.route('/savesettings', methods=['POST'])
def savesettings():
       dbs=dbops()
       name=request.form['name']
       ps = request.form['ps']
       ss = request.form['ss']
       ts=request.form['ts']
       dur = request.form['dur']

       try:
           dbs.save_settings(name,ps,ss,ts,dur)
           Headings="Success !!!!"
           Messages="Settings Saved successfully"
           return render_template('404.html', top=Headings, msg=Messages)

       except Exception as e:
           print(e)
           Headings="Error !!!!"
           Messages=e
           return render_template('404.html',top=Headings, msg=Messages)




@application.route('/reports')
def reports():
        return render_template('reports.html')


@application.route('/export')
def export():
        return render_template('export.html')

@application.route('/index')
def index():
    """Video streaming home page."""
    username=session.get('user')
    return render_template('index.html')

@application.route('/view')
def view():
    """Video streaming home page."""
    accountid=session.get('userid')
    print(accountid)
    dbs = dbops()
    camdlist = dbs.get_Camera_list_by_userid(str(accountid))
    camname=[]
    for cam in camdlist:
        print(cam[1])
        camname.append(cam[1].upper())

    camviewlist = dbs.get_camViews(accountid)
    listview = []
    if len(camviewlist) != 0:
        for camview in camviewlist:
            listview.append(camview[1])
    return render_template('viewcam.html',cameras=camname,camviews=listview)

@application.route('/camview/<viewname>')
def camview(viewname):
    """Video streaming home page."""
    accountid=session.get('userid')
    print(accountid)
    dbs = dbops()

    # Get List of cameras for Views
    view=dbs.get_camViews_byname(viewname)
    print (view)
    camname_forview = []	
    if len(view) > 0:	
    	camids=view[0][2].split(":")

    	for camid in camids:
        	try:
            		camdetails = dbs.get_Camera_details(int(camid))
            		camname_forview.append(camdetails[0].upper())
        	except:
            		print("Error in Querying Camera details")

    #Get All View List for User
    camviewlist = dbs.get_camViews(accountid)
    listview = []
    if len(camviewlist) != 0:
        for camview in camviewlist:
            listview.append(camview[1])

    #List All Cameras
    camdlist = dbs.get_Camera_list_by_userid(str(accountid))
    camname = []

    for cam in camdlist:
        print(cam)
        camname.append(cam[1].upper())

    return render_template('viewcam.html',cameras=camname,camviews=listview,camlistforviews=camname_forview,NameView=viewname)

@application.route('/viewsinglecam/<camname>')
def viewsinglecam(camname):
    """Video streaming home page."""
    accountid=session.get('userid')
    print(accountid)
    dbs = dbops()
    cm=camname

    #Get All View List for User
    camviewlist = dbs.get_camViews(accountid)
    listview = []
    if len(camviewlist) != 0:
        for camview in camviewlist:
            listview.append(camview[1])

    #List All Cameras
    camdlist = dbs.get_Camera_list_by_userid(str(accountid))
    camname = []

    for cam in camdlist:
        print(cam)
        camname.append(cam[1].upper())

    return render_template('viewsinglecam.html',cameras=camname,camviews=listview,camnm=cm)

@application.route('/camplay/<viewname>')
def camplay(viewname):
    """Video streaming home page."""
    accountid=session.get('userid')
    print(accountid)
    dbs = dbops()


    # Get List of cameras for Views
    view=dbs.get_camViews_byname(viewname)
    camname_forview = []
    print (view)
    if len(view)>0:	
    	camids=view[0][2].split(":")

    	for camid in camids:
        	try:
            		camdetails = dbs.get_Camera_details(int(camid))
            		camname_forview.append(camdetails[0].upper())
        	except:
            		print("Error in Querying Camera details")

    #Get All View List for User
    camviewlist = dbs.get_camViews(accountid)
    listview = []
    if len(camviewlist) != 0:
        for camview in camviewlist:
            listview.append(camview[1])

    #List All Cameras
    camdlist = dbs.get_Camera_list_by_userid(str(accountid))
    allcamname = []

    for cam in camdlist:
        print(cam)
        allcamname.append(cam[1].upper())

    return render_template('playcam.html',cameras=allcamname,camviews=listview,camlistforviews=camname_forview,NameView=viewname)

@application.route('/searchvideo' , methods=['POST'])
def searchvideo():
    dbs = dbops()
    accountid=session.get('userid')
    userpath="static/videos/" +str(accountid)
    fileDir = os.path.dirname(os.path.realpath(__file__))
    newpath = os.path.join(fileDir, userpath)
    if os.path.exists(newpath):
        shutil.rmtree(newpath)

    #Get Details from screen
    settingdatails=dbs.get_settingsdetails()
    sdate=request.form['sdate']
    stime = request.form['stime']
    etime = request.form['etime']
    viewname=request.form['viewname']
    sdate=datetime.datetime.strptime(sdate,"%Y-%m-%d")
    year = str(sdate.strftime("%Y"))
    month = str(sdate.strftime("%m"))
    day = str(sdate.strftime("%d"))
    stime=stime.replace(":","")
    etime = etime.replace(":", "")

    #Generate Paths for video
    startrange=int(year+month+day+stime+"00")
    endrange=int(year+month+day+etime+"00")
    rootpathprimary=settingdatails[0][2]
    rootpathsecondary = settingdatails[0][3]
    rootpathtertiary = settingdatails[0][4]

    camviewlist = dbs.get_camViews(accountid)
    listview = []
    if len(camviewlist) != 0:
        for camview in camviewlist:
            listview.append(camview[1])

    # Get List of cameras for Views
    view = dbs.get_camViews_byname(viewname)
    print (view)
    camids = view[0][2].split(":")
    camname_forview = []
    video_forview = []

    for camid in camids:
        try:
            camdetails = dbs.get_Camera_details(int(camid))
            camname=camdetails[0].upper()
            camname_forview.append(camname)

            videoroot_primary= rootpathprimary +"/videos/" +camname+"/hist/" +str(year) +"/" + str(month)+"/" +str(day)
            videoroot_sec = rootpathsecondary + "/videos/" + camname + "/hist/" + str(year) + "/" + str(
                month) + "/" + str(day)
            videoroot_ter = rootpathtertiary + "/videos/" + camname + "/hist/" + str(year) + "/" + str(
                month) + "/" + str(day)

            if os.path.exists(videoroot_primary):
                videoroot = videoroot_primary
            elif os.path.exists(videoroot_sec):
                videoroot = videoroot_sec
            elif os.path.exists(videoroot_ter):
                videoroot = videoroot_ter

            generatevideos(camname,videoroot,startrange,endrange)
            finalvideo="/static/videos/" +str(accountid)+"/"+str(startrange)+"/"+camname+"/"+"show.mp4"
            video_forview.append(finalvideo)
        except Exception as e:
            print(e)
            print("Error in Querying Camera details")

    #Create tempvideo for display
    return render_template('playcam.html',cameras=camname,camviews=listview,camlistforviews=camname_forview,videolist=video_forview,NameView=viewname)

@application.route('/downloadvideo/<view>')
def downloadvideo(view):
    accountid=session.get('userid')
    userpath = "static/videos/" + str(accountid)
    zfilename=None
    if os.path.exists(userpath):
        dirs= os.listdir(userpath)
        zipdir=dirs[0]
        zippath=userpath + "/" +zipdir
        fileDir = os.path.dirname(os.path.realpath(__file__))
        newpath = os.path.join(fileDir, zippath)
        shutil.make_archive(newpath,'zip',newpath)
        zfilename=zipdir+".zip"
        return send_from_directory(directory=userpath, filename=zfilename,as_attachment=True)
    else:
        return redirect(url_for("camplay",viewname=view))


@application.route('/videofile_feed/<dirid>/<camname>')
def videofile_feed(dirid,camname):
    path="/static/videos/" +str(dirid) + "/" + str(camname) +"/show.mp4"
    return redirect(path)

def generatevideos(camname,videoroot,startrange,endrange):
    os.listdir(videoroot)
    onlyfiles = [f for f in os.listdir(videoroot) if os.path.isfile(os.path.join(videoroot, f))]
    matching_files=[]
    for f in onlyfiles:
        filname=f.split(".")[0]
        if int(filname) > int(startrange)  and int(filname) < int(endrange):
            file= os.path.join(videoroot,f)
            try:
                clip1 = VideoFileClip(file)
                matching_files.append(clip1)
            except:
                print("Bad file",file)

    final_clip = concatenate_videoclips(matching_files)

    #Path Generation ("/static/videos/<userid>/<searchdate>/<camname>/show.mp4)
    outpath = "./static/videos"
    if not os.path.exists(outpath):
        try:
            os.makedirs(outpath)

        except:
            print("unable to create directory",outpath)

    accountid = session.get('userid')
    outpath=outpath+"/"+str(accountid)
    if not os.path.exists(outpath):
        try:
            os.makedirs(outpath)
        except:
            print("unable to create directory", outpath)

    outpath=outpath + "/" +str(startrange).strip()
    if not os.path.exists(outpath):
        try:
            os.makedirs(outpath)
        except:
            print("unable to create directory", outpath)

    outpath = outpath + "/" +camname
    if not os.path.exists(outpath):
        try:
            os.makedirs(outpath)
        except:
            print("unable to create directory", outpath)


    try:
        outpath = outpath + "/show.mp4"
        final_clip.write_videofile(outpath)
    except:
        print ("unable to create outputvideo",outpath)
        outpath = None

@application.route('/viewshared')
def viewshared():
    """Video streaming home page."""
    accountid=session.get('userid')
    print(accountid)
    dbs = dbops()
    camdlistshared = dbs.get_Camera_list_sharedtome(str(accountid))
    camnameshared = []
    for cam in camdlistshared:
        print(cam[1])
        camnameshared.append(cam[1])
    return render_template('viewcamshared.html',sharedcameras=camnameshared)

@application.route('/addview')
def addview():
    """Video streaming home page."""
    accountid=session.get('userid')
    print(accountid)
    dbs = dbops()
    camdlist = dbs.get_Camera_list_by_userid(str(accountid))
    camname=[]
    for cam in camdlist:
        print(cam[1])
        camname.append(cam[1].upper())

    return render_template('addviews.html',cameras=camname)

@application.route('/savecamview',methods=['POST'] )
def savecamview():
    accountid = session.get('userid')
    dbs = dbops()
    viewname = request.form['name']
    cam1id=request.form['cam1']
    cam2id = request.form['cam2']
    cam3id = request.form['cam3']
    cam4id = request.form['cam4']
    cam5id = request.form['cam5']
    cam6id = request.form['cam6']


    try:
        cam1id = dbs.get_Camera_details_byname(cam1id)
        cam2id = dbs.get_Camera_details_byname(cam2id)
        cam3id = dbs.get_Camera_details_byname(cam3id)
        cam4id = dbs.get_Camera_details_byname(cam4id)
        cam5id = dbs.get_Camera_details_byname(cam5id)
        cam6id = dbs.get_Camera_details_byname(cam6id)
        camid=str(cam1id[4]) + ":" +str(cam2id[4]) + ":" +str(cam3id[4]) + ":" +str(cam4id[4]) + ":"+str(cam5id[4]) + ":"+str(cam6id[4])
        dbs.Add_camViews(viewname,camid,accountid)
        rd="/camview/"+viewname

        accountid = session.get('userid')
        print(accountid)
        dbs = dbops()
        camdlist = dbs.get_Camera_list_by_userid(str(accountid))
        camname = []
        for cam in camdlist:
            print(cam[1])
            camname.append(cam[1].upper())
        return render_template('addviews.html', cameras=camname)
    except Exception as e:
	print e
        return render_template("404.html",errormessage=e)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@application.route('/video_feed/<name>')
def video_feed(name):

    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera(name)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

application.secret_key = os.urandom(12)


#paint
app = Flask(__name__)


@application.route('/paintapp', methods=['GET', 'POST'])
def paintapp():
    if request.method == 'GET':
        return render_template("paint.html")
    if request.method == 'POST':
        filename = request.form['save_fname']
        data = request.form['save_cdata']
        canvas_image = request.form['save_image']
        conn = psycopg2.connect(database="paintmyown", user = "nidhin")
        cur = conn.cursor()
        cur.execute("INSERT INTO files (name, data, canvas_image) VALUES (%s, %s, %s)", [filename, data, canvas_image])
        conn.commit()
        conn.close()
        return redirect(url_for('save'))        
        
        
@application.route('/save', methods=['GET', 'POST'])
def save():
    conn = psycopg2.connect(database="paintmyown", user="nidhin")
    cur = conn.cursor()
    cur.execute("SELECT id, name, data, canvas_image from files")
    files = cur.fetchall()
    conn.close()
    return render_template("save.html", files = files )
    
@application.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template("search.html")
    if request.method == 'POST':
        filename = request.form['fname']
        conn = psycopg2.connect(database="paintmyown", user="nidhin")
        cur = conn.cursor()
        cur.execute("select id, name, data, canvas_image from files")
        files = cur.fetchall()
        conn.close()
        return render_template("search.html", files=files, filename=filename)
    

if __name__ == '__main__':
    application.run(host='0.0.0.0',port='5200', debug=True, threaded=True)
    #application.run(host='0.0.0.0')



