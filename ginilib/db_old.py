import sqlite3
#import pandas as pd
import xlsxwriter
from datetime import date, time, datetime
import os


class dbops:
    # def __init__(self):

    def getconnection(self):
        con = sqlite3.connect("users.sqlite3")
        return con

    def getid(self):
        con = self.getconnection()
        cur = self.con.execute("select max(id) from clients_visitor")
        for row in cur:
            x = row[0]
            print (x + 1)

        con.close()
        return x + 1

    def createAccount(self,fname,lname,email,pwd,cdate,ASDate,AEDAte,active):
        con = self.getconnection()
        QS = "insert into Account (firstname,lastname,email,pwd,Createdon,ActiveSDate,ActiveEDate,Active) values (?,?,?,?,?,?,?,?)"
        con.execute(QS, (fname,lname,email,pwd,cdate,ASDate,AEDAte,active))
        con.commit()
        con.close()

    def update_Account(self, id, field, value):
        con = self.getconnection()
        QS = "update Account set %s = ? WHERE id = ?" % (field)
        print (QS)
        con.execute(QS, (value, id))
        con.commit()
        con.close()

    def get_Account_details_byname(self, email):
        con = self.getconnection()
        # print(str(camname))
        column = 'email'
        QS = "select * from Account WHERE " + column + "='" + str(email) + "'"
        # print (QS)
        res = con.execute(QS)
        results = res.fetchall()
        # print(results)
        con.close()
        return results

    def Add_Camera(self, Cameraname, IP, Location, Type,userid):  # Type should be hhtp or rtsp or webcam
        con = self.getconnection()
        QS = "insert into clients_camera (CamName,IP,Location,Type,userid) values (?,?,?,?,?)"
        print (QS)
        con.execute(QS, (Cameraname, IP, Location, Type,userid))
        con.commit()
        con.close()

    def update_Camera(self, camid, field, value):
        con = self.getconnection()
        QS = "update clients_camera set %s = ? WHERE id = ?" % (field)
        print (QS)
        con.execute(QS, (value, camid))
        con.commit()
        con.close()

    def get_Camera_details(self, camid):
        con = self.getconnection()
        QS = "select * from clients_camera WHERE id =" + str(camid)
        # print (QS)
        res = con.execute(QS)
        results = []
        for rec in res:
            results.append(rec[1])
            results.append(rec[2])
            results.append(rec[3])
            results.append(rec[4])
        con.close()
        return results

    def get_Camera_details_byname(self, camname):
        con = self.getconnection()
        print(str(camname))
        camname=camname.strip()
        column = 'CamName'
        QS = "select * from clients_camera WHERE " + column + "='" + str(camname) + "'"
        # print (QS)
        res = con.execute(QS)
        results = []
        for rec in res:
            results.append(rec[1])
            results.append(rec[2])
            results.append(rec[3])
            results.append(rec[4])
            results.append(rec[0])
        # print(results)
        con.close()
        return results

    def get_Camera_list(self):
        con = self.getconnection()
        QS = "select * from clients_camera"
        # print (QS)
        res = con.execute(QS)
        results = res.fetchall()
        con.close()
        return results

    def get_Camera_list_by_userid(self,accountid):
        con = self.getconnection()
        QS = "select * from clients_camera" #where userid =" + str(accountid)  - Future implementation
        print (QS)
        res = con.execute(QS)
        print (res)
        results = res.fetchall()
        con.close()
        return results

    def get_Camera_list_sharedtome(self,userid):
        con = self.getconnection()
        QS = "select * from clients_camera where id IN (select camid from sharedcamera where sharedto = " + str(userid) +" )"
        print (QS)
        res = con.execute(QS)
        print (res)
        results = res.fetchall()
        con.close()
        return results

    def Delete_Camera(self, camid):
        con = self.getconnection()
        QS = "delete from clients_camera WHERE id =" + str(camid)
        #print (QS)
        res = self.con.execute(QS)
        con.commit()
        con.close()
        return res

    def Add_user(self, Username, address, mobile, Type, Nationalid):  # Type should be IP or NONIP
        con = self.getconnection()
        QS = "insert into User (Name,Address,mobile,Type,Nationalid) values (?,?,?,?,?)"
        #print (QS)
        con.execute(QS, (Username, address, mobile, Type, Nationalid))
        con.commit()
        con.close()

    def update_user(self, id, field, value):
        con = self.getconnection()
        QS = "update User set %s = ? WHERE id = ?" % (field)
        #print (QS)
        con.execute(QS, (value, id))
        con.commit()
        con.close()

    def get_user_details(self, id):
        con = self.getconnection()
        QS = "select * from TrackUser WHERE Nationalid =" + str(id)
        # print (QS)
        res = con.execute(QS)
        details = []
        for row in res:
            details.append(row[1])
            details.append(str(row[3]))
            details.append(row[4])
        con.close()
        return details

    def Delete_user(self, id):
        con = self.getconnection()
        QS = "delete from User WHERE id =" + str(id)
        #print (QS)
        res = self.con.execute(QS)
        con.commit()
        con.close()
        return res

    def Transactions(self,id,Userid,Name,Address,mobile,email,Nationalid,Status,Action,Location): 
        con = self.getconnection()
        QS = "insert into Transactions (Userid,Name,Address,mobile,email,Nationalid,Status,Action,Location) values (?,?,?,?,?,?,?,?,?)"
        val = [Userid,str(Name), str(Address), mobile, str(email), Nationalid,str(Status),str(Action),str(Location)]
        con.execute(QS, tuple(val))  
        con.commit()
        con.close()

    def update_Transactions(self, Userid,status,action,location):
	con = self.getconnection()
	QS = "update Transactions set  Status= ?,Action= ?,Location= ? WHERE Userid = ?" 
        print (QS)
        con.execute(QS, (status,action,location,Userid))
        con.commit()
        con.close()

    def get_Transactions(self):  
        con = self.getconnection()
	#"select * from clients_camera WHERE id =" + str(camid)
        QS ="""select * from Transactions WHERE Status ='Searching'"""
        res = con.execute(QS)
        results = res.fetchall()
        con.close()
        return  results

    def get_Transactions_id(self):  
        con = self.getconnection()
        QS = """select Userid from Transactions  WHERE Status = 'Searching'"""
        res = con.execute(QS)
        results = res.fetchall()
        con.close()
        return  results




    def Track_user(self, Username, address, mobile, email, Nationalid,
                   faceencode):  # Type should be employee or visitor
        con = self.getconnection()
        QS1 = "insert into TrackUser (Name,Address,mobile,email,Nationalid"
        QS2 = ") values (?,?,?,?,?"
        QS3 = ")"
        val = [str(Username), str(address), mobile, str(email), Nationalid]
        i = 1
        for x in (faceencode):
            QS1 = QS1 + "," + "en_" + str(i)
            QS2 = QS2 + "," + "?"
            val.append(float(x))
            i = i + 1
        QS = QS1 + QS2 + QS3
        con.execute(QS, tuple(val))  
        con.commit()
        con.close()

    def get_Track_user_list(self):  
        con = self.getconnection()
        QS = "select * from TrackUser"
        # print (QS)
        res = con.execute(QS)
        id = []
        name = []
        encode = []

        for rec in res:
            id.append(rec[5])
            name.append(str(rec[1]))
            encode.append(rec[6:134])
        con.close()
        return id, name, encode

    def get_Track_user_encoders(self):  # Type should be employee or visitor
        con = self.getconnection()
        i = 1
        limit = 128
        qs = "id"
        while i <= 128:
            qs = qs + "," + "en_" + str(i)
            i = i + 1

        QS = "select " + qs + " from TrackUser"
        # print (QS)
        res = con.execute(QS)
        res = res.fetchall()
        con.close()
        return res

    def Add_log(self, Nationalid):  # Type should be IP or NONIP
        con = self.getconnection()
        year = int(datetime.now().strftime("%Y"))
        month = int(datetime.now().strftime("%m"))
        day = int(datetime.now().strftime("%d"))
        intime = float(datetime.now().strftime("%H.%M"))
        outtime = float(datetime.now().strftime("%H.%M"))
        QS = "insert into att_log (imageid,yrs,mnt,days,Stime,etime) values (?,?,?,?,?,?)"
        print (QS)
        con.execute(QS, (int(Nationalid), year, month, day, intime, outtime))
        con.commit()
        con.close()

    def Add_camViews(self,name,camid,accountid):
        con = self.getconnection()
        QS = "insert into camviews (viewname,camid,Accountid) values (?,?,?)"
        con.execute(QS, (name,camid,int(accountid)))
        con.commit()
        con.close()

    def get_camViews(self,accountid):
        con = self.getconnection()
        QS = "select * from camviews where Accountid=" + str(accountid)
        res = con.execute(QS)
        res=res.fetchall()
        con.close()
        print (res)
        return res

    def get_camViews_byname(self,name):
        con = self.getconnection()
        column="viewname"
        names=name
        QS = "select * from camviews WHERE " + column + "='" +name + "'"

        #QS = "select * from camviews where viewname=" + str(name)
        res = con.execute(QS)
        res=res.fetchall()
        con.close()
        print (res)
        return res

    def edit_camViews(self,name,camid,accountid):
        con = self.getconnection()
        QS = "insert into camviews (name,camid,accountid) values (?,?,?)"
        con.execute(QS, (name,camid,int(accountid)))
        con.commit()
        con.close()

    def update_camViews(self, id, field, value):
        con = self.getconnection()
        QS = "update camviews set %s = ? WHERE id = ?" % (field)
        #print (QS)
        con.execute(QS, (value, id))
        con.commit()
        con.close()

    def Delete_camViews(self, viewid):
        con = self.getconnection()
        QS = "delete from camviews WHERE id =" + str(viewid)
        # print (QS)
        res = self.con.execute(QS)
        con.commit()
        con.close()
        return res

    def save_settings(self, name,primary,secondary,tertiory,duration):  # Type should be IP or NONIP
        con = self.getconnection()
        cond = self.getconnection()
        nm = name
        ps = primary
        ss = secondary
        ts = tertiory
        dur = duration
        try:
            QSD="delete from Settings"
            res = con.execute(QSD)
            con.commit()

        except Exception as e:
            print(e)
        QS = "insert into Settings (name,primarypath,secpath,thirdpath,duration) values (?,?,?,?,?)"
        print (QS)
        con.execute(QS, (nm,ps,ss,ts,dur))
        con.commit()
        con.close()

    def get_settingsdetails(self):
        con = self.getconnection()
        QS = "select * from Settings"
        res = con.execute(QS)
        res=res.fetchall()
        con.close()
        print (res)
        return res


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

        con = self.getconnection()
        QS = "select * from att_log  where yrs=" + str(year) + " and mnt=" + str(month) + " and (days BETWEEN " + str(
        startday - 1) + " and " + str(endday) + " ) group by imageid,days"

        QS1 = "select Nationalid,name from Trackuser group by Nationalid"
        df1 = pd.read_sql(QS1, con)
        res1 = con.execute(QS1)

        ids = df1["Nationalid"]

        print(ids)
        res = con.execute(QS)
        df = pd.read_sql(QS, con)
        days = range(startday, endday)
        print(ids)
        Attendence = []
        count = 0
        row = 7
        col = 2
        ws.write(row - 1, col - 2, "Id", bold_g)
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
            names = df1[df1["Nationalid"] == int(id)]["Name"]
            for name in names:
                print(name)
            for day in days:
                usersrecords = df[(df["imageid"] == id) & (df["days"] == day)]
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

        con.close()
        wb.close()
        return df
