
import mysql.connector
from mysql.connector import Error,MySQLConnection
from datetime import datetime
from mysql.connector.cursor import MySQLCursorPrepared

class dbops:
	#def __init__(self):

	def getconnection(self):
		conn = mysql.connector.connect(host='localhost',
					database='AVIS_Face',
					user='root',
					password='Welcome123#',use_pure=True)
		if conn.is_connected():
			print('Connected to MySQL database')
		return conn
###############################################################################################################
# for Account table

	def getid(self):
		conn = self.getconnection()
		cursor = conn.cursor(prepared = True)
		cursor.execute("select max(id) from Account")
		cur = cursor.fetchall()
		for row in cur:
			x = row[0]
			print (x + 1)

		conn.close()
		return x + 1
	
	def create_Account(self,fname,lname,email,pwd,cdate,ASDate,AEDAte,active):
		conn = self.getconnection()
		QS = "insert into Account (firstname, lastname, email, pwd, Createdon, ActiveSDate, ActiveEDate, Active) VALUES(?,?,?,?,?,?,?,?)"
		cursor = conn.cursor(prepared = True)
		res= cursor.execute (QS, (fname,lname,email,pwd,cdate,ASDate,AEDAte,active))
		conn.commit()
		conn.close()
   
	def update_Account(self, id, field,value):
		conn = self.getconnection()
		QS = "update Account set %s = ? WHERE id= ?" % (field)
		print (QS)
		cursor = conn.cursor(prepared = True)
		res = cursor.execute(QS, (value, id))
		conn.commit()
		conn.close()
	
	def get_Account_details_byname(self, name):
		conn = self.getconnection()
		# print(str(camname))
        	column = 'email'
		QS = "select * from Account WHERE " + column + "='" + name + "'"
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS)
		result = cursor.fetchall()
		conn.close()
		print (result)
		return result

	def delete_Account(self, id):
		conn = self.getconnection()
		QS = "delete from Account WHERE id=" + str(id)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res
##################################################################################################################
#for Track user Trasaction
	def Transactions(self,id,Userid,Name,Address,mobile,email,Nationalid,Status,Action,Location): 
		conn = self.getconnection()
		QS = "insert into Transactions (Userid,Name,Address,email,mobile,National_ID,Status,Action,Location) values (?,?,?,?,?,?,?,?,?)"
		val = [Userid,str(Name), str(Address), mobile, str(email), Nationalid,str(Status),str(Action),str(Location)]
		cursor = conn.cursor(prepared = True)
		res = cursor.execute (QS, tuple(val))
		conn.commit()
		conn.close()

	def update_Transactions(self, Userid,status,action,location):
		conn = self.getconnection()
		QS = "update Transactions set  Status= ?,Action= ?,Location= ? WHERE Userid = ?" 
		print (QS)
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS, (status,action,location,Userid))
		conn.commit()
		conn.close()

	def get_Transactions(self):  
		conn = self.getconnection()
		#"select * from clients_camera WHERE id =" + str(camid)
		QS ="""select * from Transactions """ # WHERE Status ='Searching'"""
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		results =cursor.fetchall()
		conn.close()
		return  results

	def get_Transactions_id(self):  
		conn = self.getconnection()
		QS = """select Userid from Transactions  WHERE Status = 'Searching'"""
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		results = cursor.fetchall()
		conn.close()
		return  results


	def delete_Transactions_id(self, id):
		conn = self.getconnection()
		QS = "delete from Transactions WHERE id=" + str(id)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res
		
###################################################################################################################
# for clients_camera table

	def Add_Camera(self,Cameraname, IP, Location, Type,userid):
		conn = self.getconnection()
		QS = "insert into clients_camera(CAMNAME, IP, LOCATION, TYPE, USERID) values (?,?,?,?,?)"
		print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (Cameraname, IP, Location, Type,userid))
		conn.commit()
		conn.close()

	def update_Camera(self, camid, field, value):
		conn = self.getconnection()
		QS = "update clients_camera set %s = ? WHERE id= ?" % (field)
		print (QS)
		cursor = conn.cursor(prepared = True)
		result = cursor.execute(QS, (value, camid))
		conn.commit()
		conn.close()

	def get_Camera_details(self, camid):
		conn = self.getconnection()
		QS = "select * from clients_camera WHERE id=" + str(camid)
		# print (QS)
		cursor = conn.cursor(prepared = True)
		cursor.execute(QS)
		res = cursor.fetchall()
		results = []
		for rec in res:
			results.append(rec[1])
			results.append(rec[2])
			results.append(rec[3])
			results.append(rec[4])
		conn.close()
		print(results)
		return results

	def get_Camera_details_byname(self, camname):
		conn = self.getconnection()
		print(str(camname))
		camname=camname.strip()
		column = 'CamName'
		QS = "select * from clients_camera WHERE " + column + "='" + str(camname) + "'"
		# print (QS)
		cursor = conn.cursor(prepared = True)
		cursor.execute(QS)
		res = cursor.fetchall()
		results = []
		for rec in res:
			results.append(rec[1])
			results.append(rec[2])
			results.append(rec[3])
			results.append(rec[4])
			results.append(rec[0])
		# print(results)
		conn.close()
		print(results)
		return results


	def get_Camera_list(self):
		conn = self.getconnection()
		QS = "select * from clients_camera"
		cursor = conn.cursor(prepared=True)
		# print (QS)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.commit()
		conn.close()
		return res

	def get_Camera_list_by_userid(self, accountid):
		conn = self.getconnection()
		QS = "select * from clients_camera" #where USERid=" + str(id)  - Future implementation
		cursor = conn.cursor(prepared=True)
		# print (QS)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.commit()
		conn.close()
		print(res)
		return res

	def get_Camera_list_sharedtome(self,userid):
		conn = self.getconnection()
		QS = "select * from clients_camera where id IN (select camid from sharedcamera where 		sharedto = " + str(userid) +" )"
		print (QS)
                cursor = conn.cursor(prepared=True)
		# print (QS)
		cursor.execute(QS)
		results = cursor.fetchall()
		conn.close()
		return results

	def delete_Camera(self, camid):
		conn = self.getconnection()
		QS = "delete from clients_camera WHERE id=" + str(camid)
		print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		print (res)
		conn.commit()
		conn.close()
		return res


#########################################################################################################################
#  for User table
	
	def Add_user(self, id, Username, address, mobile, Type, Nationalid, Filepath):  # Type should be IP or NONIP
		conn = self.getconnection()
		QS = "insert into User (ID, Name, Address, Mobile, Type, National_ID, Filepath) values (?,?,?,?,?,?,?)"
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (id, Username, address, mobile, Type, Nationalid, Filepath))
		conn.commit()
		conn.close()
		return res

	def update_user(self, id, field, value):
		conn = self.getconnection()
		QS = "update User set %s = ? WHERE id= ?" % (field)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (value, id))
		conn.commit()
		conn.close()
		return res

	def get_user_details(self, id):
		conn = self.getconnection()
		QS = "select * from TrackUser WHERE Nationalid =" + str(id)  #Future implementation
		cursor = conn.cursor(prepared=True)
		# print (QS)
		cursor.execute(QS)
		res = cursor.fetchall()
		details = []
		for row in res:
                	details.append(row[1])
                	details.append(str(row[3]))
                	details.append(row[4])
		conn.commit()
		conn.close()
		print(res)
		return details 
	
	def Delete_user(self, id):
		conn = self.getconnection()
		QS = "delete from User WHERE id=" + str(id)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res
#########################################################################################

# for TrackUser table
	def Track_user(self,Username, address, mobile, email, Nationalid, faceencode):#Type should be employee or visitor
		conn = self.getconnection()
		QS1 = "insert into Track_user (Name,Address,mobile,email,National_ID"
		QS2 = ") values (?,?,?,?,?"
		QS3 = ")"
		# print (QS)
		# faceencode=str(faceencode).replace("  ",",")
		val = [str(Username), str(address), mobile, str(email), Nationalid]
		# print(faceencode)
		i = 1
		for x in (faceencode):
			QS1 = QS1 + "," + "en_" + str(i)
			QS2 = QS2 + "," + "?"
			val.append(float(x))
			i = i + 1
		QS = QS1 + QS2 + QS3
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, tuple(val))  
		conn.commit()
		conn.close()

  
	def get_Track_user_list(self):  # Type should be employee or visitor
		conn = self.getconnection()
		QS = "select * from Track_user"
		# print (QS)
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS)
		res = cursor.fetchall()
		id= []
		name = []
		encode = []

		for rec in res:
			id.append(rec[5])
			name.append(str(rec[1]))
			encode.append(rec[6:134])
		conn.commit()
		conn.close()
		print(res)
		return id, name, encode

	def get_track_user_encoders(self):  # Type should be employee or visitor
		conn = self.getconnection()
		i = 1
		limit = 128
		qs = "ID"
		while i <= 128:
			qs = qs + "," + "en_" + str(i)
			i = i + 1

		QS = "select " + qs + " from Track_user"
		# print (QS)
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.commit()
		conn.close()
		print(res)
		return res

	def get_track_user_details(self, id):
		conn = self.getconnection()
		QS = "select * from Track_user WHERE id=" + str(id)
		cursor = conn.cursor(prepared=True)
		# print (QS)
		cursor.execute(QS)
		res = cursor.fetchall()
		details = []
		for row in res:
			details.append(row[1])
			details.append(str(row[3]))
			details.append(row[4])
		conn.close()
		print(res)
		return details

	def Delete_track_user(self, National_id):
		conn = self.getconnection()
		QS = "delete from Track_user WHERE National_id=" + str(National_id)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res

	
	
	def update_track_user(self, id, field, value):
		conn = self.getconnection()
		QS = "update Track_user set %s = ? WHERE id= ?" % (field)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (value, id))
		conn.commit()
		conn.close()
		return res





######################################################################################################
# for att_log table

	def Add_log(self, Nationalid, year, month, day, intime, outtime):  # Type should be IP or NONIP
		conn = self.getconnection()
		year = int(datetime.now().strftime("%Y"))
		month = int(datetime.now().strftime("%m"))
		day = int(datetime.now().strftime("%d"))
		intime = float(datetime.now().strftime("%H.%M"))
		outtime = float(datetime.now().strftime("%H.%M"))
		QS = "insert into att_log (Image_ID,Years,Month,Days,Stime,Etime) values (?,?,?,?,?,?)"
		print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (int(Nationalid), year, month, day, intime, outtime))
		conn.commit()
		conn.close()
	
	def Delete_att_log(self, id):
		conn = self.getconnection()
		QS = "delete from att_log WHERE id=" + str(id)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res

	def update_att_log(self, id, field, value):
		conn = self.getconnection()
		QS = "update att_log set %s = ? WHERE id= ?" % (field)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (value, id))
		conn.commit()
		conn.close()
		return res

	def get_att_log_by_id(self, id):
		conn = self.getconnection()
		QS = "select * from att_log" #where id=" + str(id)  - Future implementation
		cursor = conn.cursor(prepared=True)
		# print (QS)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.commit()
		conn.close()
		print(res)
		return res

#############################################################################################################
#  for camviews table

	def Add_camViews(self,name,camid,accountid):
		conn = self.getconnection()
		QS = "insert into camviews (VIEWNAME,CAMID,ACCOUNTID) values (?,?,?)"
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (name,camid,int(accountid)))
		conn.commit()
		conn.close()

	def get_camViews(self,ACCOUNTID):
		conn = self.getconnection()
		QS = "select * from camviews where ACCOUNTID=" + str(ACCOUNTID)
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.commit()
		conn.close()
		print (res)
		return res

	def get_camViews_byname(self,VIEWNAME):
		conn = self.getconnection()
		column ="VIEWNAME"
		names = VIEWNAME
		QS = "select * from camviews WHERE " + column + "='" + VIEWNAME + "'"
		#QS = "select * from camviews where viewname=" + str(name)
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.commit()
		conn.close()
		print (res)
		return res

	def edit_camViews(self, id, VIEWNAME, CAMID, ACCOUNTID):
		conn = self.getconnection()
		QS = "insert into camviews (ID, VIEWNAME, CAMID, ACCOUNTID) values (?,?,?,?)"
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (id, VIEWNAME, CAMID, int(ACCOUNTID)))
		conn.commit()
		conn.close()

	def update_camViews(self, id, field, value):
		conn = self.getconnection()
		QS = "update camviews set %s = ? WHERE id= ?" % (field)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (value, id))
		conn.commit()
		conn.close()

	def Delete_camViews(self, CAMID):
		conn = self.getconnection()
		QS = "delete from camviews WHERE id=" + str(CAMID)
		# print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res

################################################################################################################################

# for settings table


	def Add_settings(self,id,name,primary,secondary,tertiory,duration):
		conn = self.getconnection()
		QS = "insert into Settings (ID, name, primarypath, secpath, thirdpath, duration) values (?,?,?,?,?,?)"
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (id,name,primary,secondary,tertiory,duration))
		conn.commit()
		conn.close()


	def save_settings(self, name,primary,secondary,tertiory,duration):  # Type should be IP or NONIP
		conn = self.getconnection()
		nm = name
		ps = primary
		ss = secondary
		ts = tertiory
		dur = duration
		try:
			QSD="delete from Settings"
			cursor = conn.cursor(prepared=True)
			res = cursor.execute(QSD)
			conn.commit()

		except Exception as e:
			print(e)
		QS = "insert into Settings (name,primarypath,secpath, thirdpath, duration) values (?,?,?,?,?)"
		print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (nm,ps,ss,ts,dur))
		conn.commit()
		conn.close()

	def get_settingsdetails(self):
		conn = self.getconnection()
		QS = "select * from Settings"
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.commit()
		conn.close()
		print (res)
		return res

	def update_Settings(self, id, field, value):
		conn = self.getconnection()
		QS = "update Settings set %s = ? WHERE id= ?" % (field)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS, (value, id))
		conn.commit()
		conn.close()

	def Delete_Settings(self, id):
		conn = self.getconnection()
		QS = "delete from Settings WHERE id=" + str(id)
		# print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res

###############################################################################################################
# for shared_camera table

    	
	def create_shared_camera(self,id, shared_from, shared_to, cam_ID):
		conn = self.getconnection()
		QS = "insert into shared_camera (ID,shared_from, shared_to, cam_ID) VALUES (?,?,?,?)"
		cursor = conn.cursor(prepared = True)
		res= cursor.execute (QS, (id, shared_from, shared_to, cam_ID))
		conn.commit()
		conn.close()
   
	def update_shared_camera(self, id, field,value):
		conn = self.getconnection()
		QS = "update shared_camera set %s = ? WHERE id= ?" % (field)
		print (QS)
		cursor = conn.cursor(prepared = True)
		res = cursor.execute(QS, (value, id))
		conn.commit()
		conn.close()
	
	def get_shared_camera(self, id):
		conn = self.getconnection()
		# print(str(shared_camera))
		column = 'ID'
		QS = "select * from shared_camera WHERE " + column + "='" + str(id) + "'"
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.close()
		print (res)
		return res

	def Delete_shared_camera(self, id):
		conn = self.getconnection()
		QS = "delete from shared_camera WHERE id=" + str(id)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res

#############################################################################################################

# for camstatus table

    	
	def create_camstatus (self,id, CAMID, CAMNAME, STATUS):
		conn = self.getconnection()
		QS = "insert into camstatus (ID, CAMID, CAMNAME, STATUS) VALUES (?,?,?,?)"
		cursor = conn.cursor(prepared = True)
		res= cursor.execute (QS, (id, CAMID, CAMNAME, STATUS))
		conn.commit()
		conn.close()
   
	def update_camstatus (self, id, field,value):
		conn = self.getconnection()
		QS = "update camstatus set %s = ? WHERE id= ?" % (field)
		print (QS)
		cursor = conn.cursor(prepared = True)
		res = cursor.execute(QS, (value, id))
		conn.commit()
		conn.close()
	
	def get_camstatus (self, id):
		conn = self.getconnection()
		# print(str(camstatus))
		column = 'ID'
		QS = "select * from camstatus WHERE " + column + "='" + str(id) + "'"
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.close()
		print (res)
		return res

	def Delete_camstatus (self, id):
		conn = self.getconnection()
		QS = "delete from camstatus WHERE id=" + str(id)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res
###############################################################################################################

# for clients_visitorlog table

    	
	def create_clients_visitorlog (self,id, INTIME, LOCATION, USER_ID, DATE):
		conn = self.getconnection()
		QS = "insert into clients_visitorlog (ID, INTIME, LOCATION, USER_ID, DATE) VALUES (?,?,?,?,?)"
		cursor = conn.cursor(prepared = True)
		res= cursor.execute (QS, (id, INTIME, LOCATION, USER_ID, DATE))
		conn.commit()
		conn.close()
   
	def update_clients_visitorlog (self, id, field,value):
		conn = self.getconnection()
		QS = "update clients_visitorlog set %s = ? WHERE id= ?" % (field)
		print (QS)
		cursor = conn.cursor(prepared = True)
		res = cursor.execute(QS, (value, id))
		conn.commit()
		conn.close()
	
	def get_clients_visitorlog (self, id):
		conn = self.getconnection()
		# print(str(camstatus))
		column = 'ID'
		QS = "select * from clients_visitorlog WHERE " + column + "='" + str(id) + "'"
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.close()
		print (res)
		return res

	def Delete_clients_visitorlog (self, id):
		conn = self.getconnection()
		QS = "delete from clients_visitorlog WHERE id=" + str(id)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res

#######################################################################################################################
# for sqlite_sequence

	def create_sqlite_sequence (self,id,name,seq):
		conn = self.getconnection()
		QS = "insert into sqlite_sequence (ID, name,seq) VALUES (?,?,?)"
		cursor = conn.cursor(prepared = True)
		res= cursor.execute (QS, (id,name,seq))
		conn.commit()
		conn.close()
   
	def update_sqlite_sequence (self, id, field,value):
		conn = self.getconnection()
		QS = "update sqlite_sequence set %s = ? WHERE id= ?" % (field)
		print (QS)
		cursor = conn.cursor(prepared = True)
		res = cursor.execute(QS, (value, id))
		conn.commit()
		conn.close()
	
	def get_sqlite_sequence (self, id):
		conn = self.getconnection()
		# print(str(camstatus))
		column = 'ID'
		QS = "select * from sqlite_sequence WHERE " + column + "='" + str(id) + "'"
		cursor = conn.cursor(prepared=True)
		cursor.execute(QS)
		res = cursor.fetchall()
		conn.close()
		print (res)
		return res

	def Delete_sqlite_sequence(self, id):
		conn = self.getconnection()
		QS = "delete from sqlite_sequence WHERE id=" + str(id)
		#print (QS)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		conn.commit()
		conn.close()
		return res
##################################################################################################

	def generate_report(self, startday, endday, month, year):
		fileDir = os.path.dirname(os.path.realpath(__file__))
		rep = os.path.join(fileDir, "/reports/Attendance.xlsx")
		print(rep)
		wb = xlsxwriter.Workbook("./reports/Attendance.xlsx")
		ws = wb.add_worksheet("atendance")
		ws.set_column('D:G', 12)
		ws.set_column('A:A', 10)
		ws.set_column('B:B', 18)
		ws.set_column('O:O', 13)
		ws.set_column('P:P', 13)
		merge_format = wb.add_format({

		'bold': 2,
		'border': 1,
		'align': 'center',
		'valign': 'vcenter',
		'fg_color': 'yellow'
		})

		bold = wb.add_format({

		'bold': 0,
		'border': 1,
		'fg_color': 'yellow'
		})

		bold_g = wb.add_format({

		'bold': 0,
		'border': 1,
		'fg_color': 'green'
		})

		row = 0
		col = 0

		ws.merge_range('D1:G2', 'Attendance Report', merge_format)
		ws.write(row + 2, col, "Start Day", bold)
		ws.write(row + 2, col + 1, startday)
		ws.write(row + 3, col, "End Day", bold)
		ws.write(row + 3, col + 1, endday)
		ws.write(row + 4, col, "Month", bold)
		ws.write(row + 4, col + 1, month)
		ws.write(row + 5, col, "Year", bold)
		ws.write(row + 5, col + 1, year)

		conn = self.getconnection()
		QS = "select * from att_log  where yrs=" + str(year) + " and mnt=" + str(month) + " and (days BETWEEN " + str(
		startday - 1) + " and " + str(endday) + " ) group by imageID,days"
		QS1 = "select NationalID,name from Trackuser group by NationalID"
		df1 = pd.read_sql(QS1, con)
		cursor = conn.cursor(prepared=True)
		res1 = cursor.execute(QS1)

		ids = df1["NationalID"]

		print(ids)
		cursor = conn.cursor(prepared=True)
		res = cursor.execute(QS)
		df = pd.read_sql(QS, con)
		days = range(startday, endday)
		print(IDs)
		Attendence = []
		count = 0
		row = 7
		col = 2
		ws.write(row - 1, col - 2, "ID", bold_g)
		ws.write(row - 1, col - 1, "Name", bold_g)

		for i in days:
			ws.write(row - 1, col + count, "day" + " " + str(i), bold_g)
			count += 1

		ws.write(row - 1, col + count, "Total Absent", bold_g)
		ws.write(row - 1, col + count + 1, "Total Present", bold_g)

		# n = 0
		row = 7
		for id in ids:

			present = 0
			absent = 0
			# col = col - 2
			useratt = []
			n = 0
			names = df1[df1["NationalID"] == int(id)]["Name"]
		for name in names:
			print(name)
		for day in days:
			usersrecords = df[(df["imageID"] == id) & (df["days"] == day)]
			if usersrecords.empty == True:
				status = 'A'
				print(status, id, day)
				absent += 1
			else:
				status = 'P'
				print(status, id, day)
				present += 1

		ws.write(row, col - 2, str(id))
		# ws.write(row, col-1, "name")
		ws.write(row, col + n, status)
		n += 1

		ws.write(row, col - 1, name)
		ws.write(row, col + n, absent)
		ws.write(row, col + n + 1, present)
		row += 1
		conn.commit()
		conn.close()
		wb.close()
		return df
