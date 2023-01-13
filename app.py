from flask import *
import mysql.connector


conn = mysql.connector.connect(host="localhost",password="7899",user="root",database="hospital")
cursor= conn.cursor()


app=Flask(__name__) 
app.secret_key = 'your secret key'


@app.route("/home")
def homepage():
    return render_template('home.html')

@app.route("/",methods=['post','get'])
def signin():
    msg=''
    if request.method == 'POST':
        L_email= request.form['login_email']
        L_pwd = request.form['login_pwd']
        cursor.execute( "SELECT * FROM users WHERE email=%s AND password=%s",(L_email,L_pwd))
        record=cursor.fetchone()
        if L_email=='' or L_pwd=='':
            msg='All Fields are Required'
            return render_template("signin.html",msg=msg)
        elif record:
            return redirect (url_for('homepage'))
        else:
            msg='Incorrect Username/Password'
    
    return render_template("signin.html",msg=msg)


@app.route("/signup",methods=['post','get'])
def signup():
    signup_msg=''
    if request.method=='POST':
        First_name=request.form['f_name']
        Last_name=request.form['l_name']
        Email=request.form['signup_email']
        Pwd=request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s",[Email])
        data=cursor.fetchone()
        if First_name=='' or Email==''or Pwd=='':
            signup_msg='All Fields are Required'
            return render_template("signup.html",msg=signup_msg)
        elif data:
            signup_msg='This User Already Exist'
        else :
            cursor.execute("INSERT INTO users (firstname,lastname,email,password) VALUES (%s,%s,%s,%s)",(First_name,Last_name,Email,Pwd))
            conn.commit()
            cursor.close()
            return redirect (url_for('homepage'))
        
    return render_template("signup.html",msg=signup_msg)

@app.route("/logout")
def logout():
    session.pop('loggin',None)
    session.pop('username',None)
    return redirect(url_for('signin'))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/appointment",methods=['post','get'])
def Appointment():
    msg=''
    if request.method=='POST':
        Fullname=request.form['fullname']
        Appointment_Email=request.form['A_email']
        Phonenumber=request.form['phonenumber']
        Message=request.form['message']
        if Fullname=='' or Appointment_Email==''or Phonenumber=='' or Message=='':
            msg='All Fields are Required'
            return render_template("appointment.html",msg=msg)
        else:
            cursor.execute("INSERT INTO appointment (fullname,email,phonenumber,message) VALUES (%s,%s,%s,%s)",(Fullname,Appointment_Email,Phonenumber,Message))
            conn.commit()
            cursor.close()
            msg='Successfully Appointed'
    return render_template('appointment.html',msg=msg)


if __name__=="__main__" :
    app.run(debug=True)