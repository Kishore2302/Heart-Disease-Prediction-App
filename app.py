from flask import Flask, render_template, request, url_for
# import model
import pickle
import numpy as np
import pymysql

import mysql.connector

gmail_list=[]
password_list=[]
gmail_list1=[]
password_list1=[]
import flask

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('register.html')
@app.route('/register',methods=['POST'])
def register():
    int_features2=[str(x) for x in request.form.values()]
    r1=int_features2[0]
    print(r1)
    r2=int_features2[1]
    print(r2)
    logu1=int_features2[0]
    passw1=int_features2[1]
#if int_features2[0]==12345 and int_features2[1]==12345:
    import mysql.connector
#open database connection
    mydb=mysql.connector.connect(host="localhost",user="kishore",passwd="kishore@2302",database="dddd")

#prepare a cursor object using cursor() method
    mycursor=mydb.cursor()
    mycursor.execute("SELECT user FROM user_register")
    result1=mycursor.fetchall()
   
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list1.append(str(row1[0]))
    print(gmail_list1)
    if logu1 in gmail_list1:
        return render_template('register.html',text="this Username is Already in Use")
    else:

       
#prepare SQL query to INSERT a record into the database.
                 sql="INSERT INTO user_register(user,password)VALUES(%s,%s)"
                 val=(r1,r2)
                 try:
#Execute the SQL command
                                    mycursor.execute(sql,val)
#commit your changes in the database
                                    mydb.commit()
                 except:
#Rollback in case there is any error
                                    mydb.rollback()
#disconnect from server
                 mydb.close()
                 return render_template('register.html',text="Successfully Registered")
                
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logedin',methods=['POST'])
def logedin():
    int_features3=[str(x) for x in request.form.values()]
    print(int_features3)
    logu=int_features3[0]
    passwd=int_features3[1]
    
    import mysql.connector
#open database connection
    mydb=mysql.connector.connect(host="localhost",user="kishore",passwd="kishore@2302",database="dddd")
 #prepare a cursor object using cursor() method
    mycursor=mydb.cursor()
    mycursor.execute("SELECT user FROM user_register")
    result1=mycursor.fetchall()
    
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list.append(str(row1[0]))
    print(gmail_list)
    
    mycursor1=mydb.cursor()
    mycursor1.execute("SELECT password FROM user_register")
    result2=mycursor1.fetchall()
    
    for row2 in result2:
                      print(row2)
                      print(row2[0])
                      password_list.append(str(row2[0]))
    print(password_list)
    print(gmail_list.index(logu))
    print(password_list.index(passwd))
    
    if gmail_list.index(logu)==password_list.index(passwd):
        return render_template('index.html')
    else:
        return render_template('login.html',text='Use Proper Username and Password')

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('index.html')

def pred_dis(d):
    data = np.array(d).reshape(1,9)
    clf = pickle.load(open("Heart Disease Logreg Model.pkl", "rb"))
    pred = clf.predict(data)

    return pred

@app.route("/result", methods = ["GET", "POST"])
def hello():
    if request.method == "POST":
        data = request.form.to_dict()
        data = list(data.values())
        data = list(map(int, data))
        result = pred_dis(data)

        if int(result) == 0:
            pred = "The patient has heart disease."
        else:
            pred = "The patient does not have heart disease."

        return render_template("result.html", pred=pred)


# @app.route("/", methods=["POST"])
# def hello():

#      # From html to .py 
#     if request.method == "POST":
#         # age = request.form["age"]
#         # cp = request.form["cp"]
#         # trestbps = request.form["trestbps"]
#         # chol = request.form["chol"]
#         # thalach = request.form["thalach"]
#         # exang = request.form["exang"]
#         # oldpeak = request.form["oldpeak"]
#         # ca = request.form["ca"]
#         # thal = request.form["thal"]

#         # data = [age, cpm, trestbps, chol, thalach, exang, oldpeak, ca, thal]
#         data = request.form.to_dict()
#         data = list(data.values())
#         data = list(map(int, data))

#         dis = pred_dis(data)
#         if int(dis) == 1:
#             pred = "You have heart disease."
#         else:
#             pred = "You do not have heart disease"
#         # global dis
#     # From .py to html
#         return render_template("index.html", pred=pred)

if __name__ == "__main__":
    app.run(debug=True)
