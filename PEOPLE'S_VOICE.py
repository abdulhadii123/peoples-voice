import smtplib
from email.mime.text import MIMEText

from flask import Flask,render_template,request,redirect,session,jsonify
from DBConnection import Db
import datetime
import random
app = Flask(__name__)
app.secret_key="abc"
# @app.route('/')
# def abc():
#     return render_template("login_index.html")


@app.route('/',methods=['get','post'])
def login():
    if request.method=="POST":
        u=request.form['textfield']
        p=request.form['textfield2']
        db=Db()
        res=db.selectOne("select * from login where USERNAME='"+u+"'and PASSWORD='"+p+"'")
        if res is not None:
            if res['USERTYPE']=='admin':
                session['lg']='lin'
                return '''<script>alert('Welcome!!');window.location="/adminhome"</script>'''

            if res['USERTYPE'] == 'police':
                session['lid']= res['LOGIN_ID']
                session['lg']='lin'
                return '''<script>alert('Welcome!!');window.location="/policehome"</script>'''

            else:
                return '''<script>alert('Invalid user!!');window.location="/"</script>'''
        else:
            return '''<script>alert('User not found!!');window.location="/"</script>'''
    else:
      return render_template("login_index.html")
@app.route('/logout')
def logout():
    session.clear()
    session['lg']=""
    return redirect('/')

@app.route('/adminhome')
def adminhome():
    return render_template("ADMIN/admin_home_index.html")


@app.route('/add_category',methods=['get','post'])
def add_category():
    if session['lg']=='lin':

        if request.method=="POST":
            c=request.form['select2']
            d=request.form['textarea']
            db=Db()
            res=db.selectOne("select * from crime_category WHERE crime_type='"+c+"' and description='"+d+"'")
            if res is not None:
                return '<script>alert("ALREADY EXIST");window.location="/adminhome"</script>'
            else:
                qry=db.selectOne("select * from crime_category where crime_type='"+c+"' ")
                if qry is not None:
                    return '<script>alert("Already added");window.location="/add_category"</script>'
                else:
                    db.insert("insert into crime_category(category_id,crime_type,description) VALUES (NULL,'"+c+"','"+d+"')")
                    return '<script>alert("ADDED SUCCESSFULLY");window.location="/adminhome"</script>'
        else:
          return render_template("ADMIN/add_category.html")
    else:
        return redirect('/')


@app.route('/view_category')
def view_category():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from crime_category")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/adminhome"</script>'
        else:
            res=db.select("select * from crime_category")
            return render_template("ADMIN/view_category.html",data=res)
    else:
        return redirect('/')


@app.route('/update_category/<cid>',methods=['get','post'])
def update_category(cid):
    if session['lg']=='lin':

        if request.method=="POST":
            c=request.form['select']
            d=request.form['textarea']
            db=Db()
            db.update("update crime_category set crime_type='"+c+"',description='"+d+"'where category_id='"+cid+"'")
            return '<script>alert("UPDATED SUCCESSFULLY");window.location="/view_category#f"</script>'
        else:
            db=Db()
            res=db.selectOne("select * from crime_category where category_id='"+cid+"'")
            return render_template("ADMIN/update_category.html",data=res)
    else:
        return redirect('/')


@app.route('/delete_category/<cid>')
def delete_category(cid):
    if session['lg']=='lin':

        db=Db()
        db.delete("delete from crime_category where category_id='"+cid+"'")
        return redirect('/view_category#f')
    else:
        return redirect('/')


@app.route('/add_emergency_contact',methods=['get','post'])
def add_emergency_contact():
    if session['lg']=='lin':

        if request.method=="POST":
            dep=request.form['textfield']
            con=request.form['textfield2']
            db=Db()
            qry=db.selectOne("select * from emergency_contact where dept='"+dep+"' and contact='"+con+"' ")
            if qry is not None:
                return '<script>alert("ALREADY ADDED");window.location="/add_emergency_contact"</script>'
            else:
                db.insert("insert into emergency_contact(em_id,dept,contact) values(NULL,'"+dep+"','"+con+"')")
                return '<script>alert("ADDED SUCCESSFULLY");window.location="/adminhome"</script>'
        else:
          return render_template("ADMIN/add_emergency_contact.html")
    else:
        return redirect('/')


@app.route('/police',methods=['get','post'])
def police():
    if session['lg']=='lin':

        if request.method=="POST":
            p=request.form['textfield']
            s=request.form['textfield2']
            lat=request.form['textfield4']
            lon=request.form['textfield5']
            sn=request.form['textfield6']
            e=request.form['textfield7']
            pn=request.form['textfield3']
            passwd=random.randint(0000,9999)
            db=Db()
            qry=db.selectOne("select * from login where USERNAME='"+e+"' ")
            if qry is not None:
                return '<script>alert("Email already exist!!");window.location="/police"</script>'
            else:
                res=db.insert("insert into login(LOGIN_ID,USERNAME,PASSWORD,USERTYPE) values(NULL,'"+e+"','"+str(passwd)+"','police')")
                db.insert("insert into police(police_id,location_name,place,phone,email_id,station_no,latitude,longitude)VALUES ('"+str(res)+"','"+s+"','"+p+"','"+pn+"','"+e+"','"+sn+"','"+lat+"','"+lon+"')")

                try:
                    gmail = smtplib.SMTP('smtp.gmail.com', 587)

                    gmail.ehlo()

                    gmail.starttls()

                    gmail.login('peoplesvoicewrs23@gmail.com',' jxpizvygdahshrhf')

                except Exception as e:
                    print("Couldn't setup email!!" + str(e))

                msg = MIMEText("Your Password is " + str(passwd))

                msg['Subject'] = 'Verification'

                msg['To'] = e

                msg['From'] = 'peoplesvoicewrs23@gmail.com'

                try:

                    gmail.send_message(msg)

                except Exception as e:

                    print("COULDN'T SEND EMAIL", str(e))

                return '<script>alert("ADDED SUCCESSFULLY");window.location="/adminhome"</script>'
        else:
            return render_template("ADMIN/police.html")
    else:
        return redirect('/')


@app.route('/VIEW_POLICE')
def VIEW_POLICE():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from police")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/adminhome"</script>'
        else:
            res=db.select("select * from police")
            return render_template("ADMIN/VIEW_POLICE.HTML",data=res)
    else:
        return redirect('/')


@app.route('/update_police/<pid>',methods=['get','post'])
def update_police(pid):
    if session['lg']=='lin':

        if request.method=="POST":
            p=request.form['textfield']
            s=request.form['textfield2']
            lat=request.form['textfield4']
            lon=request.form['textfield5']
            sn=request.form['textfield15']
            e=request.form['textfield6']
            pn=request.form['textfield7']
            db=Db()
            db.update("update police set location_name='"+s+"',place='"+p+"',phone='"+pn+"',email_id='"+e+"',station_no='"+sn+"',latitude='"+lat+"',longitude='"+lon+"'where police_id='"+pid+"'")
            return '<script>alert("UPDATED SUCCESSFULLY");window.location="/VIEW_POLICE#f"</script>'
        else:
            db=Db()
            res=db.selectOne("select * from police where police_id='"+pid+"'")
            return render_template("ADMIN/update_police.html",data=res)
    else:
        return redirect('/')


@app.route('/delete_police/<pid>')
def delete_police(pid):
    if session['lg']=='lin':

        db=Db()
        db.delete("delete from login where LOGIN_ID='"+pid+"'")
        db.delete("delete from police where police_id='"+pid+"'")
        return redirect('/VIEW_POLICE#f')
    else:
        return redirect('/')


@app.route('/view_complaint')
def view_complaint():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from complaint,user where complaint.user_id=user.user_id")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/adminhome"</script>'
        else:
            res=db.select("select * from complaint,user where complaint.user_id=user.user_id ")
            return render_template("ADMIN/view_complaint.html",data=res)
    else:
        return redirect('/')


@app.route('/reply/<cid>',methods=['get','post'])
def reply(cid):
    if session['lg']=='lin':

        if request.method=="POST":
            r=request.form['textarea']
            db=Db()
            db.update("update complaint set reply='"+r+"',reply_date=curdate() where complaint_id='"+cid+"'")
            return '<script>alert("REPLIED SUCCESSFULLY");window.location="/adminhome"</script>'
        else:
            return render_template("ADMIN/reply.html")
    else:
        return redirect('/')


@app.route('/view_criminal_alert')
def view_criminal_alert():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from criminal_alert,criminal,`user` where criminal_alert.criminal_id=criminal.criminal_id AND criminal_alert.user_id=user.user_id")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/adminhome"</script>'
        else:
            # res=db.select("select criminal.name as cn,criminal.image as cp,criminal.phone_no as cph,criminal.*,criminal_alert.*,`user`.* from criminal_alert,criminal,user where criminal_alert.criminal_id=criminal.criminal_id AND criminal_alert.user_id=user.user_id and criminal_alert.type='user' ")
            res=db.select("select criminal.name as cn,criminal.image as im,criminal_alert.*,user.name as un,user.phone_number as ph from criminal,criminal_alert,user where criminal_alert.criminal_id=criminal.criminal_id and criminal_alert.user_id=user.user_id union(select criminal.name as cn,criminal.image as im,criminal_alert.*,cctv.camera_no as un,cctv.location as ph from criminal,criminal_alert,cctv where criminal_alert.criminal_id=criminal.criminal_id and criminal_alert.user_id=cctv.cctv_id) ")
            return render_template("ADMIN/view_criminal_alert.html",data=res)
    else:
        return redirect('/')


@app.route('/view_feedback')
def view_feedback():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from feedback,user where feedback.user_id=user.user_id")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/adminhome"</script>'
        else:
            res=db.select("select * from feedback,user where feedback.user_id=user.user_id ")
            return render_template("ADMIN/VIEW_FEEDBACK.html",data=res)
    else:
        return redirect('/')


@app.route('/view_missing_person')
def view_missing_person():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from missing_person,police where missing_person.police_id=police.police_id")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/adminhome"</script>'
        else:
            res=db.select("select * from missing_person,police where missing_person.police_id=police.police_id")
            return render_template("ADMIN/view_missing_person.html",data=res)
    else:
        return redirect('/')


@app.route('/found_missing_person/<fid>')
def found_missing_person(fid):
    if session['lg']=='lin':

        db=Db()
        db.update("update missing_person set status='found' where missing_id='"+fid+"'")
        return '<script>alert("FOUND");window.location="/adminhome"</script>'
    else:
        return redirect('/')


@app.route('/notfound_missing_person/<fid>')
def notfound_missing_person(fid):
    if session['lg']=='lin':

        db=Db()
        db.update("update missing_person set status='not found' where missing_id='"+fid+"'")
        return '<script>alert("NOT FOUND");window.location="/adminhome"</script>'
    else:
        return redirect('/')


@app.route('/VIEW_MOST_WANTED')
def VIEW_MOST_WANTED():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from most_wanted_criminal,criminal where most_wanted_criminal.criminal_id=criminal.criminal_id ")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/adminhome"</script>'
        else:
            res=db.select("select * from most_wanted_criminal,criminal where most_wanted_criminal.criminal_id=criminal.criminal_id ")
            return render_template("ADMIN/VIEW_MOST_WANTED.HTML",data=res)
    else:
        return redirect('/')


@app.route('/add_cctv',methods=['get','post'])
def add_cctv():
    if session['lg']=='lin':

        if request.method=="POST":
            cam=request.form['textfield']
            pin=request.form['textfield2']
            loc=request.form['textfield3']
            lat=request.form['textfield4']
            lon=request.form['textfield5']
            db=Db()
            db.insert("insert into cctv(cctv_id,camera_no,pin_no,location,latitude,longitude) VALUES(NULL,'"+cam+"','"+pin+"','"+loc+"','"+lat+"','"+lon+"')")
            return '<script>alert("INSERT SUCCESSFUL");window.location="/adminhome"</script>'

        else:
            return render_template("ADMIN/add_cctv.html")
    else:
        return redirect('/')


@app.route('/view_cctv')
def view_cctv():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from cctv")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/adminhome"</script>'
        else:
            res=db.select("select * from cctv")
            return render_template("ADMIN/view_cctv.html",data=res)
    else:
        return redirect('/')


@app.route('/update_cctv/<cid>',methods=['get','post'])
def update_cctv(cid):
    if session['lg']=='lin':

        if request.method=="POST":
            cam=request.form['textfield']
            pin=request.form['textfield2']
            loc=request.form['textfield3']
            lat=request.form['textfield4']
            lon=request.form['textfield5']
            db=Db()
            db.update("update cctv set camera_no='"+cam+"',pin_no='"+pin+"',location='"+loc+"',latitude='"+lat+"',longitude='"+lon+"'where cctv_id='"+cid+"'")
            return '<script>alert("UPDATE SUCCESSFUL");window.location="/view_cctv#f"</script>'
        else:
            db=Db()
            res=db.selectOne("select * from cctv where cctv_id='"+cid+"'")
            return render_template("ADMIN/update_cctv.html",data=res)
    else:
        return redirect('/')


@app.route('/delete_cctv/<cid>')
def delete_cctv(cid):
    if session['lg']=='lin':

        db=Db()
        db.delete("delete from cctv where cctv_id='"+cid+"' ")
        return redirect('/view_cctv#f')
    else:
        return redirect('/')


############################police##############

@app.route('/policehome')
def policehome():
    return render_template("POLICE/police_home_index.html")


@app.route('/add_control',methods=['get','post'])
def add_control():
    if session['lg']=='lin':

        if request.method=="POST":
            e=request.form['textfield']
            vn=request.form['textfield2']
            loc=request.form['textfield3']
            ph=request.form['textfield4']
            passwd=random.randint(0000,9999)
            db=Db()
            qry=db.selectOne("select * from login where USERNAME='"+e+"'")
            if qry is not None:
                return '<script>alert("Email already exist");window.location="/add_control"</script>'
            else:
                qry1=db.selectOne("select * from control_room_vehicle where vehicle_no='"+vn+"' and police_id='"+str(session['lid'])+"' ")
                if qry1 is not None:
                    return '<script>alert("Already added");window.location="/add_control"</script>'
                else:
                    res=db.insert("insert into login(LOGIN_ID,USERNAME,PASSWORD,USERTYPE)values(NULL,'"+e+"','"+str(passwd)+"','control room')")
                    db.insert("insert into control_room_vehicle VALUES ('"+str(res)+"' ,'"+e+"','"+vn+"','"+loc+"','"+ph+"','"+str(session['lid'])+"')")
                try:
                    gmail = smtplib.SMTP('smtp.gmail.com', 587)

                    gmail.ehlo()

                    gmail.starttls()

                    gmail.login('peoplesvoicewrs23@gmail.com', ' jxpizvygdahshrhf')

                except Exception as e:
                    print("Couldn't setup email!!" + str(e))

                msg = MIMEText("Your Password is " + str(passwd))

                msg['Subject'] = 'Verification'

                msg['To'] = e

                msg['From'] = 'peoplesvoicewrs23@gmail.com'

                try:

                    gmail.send_message(msg)

                except Exception as e:

                    print("COULDN'T SEND EMAIL", str(e))

                return '<script>alert("ADDED SUCCESSFUL");window.location="/policehome"</script>'

        else:
            return render_template("POLICE/add_control.html")
    else:
        return redirect('/')


@app.route('/update_control/<cid>',methods=['get','post'])
def update_control(cid):
    if session['lg']=='lin':

        if request.method=="POST":
            vn=request.form['textfield']
            loc=request.form['textfield2']
            ph=request.form['textfield3']
            e=request.form['textfield4']
            db=Db()
            db.update("update control_room_vehicle set vehicle_no='"+vn+"',location='"+loc+"',phone='"+ph+"',email='"+e+"' where vehicle_no='"+cid+"'")
            return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_control#f"</script>'
        else:
            db=Db()
            res = db.selectOne("select * from control_room_vehicle where vehicle_id='" + cid + "'")
            return render_template("POLICE/update_control.html",data=res)
    else:
        return redirect('/')


@app.route('/view_control')
def view_control():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from control_room_vehicle where police_id='"+str(session['lid'])+"'")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/policehome"</script>'
        else:
            res=db.select("select * from control_room_vehicle where police_id='"+str(session['lid'])+"' ")
            return render_template("POLICE/view_control.html",data=res)
    else:
        return redirect('/')


@app.route('/delete_control/<cid>')
def delete_control(cid):
    if session['lg']=='lin':

        db=Db()
        db.delete("delete from control_room_vehicle where vehicle_id='" + cid + "' ")
        return '<script>alert("DELETE SUCCESSFUL");window.location="/view_control#f"</script>'
        return redirect('/view_control')
    else:
        return redirect('/')


@app.route('/add_criminal',methods=['get','post'])
def add_criminal():
    if session['lg']=='lin':

        if request.method=="POST":
            n=request.form['textfield']
            d=request.form['textfield2']
            g=request.form['RadioGroup1']
            p=request.form['textfield3']
            po=request.form['textfield5']
            pi=request.form['textfield4']
            di=request.form['select']
            im=request.files['fileField']
            ph=request.form['textfield6']
            date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            im.save(r"C:\Users\Octa\PycharmProjects\PEOPLE'S_VOICE\static\pic\\" +date+ '.jpg')
            w="/static/pic/"+date+'.jpg'
            db=Db()
            qry=db.selectOne("select * from criminal where `name`='"+n+"' and gender='"+g+"' and place='"+p+"' and post='"+po+"' and pin='"+pi+"' and district='"+d+"'  and police_id='"+str(session['lid'])+"'  ")
            if qry is not None:
                return '<script>alert("ALREADY ADDED");window.location="/add_criminal"</script>'
            else:
                res=db.insert("insert into criminal VALUES(NULL,'"+n+"','"+d+"','"+g+"','"+p+"','"+po+"','"+pi+"','"+di+"','"+str(w)+"','"+ph+"','"+str(session['lid'])+"')")
                db.insert("insert into most_wanted_criminal(most_id,criminal_id,status) VALUES (NULL,'"+str(res)+"','pending')")
                return '<script>alert("ADDED SUCCESSFUL");window.location="/policehome"</script>'
        else:
             return render_template("POLICE/add_criminal.html")
    else:
        return redirect('/')


@app.route('/view_criminal')
def view_criminal():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from criminal,police WHERE criminal. police_id='"+str(session['lid'])+"'")
        if ss is None:
            return'<script>alert("NOT AVAILABLE NOW");window.location="/policehome"</script>'
        else:
            res=db.select("select * from criminal,most_wanted_criminal where criminal.criminal_id=most_wanted_criminal.criminal_id AND criminal.police_id='"+str(session['lid'])+"'")
            return render_template("POLICE/view_criminal.html",data=res)
    else:
        return redirect('/')

@app.route('/set_most_wanted/<cid>')
def set_most_wanted(cid):
    if session['lg'] == 'lin':
        db=Db()
        db.update("update most_wanted_criminal set status='MOST WANTED' where most_wanted_criminal.criminal_id='"+cid+"'")
        return '<script>alert("UPDATED SUCCESSFULLY");window.location="/policehome"</script>'
    else:
        return redirect('/')


@app.route('/update_criminal/<cid>',methods=['get','post'])
def update_criminal(cid):
    if session['lg']=='lin':

        if request.method=="POST":
            n=request.form['textfield']
            d=request.form['textfield2']
            g=request.form['RadioGroup1']
            p=request.form['textfield3']
            po=request.form['textfield5']
            pi=request.form['textfield4']
            di=request.form['select']
            im=request.files['fileField']
            ph=request.form['textfield6']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            im.save(r"C:\Users\Octa\PycharmProjects\PEOPLE'S_VOICE\static\pic\\" + date + '.jpg')
            w = "/static/pic/" + date + '.jpg'
            if request.files!="":
                if im.filename!="":
                    db=Db()
                    db.update("update criminal set name='"+n+"',dob='"+d+"',gender='"+g+"',place='"+p+"',post='"+po+"',pin='"+pi+"',district='"+di+"',image='"+str(w)+"',phone_no='"+ph+"' where criminal_id='"+cid+"'")
                    return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_criminal#f"</script>'
                else:
                    db = Db()
                    db.update("update criminal set name='" + n + "',dob='" + d + "',gender='" + g + "',place='" + p + "',post='" + po + "',pin='" + pi + "',district='" + di + "',phone_no='"+ph+"' where criminal_id='"+cid+"'")
                    return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_criminal#f"</script>'
            else:
                db = Db()
                db.update("update criminal set name='" + n + "',dob='" + d + "',gender='" + g + "',place='" + p + "',post='" + po + "',pin='" + pi + "',district='" + di + "',phone_no='" + ph + "' where criminal_id='"+cid+"'")
                return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_criminal#f"</script>'
        else:
            db=Db()
            res = db.selectOne("select * from criminal where criminal_id='" + cid + "'")
            return render_template("POLICE/update_criminal.html",data=res)
    else:
        return redirect('/')


@app.route('/delete_criminal/<cid>')
def delete_criminal(cid):
    if session['lg']=='lin':

        db=Db()
        db.delete("delete from criminal where criminal_id='"+cid+"' ")
        return '<script>alert("DELETE SUCCESSFUL");window.location="/view_criminal#f"</script>'
    else:
        return redirect('/')


@app.route('/add_missing_person',methods=['get','post'])
def add_missing_person():
    if session['lg']=='lin':

        if request.method=="POST":
            n=request.form['textfield']
            a=request.form['textfield2']
            g=request.form['RadioGroup1']
            p=request.form['textfield3']
            md=request.form['textfield4']
            cn=request.form['textfield5']
            im=request.files['fileField']
            h=request.form['textfield6']
            we=request.form['textfield7']
            kl=request.form['textfield8']
            d=request.form['textfield9']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            im.save(r"C:\Users\Octa\PycharmProjects\PEOPLE'S_VOICE\static\pic\\" + date + '.jpg')
            w = "/static/pic/" + date + '.jpg'
            db=Db()
            qry=db.selectOne("select * from missing_person WHERE name='" + n + "'and age='" + a + "'and gender='" + g + "'and place='" + p + "'and missing_date='" + md + "' and contact_number='" + cn + "'and height='" + h + "'and weight='" + we + "'and known_language='" + kl + "'and disability='" + d + "' and status='pending'")
            if qry is not None:
                return '<script>alert("ALREADY ADDED ");window.location="/add_missing_person"</script>'
            else:
                db.insert("insert into missing_person VALUES (NULL ,'"+n+"','"+a+"','"+g+"','"+p+"','"+md+"','"+cn+"','"+str(w)+"','"+h+"','"+we+"','"+str(session['lid'])+"','"+kl+"','"+d+"','pending')")
                return '<script>alert("ADDED SUCCESSFUL");window.location="/policehome"</script>'
        else:
            return render_template("POLICE/add_missing_person.html")
    else:
        return redirect('/')


@app.route('/view_police_missing_person')
def view_police_missing_person():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from missing_person where police_id='"+str(session['lid'])+"'")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/policehome"</script>'
        else:
            res=db.select("select * from missing_person where police_id='"+str(session['lid'])+"'")
            return render_template("POLICE/view_police_missing_person.html",data=res)
    else:
        return redirect('/')


@app.route('/update_missing_person/<cid>',methods=['get','post'])
def update_missing_person(cid):
    if session['lg']=='lin':

        if request.method=="POST":
            n=request.form['textfield']
            a=request.form['textfield2']
            g=request.form['RadioGroup1']
            p=request.form['textfield3']
            md=request.form['textfield4']
            cn=request.form['textfield5']
            im=request.files['fileField']
            h=request.form['textfield6']
            we=request.form['textfield7']
            # pi=request.form['select']
            kl=request.form['textfield8']
            d=request.form['textfield9']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            im.save(r"C:\Users\Octa\PycharmProjects\PEOPLE'S_VOICE\static\pic\\" + date + '.jpg')
            w = "/static/pic/" + date + '.jpg'
            if request.files!="":
                if im.filename!="":
                    db=Db()
                    db.update("update missing_person set name='"+n+"',age='"+a+"',gender='"+g+"',place='"+p+"',missing_date='"+md+"',contact_number='"+cn+"',image='"+str(w)+"',height='"+h+"',weight='"+we+"',known_language='"+kl+"',disability='"+d+"' where missing_id='"+cid+"'")
                    return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_police_missing_person#f"</script>'
                else:
                    db = Db()
                    db.update("update missing_person set name='" + n + "',age='" + a + "',gender='" + g + "',place='" + p + "',missing_date='" + md + "',contact_number='" + cn + "',height='" + h + "',weight='" + we + "',known_language='" + kl + "',disability='" + d + "' where missing_id='"+cid+"'")
                    return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_police_missing_person#f"</script>'
            else:
                db=Db()
                db.update("update missing_person set name='"+n+"',age='"+a+"',gender='"+g+"',place='"+p+"',missing_date='"+md+"',contact_number='"+cn+"',height='"+h+"',weight='"+we+"',known_language='"+kl+"',disability='"+d+"' where missing_id='"+cid+"'")
                return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_police_missing_person#f"</script>'
        else:
            db=Db()
            res=db.selectOne("select * from missing_person where missing_id='"+cid+"'")
            return render_template("POLICE/update_missing_person.html",data=res)
    else:
        return redirect('/')


@app.route('/delete_missing_person/<cid>')
def delete_missing_person(cid):
    if session['lg']=='lin':

        db=Db()
        db.delete("delete from missing_person where missing_id='"+cid+"'")
        return redirect('/view_police_missing_person#f')
    else:
        return redirect('/')


@app.route('/add_most_wanted',methods=['get','post'])
def add_most_wanted():
    if session['lg']=='lin':

        if request.method=="POST":
            ci=request.form['select']
            # s=request.form['textfield']
            db=Db()
            db.insert("insert into most_wanted_criminal values(NULL ,'"+ci+"','pending')")
            return '<script>alert("ADD SUCCESSFULLY");window.location="/view_police_most_wanted"</script>'
        else:
            db=Db()
            res=db.select("select * from criminal where police_id='"+str(session['lid'])+"'")
            return render_template("POLICE/add_most_wanted.html",data=res)
    else:
        return redirect('/')


@app.route('/view_police_most_wanted')
def view_police_most_wanted():
    if session['lg']=='lin':

        db=Db()
        ss = db.selectOne("select * from most_wanted_criminal,criminal where most_wanted_criminal.criminal_id=criminal.criminal_id AND criminal.police_id='"+str(session['lid'])+"'")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/policehome"</script>'
        else:
            res=db.select("select * from most_wanted_criminal,criminal where most_wanted_criminal.criminal_id=criminal.criminal_id AND criminal.police_id='"+str(session['lid'])+"'")
            return render_template("POLICE/view_police_most_wanted.html",data=res)
    else:
        return redirect('/')


@app.route('/update_most_wanted/<mid>',methods=['get','post'])
def update_most_wanted(mid):
    if session['lg']=='lin':

        if request.method=="POST":
            ci=request.form['select']
            s=request.form['textfield']
            db=Db()
            db.update("update most_wanted_criminal set criminal_id='"+ci+"',status='"+s+"' where most_id='"+mid+"'")
            return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_police_most_wanted"</script>'
        else:
            db=Db()
            res=db.selectOne("select * from most_wanted_criminal where most_id='"+mid+"'")
            res1=db.select("select * from criminal where police_id='"+str(session['lid'])+"'")
            return render_template("POLICE/update_most_wanted.html",data=res,data1=res1)
    else:
        return redirect('/')


@app.route('/delete_most_wanted/<mid>')
def delete_most_wanted(mid):
    if session['lg']=='lin':

        db=Db()
        db.delete("delete from most_wanted_criminal where most_id='"+mid+"'")
        return '<script>alert("DELETED SUCCESSFUL");window.location="/view_police_most_wanted"</script>'
        return redirect('/view_police_most_wanted')
    else:
        return redirect('/')


@app.route('/add_record/<cid>',methods=['get','post'])
def add_record(cid):
    if session['lg']=='lin':

        if request.method=="POST":
            rec=request.files['fileField']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            rec.save(r"C:\Users\Octa\PycharmProjects\PEOPLE'S_VOICE\static\pic\\" + date + '.pdf')
            w = "/static/pic/" + date + '.pdf'
            # d=request.form['textfield2']
            cat=request.form['select']
            db=Db()
            db.insert("insert into crime_record VALUES (NULL ,'"+cid+"','"+str(w)+"',curdate(),'"+cat+"')")
            return '<script>alert("ADDED SUCCESSFUL");window.location="/view_criminal#f"</script>'
        else:
            db=Db()
            res1=db.select("select * from crime_category")
            return render_template("POLICE/add_record.html",data1=res1)
    else:
        return redirect('/')


@app.route('/view_record/<cid>')
def view_record(cid):
    if session['lg']=='lin':

        db=Db()
        ss=db.selectOne("select * from crime_category,crime_record where crime_record.category_id=crime_category.category_id AND crime_record.criminal_id='"+cid+"'")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/policehome"</script>'
        else:
            res=db.select("select * from crime_category,crime_record where crime_record.category_id=crime_category.category_id AND crime_record.criminal_id='"+cid+"'")
            return render_template("POLICE/view_record.html",data=res)
    else:
        return redirect('/')


@app.route('/update_record/<rid>',methods=['get','post'])
def update_record(rid):
    if session['lg']=='lin':

        if request.method=="POST":
            #ci=request.form['select2']
            cat = request.form['select']
            rec=request.files['fileField']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            rec.save(r"C:\Users\Octa\PycharmProjects\PEOPLE'S_VOICE\static\pic\\" + date + '.pdf')
            w = "/static/pic/" + date + '.pdf'
            if request.files!="":
                if rec.filename!="":
                    db=Db()
                    db.update("update crime_record set records='" + str(w) + "',category_id='" + cat + "' where record_id='"+rid+"'")
                    return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_criminal#f"</script>'
                else:
                    db = Db()
                    db.update("update crime_record set category_id='" + cat + "' where record_id='"+rid+"'")
                    return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_criminal#f"</script>'
            else:
                db=Db()
                db.update("update crime_record set category_id='" + cat + "' where record_id='"+rid+"'")
                return '<script>alert("UPDATED SUCCESSFUL");window.location="/view_criminal#f"</script>'
            ##d=request.form['textfield2']
        else:
            db=Db()
            res=db.selectOne("select * from crime_record where record_id='"+rid+"' ")
            res1=db.select("select * from crime_category ")
            return render_template("POLICE/update_record.html",data=res,data1=res1)
    else:
        return redirect('/')


@app.route('/delete_record/<rid>')
def delete_record(rid):
    if session['lg']=='lin':

        db=Db()
        db.delete("delete from crime_record where record_id='"+rid+"' ")
        return '<script>alert("DELETED SUCCESSFUL");window.location="/view_criminal#f"</script>'
        return redirect('/view_record')
    else:
        return redirect('/')


@app.route('/track_vehicle/<vid>')
def track_vehicle(vid):
    if session['lg']=='lin':

        db=Db()
        res=db.select("select * from track_vehicle where track_vehicle.vehicle_id='"+vid+"' ")
        return render_template("POLICE/track_vehicle.html",data=res)
    else:
        return redirect('/')


@app.route('/view_criminal_alert1')
def view_criminal_alert1():
    if session['lg']=='lin':

        db=Db()
        ss=db.selectOne("select * from criminal,criminal_alert where criminal.criminal_id=criminal_alert.criminal_id AND criminal.police_id='"+str(session['lid'])+"'")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/policehome"</script>'
        else:
            res=db.select("select criminal.*,user.name as un,user.phone_number as ph,criminal_alert.* from criminal,criminal_alert,`user` where criminal.criminal_id=criminal_alert.criminal_id and criminal_alert.user_id=user.user_id and criminal.police_id='"+str(session['lid'])+"'union (select criminal.*,cctv.camera_no as un,cctv.pin_no as ph,criminal_alert.* from criminal,criminal_alert,`cctv` where criminal_alert.criminal_id=criminal.criminal_id and criminal_alert.user_id=cctv.cctv_id and criminal.police_id='"+str(session['lid'])+"'  )")
            return render_template("POLICE/view_criminal_alert.html",data=res)
    else:
        return redirect('/')


@app.route('/view_missing_alert')
def view_missing_alert():
    if session['lg']=='lin':

        db=Db()
        ss=db.selectOne("select * from missing_person_alert,missing_person where missing_person_alert.missing_id=missing_person.missing_id and missing_person.police_id='"+str(session['lid'])+"'")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/policehome"</script>'
        else:
            res=db.select("select missing_person.*,missing_person_alert.*,user.name as un,user.phone_number as ph from missing_person_alert,missing_person,`user` where missing_person_alert.user_id=user.user_id and missing_person_alert.missing_id=missing_person.missing_id and missing_person.police_id='"+str(session['lid'])+"' union (select missing_person.*,missing_person_alert.*,cctv.camera_no as un,cctv.pin_no as ph from missing_person_alert,missing_person,`cctv` where missing_person_alert.user_id=cctv.cctv_id and missing_person_alert.missing_id=missing_person.missing_id and missing_person.police_id='"+str(session['lid'])+"' )")
            return render_template("POLICE/view_missing_alert.html",data=res)
    else:
        return redirect('/')


@app.route('/view_profile')
def view_profile():
    if session['lg']=='lin':

        db=Db()
        ss=db.selectOne("select * from police where police_id='"+str(session['lid'])+"'")
        if ss is None:
            return '<script>alert("NOT AVAILABLE NOW");window.location="/policehome"</script>'
        else:
            res=db.selectOne("select * from police where police_id='"+str(session['lid'])+"'")
            return render_template("POLICE/view_profile.html",data=res)
    else:
        return redirect('/')

 # ================================================================================================================================
 #                                    CONTROL ROOM --ANDROID
# =================================================================================================================================


@app.route('/and_login',methods=['post'])
def and_login():
    u=request.form['u']
    p=request.form['p']
    db=Db()
    res = db.selectOne("select * from login where USERNAME='" + u + "'and PASSWORD='" + p + "'")
    if res is not None:
        if res['USERTYPE']=='user':
            l=res['LOGIN_ID']
            qry=db.selectOne("select * from `user` where user_id='"+str(l)+"'")
            return jsonify(status="ok",type=res['USERTYPE'],lid=res['LOGIN_ID'],n=qry['name'],e=qry['email'],im=qry['image'])
        else:
            return jsonify(status="ok",type=res['USERTYPE'],lid=res['LOGIN_ID'])

    else:
        return jsonify(status="no")


@app.route('/and_view_emergency_alert2',methods=['post'])
def and_view_emergency_alert2():
    cid=request.form['id']
    lat=request.form['lati']
    log=request.form['logi']
    print("lat",lat)
    print("lo",log)
    db=Db()
    qry = "SELECT `user`.`user_id`,`user`.`name`,`emergency_alert`.`date`,emergency_alert.emergency_alert_id,`emergency_alert`.`time`,emergency_alert.status,`emergency_alert`.`latitude`,`emergency_alert`.`longitude`, (3959 * ACOS ( COS ( RADIANS('" + str(lat) + "') ) * COS( RADIANS( emergency_alert.latitude) ) * COS( RADIANS( emergency_alert.longitude ) - RADIANS('" + str(log) + "') ) + SIN ( RADIANS('" + str(lat) + "') ) * SIN( RADIANS( emergency_alert.latitude ) ))) AS user_distance FROM emergency_alert,user where emergency_alert.user_id=user.user_id  HAVING user_distance  < 6.2137"
    print(qry)
    res = db.select(qry)
    print(res)

    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")



@app.route('/and_view_criminal_alert2',methods=['post'])
def and_view_criminal_alert2():
    cid=request.form['id']
    lat=request.form['lati']
    log=request.form['longi']
    print(cid,"eeeeeeeeeeeeeee")
    db=Db()
    qry=db.selectOne("select * from control_room_vehicle where vehicle_id='"+cid+"'")
    p=qry['police_id']
    qry = "SELECT criminal.name as cn,criminal_alert.*,criminal.*,user.*,`criminal_alert`.`latitude`,`criminal_alert`.`longitude`, (3959 * ACOS ( COS ( RADIANS('" + str(lat) + "') ) * COS( RADIANS( criminal_alert.latitude) ) * COS( RADIANS( criminal_alert.longitude ) - RADIANS('" + str(log) + "') ) + SIN ( RADIANS('" + str(lat) + "') ) * SIN( RADIANS( criminal_alert.latitude ) ))) AS user_distance FROM criminal_alert,criminal,user where criminal_alert.user_id=user.user_id and criminal_alert.criminal_id=criminal.criminal_id and criminal.police_id='"+str(p)+"'  HAVING user_distance  < 6.2137"
    res=db.select(qry)
    # res=db.select("select criminal.name as cn,criminal_alert.*,criminal.*,user.*  from criminal_alert,criminal,`user` where criminal_alert.criminal_id=criminal.criminal_id AND `user`.user_id=criminal_alert.user_id and criminal.police_id='"+str(p)+"'")
    if len(res) > 0:
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")




@app.route('/and_status',methods=['post'])
def and_status():
    eid=request.form['eid']
    s=request.form['st']
    db=Db()
    db.update("update emergency_alert set status ='"+s+"' where emergency_alert_id='"+eid+"'")
    return jsonify(status="ok")

# ====================================================================================================================================
#                                                 USER MODULE--ANDROID
# =====================================================================================================================================

@app.route('/and_registration',methods=['post'])
def and_registration():
    n=request.form['n']
    p=request.form['p']
    pi=request.form['pi']
    ph=request.form['ph']
    e=request.form['e']
    aa=request.form['aa']
    pa=request.form['pa']
    d=request.form['d']
    g=request.form['g']
    pic=request.files['pic']
    date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    pic.save(r"C:\Users\Octa\PycharmProjects\PEOPLE'S_VOICE\static\pic\\" + date + '.jpg')
    w = "/static/pic/" + date + '.jpg'
    db=Db()
    qry1=db.selectOne("select * from login WHERE USERNAME='"+e+"' ")
    if qry1 is not None:
        return jsonify(status="already")
    else:
        qry=db.insert("insert into login(USERNAME,PASSWORD,USERTYPE) VALUES ('"+e+"','"+pa+"','user')")
        db.insert("insert into `user`(user_id,name,gender,place,pin,district,phone_number,email,aadhar_no,image) VALUES ('"+str(qry)+"','"+n+"','"+g+"','"+p+"','"+pi+"','"+d+"','"+ph+"','"+e+"','"+aa+"','"+str(w)+"')")
        return jsonify(status="ok")


@app.route('/and_view_profile',methods=['post'])
def and_view_profile():
    id=request.form['id']
    db=Db()
    res=db.selectOne("select * from `user` where user_id='"+id+"'")
    if len(res)>0:
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")




@app.route('/and_send_complaint',methods=['post'])
def and_send_complaint():
    db=Db()
    c=request.form['comp']
    id=request.form['id']
    db.insert("insert into complaint(complaint,complaint_date,reply,reply_date,user_id) VALUES ('"+c+"',curdate(),'pending','pending','"+id+"')")
    return jsonify(status="ok")





@app.route('/and_view_reply',methods=['post'])
def and_view_reply():
    db=Db()
    id=request.form['id']
    res=db.select("select * from complaint where user_id='"+id+"'")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")



@app.route('/and_send_feedback',methods=['post'])
def and_send_feedback():
    db=Db()
    c = request.form['fed']
    id = request.form['id']
    db.insert(
        "insert into feedback(feedback,date,user_id) VALUES ('" + c + "',curdate(),'" + id + "')")
    return jsonify(status="ok")


@app.route('/and_view_emergency_contact',methods=['post'])
def and_view_emergency_contact():
    db=Db()

    res=db.select("select * from emergency_contact")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")


@app.route('/and_delete',methods=['post'])
def and_delete():
    cid=request.form['cid']
    db=Db()
    db.delete("delete from complaint where complaint_id='"+cid+"'")
    return jsonify(status="ok")

@app.route('/and_view_missing_person',methods=['post'])
def and_view_missing_person():
    db=Db()

    res=db.select("select missing_person.image as cimg,missing_person.*,police.location_name as station_name from missing_person,police where missing_person.police_id=police.police_id and status!='found'")
    print(res)
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")



@app.route('/and_view_crimerecord',methods=['post'])
def and_view_crimerecord():
    db=Db()
    cid=request.form['cd']
    print(cid)

    res=db.select("select * from criminal,crime_record,crime_category where criminal.criminal_id=crime_record.criminal_id AND crime_category.category_id=crime_record.category_id and criminal.criminal_id='"+cid+"'")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")

@app.route('/and_view_crime_category',methods=['post'])
def and_view_crime_category():
    db=Db()
    res=db.select("select * from crime_category  ")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")


@app.route('/and_view_most_wanted',methods=['post'])
def and_view_most_wanted():
    db=Db()

    res=db.select("select criminal.image as cimg,criminal.*,most_wanted_criminal.* from criminal,most_wanted_criminal where criminal.criminal_id=most_wanted_criminal.criminal_id and most_wanted_criminal.status='MOST WANTED'")
    print(res)
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")



@app.route('/and_view_criminal',methods=['post'])
def and_view_criminal():
    db=Db()
    res = db.select("select criminal.image as cimg,criminal.* ,police.location_name as station_name from criminal,police where criminal.police_id=police.police_id")
    print(res)
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")



@app.route('/and_missing_person_alert',methods=['post'])
def and_missing_person_alert():
    db = Db()
    c = request.form['mid']
    id = request.form['id']
    lati = request.form['lati']
    longi = request.form['longi']
    qry=db.selectOne("select * from missing_person_alert where date=curdate() and missing_id='"+c+"' and user_id='"+id+"' and type='user' ")
    if qry is not None:
        aid=qry['alert_id']
        db.update("update missing_person_alert set latitude='"+lati+"',longitude='"+longi+"' where alert_id='"+str(aid)+"'  ")
        return jsonify(status="up")

    else:
        db.insert("insert into missing_person_alert(missing_id,date,user_id,time,latitude,longitude,type) VALUES ('" + c + "',curdate(),'"+id+"',curtime(),'"+lati+"','"+longi+"','user')")
        return jsonify(status="ok")




@app.route('/and_criminal_alert',methods=['post'])
def and_criminal_alert():
    db=Db()
    c = request.form['cid']
    id = request.form['id']
    lati = request.form['lati']
    longi = request.form['longi']
    qry=db.selectOne("select * from criminal_alert where date=curdate() and user_id='"+id+"' and criminal_id='"+c+"' and type='user'")
    if qry is not None:
        cid=qry['criminal_alert_id']
        db.update("update criminal_alert set latitude='"+lati+"',longitude='"+longi+"' where criminal_alert_id='"+str(cid)+"' ")
        return jsonify(status="up")

    else:
       db.insert( "insert into criminal_alert(criminal_id,date,user_id,time,latitude,longitude,type) VALUES ('" + c + "',curdate(),'" + id + "',curtime(),'"+lati+"','"+longi+"','user')")
       return jsonify(status="ok")



@app.route('/and_location_update',methods=['post'])
def and_locateion_update():
    lati=request.form['lati']
    longi=request.form['logi']
    pl=request.form['pl']
    cid=request.form['id']
    db=Db()
    res=db.selectOne("select * from track_vehicle where vehicle_id='"+cid+"'")
    if res is not None:
        db.update("update track_vehicle set location_name='"+pl+"',latitude='"+lati+"',longitude='"+longi+"' where vehicle_id='"+cid+"' ")
        return jsonify(status="ok")
    else:
        db.insert("insert into track_vehicle(vehicle_id,location_name,latitude,longitude) VALUES ('"+cid+"','"+pl+"','"+lati+"','"+longi+"')")
        return jsonify(status="ok")


@app.route('/emergency_request', methods=['POST'])
def emergency_request():
    lati = request.form['lati']
    longi = request.form['longi']
    cid = request.form['id']
    db = Db()
    qry=db.selectOne("select * from emergency_alert where status='pending' and date=curdate() and user_id='"+cid+"' ")
    if qry is not None:
        return jsonify(status="alreadysend")
    else:
        db.insert("insert into emergency_alert(user_id,date,time,latitude,longitude,status)VALUES ('"+cid+"',curdate(),curtime(),'"+lati+"','"+longi+"','pending')")
        return jsonify(status="ok")


@app.route('/and_forgot_password',methods=['post'])
def and_forgot_password():
    db=Db()
    e=request.form['u']
    res=db.selectOne("select * from login where username='"+e+"' and USERTYPE='user'")
    if res is not None:
        from email.mime import image
        import os
        import smtplib
        from email.mime.text import MIMEText
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)

            gmail.ehlo()

            gmail.starttls()

            gmail.login('wiras2764@gmail.com', 'opmcuhilocnhabea')

        except Exception as e:
            print("Couldn't setup email!!" + str(e))

        msg = MIMEText("Your Password is " + str(res['PASSWORD']))

        msg['Subject'] = 'Verification'

        msg['To'] = e

        msg['From'] = 'wiras2764@gmail.com'

        try:

            gmail.send_message(msg)

        except Exception as e:

            print("COULDN'T SEND EMAIL", str(e))
        return jsonify(status='ok')

    else:
        return jsonify(status='')

if __name__ == '__main__':
    app.run(port=4000,debug=True,host="0.0.0.0")
