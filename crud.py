from ginilib.db import dbops 
import mysql.connector

df=dbops()
####################

# for Account table

#insert
#df.create_Account("manju","Raamanedi","manju@123.com","manju123","skjdfddhf","manju","8/3/2019","8/3/2019")

#delete
#df.delete_Account(4)


#update

#val = "prithviraj"
#id = 1
#df.update_Account(id,"firstname",val)

# read
#a=  df.get_Account_details_byname("manjku")
#print(a)


#print(df.getid())
############################

# for clients_camera table

#insert
df.Add_Camera(121,"webcam",0,"4","webcam",5)

#delete
df.delete_Camera(131)


#update
'''
val = "564325"
ID = 1
df.update_Camera(ID,"CAMNAME",val)
'''

# read

#print(df.get_Camera_list_by_userid(8564264))

#print(df.get_Camera_list())

#print(df.get_Camera_details_byname("134586385"))


#df.get_Camera_details(1)

#####################################

# for User table

#insert(need to change mobile data tupe int to bigint)
#df.Add_user(2,"manju","hddgsgf",90118130,"ffff",12345678,"adj/sd/sdl/x")

#delete
#df.Delete_user(1)

#update

#val = "Madhuri"
#ID = 1
#df.update_user(ID,"Name",val)

# read
#df.get_user_by_id(1)
##########################################

# for Track_user table

#insert
#faceencode = [-0.0998279824852943,0.0775062367320061,-0.0122326025739312,-0.0691219493746758,-0.113836117088795,-0.0475627705454826,-0.0116068068891764,-0.13699671626091,0.152581006288528,-0.0446843206882477,0.123945720493793,0.0132460668683052,-0.18607260286808,-0.100127883255482,0.00616332795470953,0.146506160497665,-0.114600643515587,-0.213876903057098,-0.142664700746536,-0.0622800104320049,-0.0594674870371819,-0.00538920518010855,0.0169198680669069,0.0138403987511992,-0.132922396063805,-0.299712806940079,-0.0431933589279652,-0.0732022598385811,0.0255327112972736,-0.0423230491578579,0.0272452384233475,0.122213594615459,-0.201128274202347,-0.0801390036940575,0.0718907490372658,0.0515621937811375,-0.0677919164299965,-0.0117741134017706,0.192723676562309,0.0156182767823339,-0.229959636926651,-0.002295165322721,0.0651178508996964,0.284096360206604,0.237398713827133,0.060736857354641,0.0197447370737791,-0.0740986093878746,0.0884937569499016,-0.265320479869843,0.0676309466362,0.114216290414333,0.0542950294911861,0.0414003916084766,0.0575569979846478,-0.177811414003372,0.0251672882586718,0.129495710134506,-0.20441198348999,0.00982375536113977,0.0455604866147041,-0.135835200548172,-0.0958878546953201,-0.0733795538544655,0.2709099650383,0.155385121703148,-0.0984925404191017,-0.0515388995409012,0.223131984472275,-0.103547103703022,-0.0415402129292488,-0.0393747389316559,-0.0775531977415085,-0.137344941496849,-0.275863468647003,0.0176164694130421,0.382108122110367,0.133477315306664,-0.191909283399582,0.0542044080793858,-0.0388992317020893,0.0652598291635513,0.0596376620233059,0.0522903501987457,-0.145594373345375,-0.042844470590353,-0.0244801882654428,-0.0259132869541645,0.178778514266014,0.00736488122493029,-0.0236250795423985,0.14460363984108,0.00553553085774183,-0.0322726294398308,0.0741259157657623,0.00274330680258572,-0.0735247135162354,-0.0292719528079033,-0.179155677556992,-0.0504145808517933,0.0432986877858639,-0.0800125524401665,0.0636484399437904,0.131539151072502,-0.167150855064392,0.167271926999092,0.042446430772543,-0.00430060736835003,0.0136022996157408,0.0235108025372028,0.0121496729552746,-0.061198003590107,0.0898254290223122,-0.207713410258293,0.272004187107086,0.154950574040413,-0.00689636217430234,0.190079018473625,0.0771173760294914,0.0751042366027832,-0.02033406868577,0.0255277212709188,-0.121118545532227,-0.0857484340667725,0.104016862809658,-0.00480305310338736,0.100485265254974,0.0878194719552994
#]
#df.create_track_user("Sridevi","dfssdfs",9845552513,"a@b.com","20074451",faceencode)

#delete
#df.Delete_track_user("8124108")

#update
#val = "suraj"
#ID = 1
#df.update_track_user(ID,"Name",val)

# read
#df.get_track_user_details(20074451)

#x = df.get_track_user_list()
#print(x)

#print(df.get_track_user_encoders())


#####################################################################

# for att_log table

#insert
#df.Add_log(564325,2109,7,1,20.1,30.3)

#delete
#df.Delete_att_log(1)


#update
#val = "2020"
#ID = 1
#df.update_att_log(ID,"Years",val)


# read
#a=df.get_att_log_by_id(1)
#print a
####################################################################

# for camViews table

#insert
#df.Add_camViews(0,"564","/usr/abd/ghj.jpg",3433289654)

#delete
#df.Delete_camViews(1)


#update
#val = "2020"
#ID = 1
#df.update_camViews(ID,"VIEWNAME",val)


# read
#print(df.get_camViews_byname("2020"))

# edit
#id= 2
#VIEWNAME = "12"
#CAMID= "jk"
#ACCOUNTID = 123
#print(df.edit_camViews(id, VIEWNAME, CAMID, ACCOUNTID))


#######################################################################

# for settings table

#insert
#df.Add_settings(13,"MySettings","/home/tensorlabs/videos" ,"/home/tensorlabs/videos","/home/tensorlabs/videos","45")

#delete
#df.Delete_Settings(1)
'''
#update
val = "2020"
ID = 1
df.update_Settings(ID,"name",val)
'''
# save
#print(df.save_settings("564325","/usr/abd/ghj.jpg","3433289654", "564325","/usr/abd/ghj.jpg"))

# read
#a=df.get_settingsdetails(1)
#print a
#####################################################################

# for shared_camera table(nw)

#insert
#df.create_shared_camera(23,564325,3,3)

#delete
#df.Delete_shared_camera(1)


#update
#val = "2020"
#ID = 1
#df.update_shared_camera(ID,"shared_from",val)


# read
#df.get_shared_camera(1)

############################################################################

# for camstatus table

#insert
#df.create_camstatus(1,"564325","/usr/abd/abcsdfdf.jpg","343334434354")

#delete
#df.Delete_camstatus(1)


#update
#val = "2020"
#ID = 1
#df.update_camstatus(ID,"CAMID",val)


# read
#a=df.get_camstatus(1)
#print a
#################################################################################

# for clients_visitorlog table

#insert>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>not workig>>>>>>>>>>>>>>>>>>>>>>>>>>>.

#df.create_clients_visitorlog(2,"564325","/usr/abd/ghj.jpg","3433289654","SDKLJJA")

#delete
#df.Delete_clients_visitorlog(1)


#update
#val = "2020"
#ID = 1
#df.update_clients_visitorlog(ID,"INTIME",val)


# read
#a=df.get_clients_visitorlog(1)
#print a
##################################################################################

# for sqlite_sequence table

#insert
#df.create_sqlite_sequence(2,"564325","/usr/abd/ghj.jpg")

#delete
#df.Delete_sqlite_sequence(1)

'''
#update
#val = "dfkjd"
#ID = 1
#df.update_sqlite_sequence(ID,"name",val)
'''

# read
#a=df.get_sqlite_sequence(1)
#print a

###########################################################################

# for sqlite_sequence table

#insert
#df.Transactions(1,564325,"abcd","gjkdhfsg","abcd@gmail.com",9011813019,123111,"searching","call","cam122")


#update
#val = "dfkjd"
#ID = 1
#df.update_Transactions(ID,"name",val)
# read
#a=df.get_Transactions()
#print a
# read_id
#df.get_Transactions_id(1)

#delete
#df.delete_Transactions_id(2)




