# Importing all necessary libraries
import cv2
import os

from flask import session

from DBConnection import Db
# Read the video from specified path
import face_recognition
from email.mime import image
import os
import smtplib
from email.mime.text import MIMEText
staticpath=r"C:\Users\Octa\PycharmProjects\PEOPLE'S_VOICE\static\\"
urgmail="peoplesvoicewrs23@gmail.com"
urpassword="jxpizvygdahshrhf"
cam = cv2.VideoCapture(0)
currentframe = 0
l=[]

db = Db()
q = db.selectOne("select * from cctv")

from geopy.geocoders import Nominatim

cid=q['cctv_id']
# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")
# Latitude & Longitude input
Latitude = str(q['latitude'])
Longitude = str(q['longitude'])

print(Latitude,Longitude,"lllllllllllllllllllllllllllllllllll")


# location = geolocator.reverse(Latitude + "," + Longitude)

# Display
# k = str(location).split(',')
# place=q['location']

falsecase=[]
def check(i,types):
    if types == 'criminal':
        # print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",i)
        q1 = db.selectOne("select * from criminal,police where   criminal.criminal_id='" + str(i) + "' and  criminal.police_id=police.police_id")
        print(q1,"qqqqqqqqqqqqqqqqqqqqqqq")
        # cname=q1['name']
        if q1 is not None:
            cname = q1['name']

            # q2 = db.selectOne("select * from criminal_alert where criminal_id='" + str(i) + "' and date=curdate() and place='"+place+"' ")
            q2 = db.selectOne("select * from criminal_alert where criminal_id='" + str(i) + "' and date=curdate()  and type='cctv'  ")
            print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv",q2)
            if q2 is None:
                print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
                # db.insert("insert into `criminal_alert` values ( '','"+str(i)+"','"+place+"','0',curdate(),curtime());")
                db.insert("insert into `criminal_alert` (criminal_id,date,user_id,time,latitude,longitude,type) values ('"+str(i)+"',curdate(),'"+str(cid)+"',curtime(),'"+Latitude+"','"+Longitude+"','cctv');")
                r = db.selectOne("select * from cctv where cctv_id=1")
                try:
                    print("mddddddddddddd")
                    gmail = smtplib.SMTP('smtp.gmail.com', 587)

                    gmail.ehlo()

                    gmail.starttls()

                    gmail.login(urgmail, urpassword)

                except Exception as e:
                    print("Couldn't setup email!!" + str(e))

                # msg = MIMEText("Criminal "+cname+" located in " + str(k))
                loctn = str(r['latitude']),str(r['longitude'])
                 #msg = MIMEText("Criminal ")
                msg = MIMEText("Criminal " + cname + " located in " + str(loctn))

                msg['Subject'] = 'Verification'

                # msg['To'] = q1['email_id']
                msg['To'] = 'krishnendv6@gmail.com'

                # msg['From'] = urgmail
                msg['From'] = 'peoplesvoicewrs23@gmail.com'


                try:

                    gmail.send_message(msg)

                except Exception as e:

                    print("COULDN'T SEND EMAIL", str(e))
            else:
                db.update("update criminal_alert set latitude='"+Latitude+"',longitude='"+Longitude+"' where criminal_id='"+str(i)+"' and type='cctv' ")

                try:
                    print("mddddddddddddd")
                    gmail = smtplib.SMTP('smtp.gmail.com', 587)

                    gmail.ehlo()

                    gmail.starttls()

                    gmail.login(urgmail, urpassword)

                except Exception as e:
                    print("Couldn't setup email!!" + str(e))

                r = db.selectOne("select * from cctv where cctv_id=1")

                # msg = MIMEText("Criminal "+cname+" located in " + str(k))
                loctn = str(r['latitude'])+str(r['longitude'])

                msg = MIMEText("Criminal " + cname + " located in " + str(loctn))

                msg['Subject'] = 'Criminal alert'

                msg['To'] = q1['email_id']

                msg['From'] = urgmail

                try:

                    gmail.send_message(msg)

                except Exception as e:

                    print("COULDN'T SEND EMAIL", str(e))

    if str(types) == 'missingperson':
        print("nnnnnnnnnn",i)
        q1 = db.selectOne("select * from missing_person,police where   missing_person.missing_id='" + str(i) + "' and  missing_person.police_id=police.police_id")
        print(q1, "qqqqqqqqqqqqqqqqqqqqqqq")
        cname = q1['name']
        if q1 is not None:

            # q2 = db.selectOne("select * from missing_person_alert where missing_id='" + str(i) + "' and date=curdate() and place='" + place + "' ")
            q2 = db.selectOne("select * from missing_person_alert where missing_id='" + str(i) + "' and date=curdate() and latitude='"+Latitude+"' and longitude='"+Longitude+"' and type='cctv' ")
            print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv", q1)
            if q2 is None:
                print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
                # db.insert("insert into `missing_person_alert` values ( '','"+str(i)+"','"+place+"','0',curdate(),curtime());")
                db.insert("insert into `missing_person_alert` (missing_id,date,user_id,time,latitude,longitude,type) values ('"+str(i)+"',curdate(),'"+str(cid)+"',curtime(),'"+Latitude+"','"+Longitude+"','cctv');")

                try:
                    gmail = smtplib.SMTP('smtp.gmail.com', 587)

                    gmail.ehlo()

                    gmail.starttls()

                    gmail.login(urgmail, urpassword)

                except Exception as e:
                    print("Couldn't setup email!!" + str(e))

                r = db.selectOne("select * from cctv where cctv_id=1")

                # msg = MIMEText("Criminal "+cname+" located in " + str(k))
                loctn = str(r['latitude']) + str(r['longitude'])

                msg = MIMEText("Missing person " + cname + " located in " + str(loctn))

                msg['Subject'] = 'Verification'

                msg['To'] = q1['email_id']

                msg['From'] = urgmail

                try:

                    gmail.send_message(msg)

                except Exception as e:

                    print("COULDN'T SEND EMAIL", str(e))
            else:
                db.update("update missing_person_alert set date=curdate(),time=curtime() where missing_id='"+ str(i) +"'")


                    # "insert into `missing_person_alert` (,date,user_id,time,latitude,longitude,type) values ('" + str(
                    #     i) + "',curdate(),'" + str(cid) + "',curtime(),'" + Latitude + "','" + Longitude + "','cctv');")

                try:
                    gmail = smtplib.SMTP('smtp.gmail.com', 587)

                    gmail.ehlo()

                    gmail.starttls()

                    gmail.login(urgmail, urpassword)

                except Exception as e:
                    print("Couldn't setup email!!" + str(e))

                r = db.selectOne("select * from cctv where cctv_id=1")

                # msg = MIMEText("Criminal "+cname+" located in " + str(k))
                loctn = str(r['latitude']) + str(r['longitude'])

                msg = MIMEText("Missing person " + cname + " located in " + str(loctn))

                msg['Subject'] = 'Verification'

                msg['To'] = q1['email_id']

                msg['From'] = urgmail

                try:

                    gmail.send_message(msg)

                except Exception as e:

                    print("COULDN'T SEND EMAIL", str(e))


while (True):

    # reading from frame
    ret, frame = cam.read()

    if ret:
        # if video is still left continue creating images
        name =  'a.jpg'
        print('Creating...' + name)
        cv2.imwrite(r"C:\Users\Octa\PycharmProjects\PEOPLE'S_VOICE\static\\"+"a.jpg", frame)
        # writing the extracted images
        from PIL import Image

        Original_Image = Image.open(staticpath + "a.jpg")

        rotated_image2 = Original_Image.transpose(Image.ROTATE_270)
        rotated_image2.save(staticpath + "a_270.jpg")

        qry = "select * from criminal"
        db = Db()
        res = db.select(qry)
        print(res)
        if res is not None:

            known_faces = []
            userids = []
            person_name = []
            identified = []
            # if res is not None:
            for result in res:
                pic = result["image"]
                pname = pic.split("/")
                img = staticpath+"pic\\" + pname[len(pname) - 1]
                print(img)
                b_img = face_recognition.load_image_file(img)
                b_imgs = face_recognition.face_encodings(b_img)[0]
                known_faces.append(b_imgs)
                userids.append(result["criminal_id"])
                person_name.append(result["name"])
                print(str(len(known_faces)) + "done")

            # unknown_image = face_recognition.load_image_file(staticpath + "a.jpg")
            unknown_image = face_recognition.load_image_file(r"C:\Users\Octa\PycharmProjects\PEOPLE'S_VOICE\static\a.jpg")
            # unknown_image = face_recognition.load_image_file(staticpath + "a.jpg")
            unkonownpersons = face_recognition.face_encodings(unknown_image)
            print(len(unkonownpersons), "llllllllllllllllllllllll")
            if len(unkonownpersons) > 0:

                for i in range(0, len(unkonownpersons)):
                    h = unkonownpersons[i]

                    red = face_recognition.compare_faces(known_faces, h, tolerance=0.45)  # true,false,false,false]
                    print(red)
                    for i in range(0, len(red)):
                        if red[i] == True:
                            check(userids[i],"criminal")
                            identified.append(userids[i])
                        else:
                            print("false.....................................")
                            falsecase.append(userids[i])
            if len(res) == len(falsecase):
                print("ssssssssss")
                qry = "select * from missing_person"
                db = Db()
                res = db.select(qry)
                if res is not None:

                    known_faces = []
                    userids = []
                    person_name = []
                    identified = []
                    if res is not None:
                        for result in res:
                            pic = result["image"]
                            pname = pic.split("/")
                            img = staticpath + "pic\\" + pname[len(pname) - 1]
                            print(img)
                            b_img = face_recognition.load_image_file(img)
                            b_imgs = face_recognition.face_encodings(b_img)[0]
                            known_faces.append(b_imgs)
                            userids.append(result["missing_id"])
                            person_name.append(result["name"])
                            print(str(len(known_faces)) + "done")

                        unknown_image = face_recognition.load_image_file(staticpath + "a.jpg")
                        # unknown_image = face_recognition.load_image_file(staticpath + "a.jpg")
                        unkonownpersons = face_recognition.face_encodings(unknown_image)
                        print(len(unkonownpersons), "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
                        if len(unkonownpersons) > 0:

                            for i in range(0, len(unkonownpersons)):
                                h = unkonownpersons[i]

                                red = face_recognition.compare_faces(known_faces, h,
                                                                     tolerance=0.45)  # true,false,false,false]
                                print(red)
                                for i in range(0, len(red)):
                                    if red[i] == True:
                                        check(userids[i], "missingperson")
                                        identified.append(userids[i])
        else:

            qry = "select * from missing_person"
            db = Db()
            res = db.select(qry)
            if res is not None:

                known_faces = []
                userids = []
                person_name = []
                identified = []
                if res is not None:
                    for result in res:
                        pic = result["image"]
                        pname = pic.split("/")
                        img = staticpath + "pic\\" + pname[len(pname) - 1]
                        print(img)
                        b_img = face_recognition.load_image_file(img)
                        b_imgs = face_recognition.face_encodings(b_img)[0]
                        known_faces.append(b_imgs)
                        userids.append(result["missing_id"])
                        person_name.append(result["name"])
                        print(str(len(known_faces)) + "done")

                    unknown_image = face_recognition.load_image_file(staticpath + "a.jpg")
                    # unknown_image = face_recognition.load_image_file(staticpath + "a.jpg")
                    unkonownpersons = face_recognition.face_encodings(unknown_image)
                    print(len(unkonownpersons), "llllllllllllllllllllllll")
                    if len(unkonownpersons) > 0:

                        for i in range(0, len(unkonownpersons)):
                            h = unkonownpersons[i]

                            red = face_recognition.compare_faces(known_faces, h,
                                                                 tolerance=0.45)  # true,false,false,false]
                            print(red)
                            for i in range(0, len(red)):
                                if red[i] == True:
                                    check(userids[i],"missingperson")
                                    identified.append(userids[i])

                else:
                    pass

        currentframe += 1
    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
print(l)

