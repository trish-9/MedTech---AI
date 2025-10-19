from flask import Flask , render_template , request , redirect , url_for  ,session,jsonify
#import twilio 
import sqlite3 as sq
#from twilio.rest import Client
import pandas as pd 
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import datetime
import random

#t = sq.connect("medtech1.db")


# Your Account SID and Auth Token from twilio.com/console
#account_sid = 'ACbb8c0db090449cb463e2b6e47dac9890'
#auth_token = '7de828614109f8367c172c5bbfc0b55d'
#client = Client(account_sid, auth_token)


app = Flask(__name__)
app.secret_key = "s3cr3t_k3y_123" 
@app.route('/')
def home():
    return render_template('index.html')
@app.route("/yug" , methods = ["GET","POST"])
def yug():
    
    if request.method == "POST":
       pat =  request.form.get("name")
       phon =  request.form.get("phone")
       date = request.form.get("appointmentDate")
       doc_type = request.form.get("doctorType")
       doc_name = request.form.get("doctorName")
       avs = request.form.get("slots")
       
       s = sq.connect("medtech6.db")
       #s.execute("Create table medtech6 (pat varchar(30) , phone varchar(30)  , doc_name varchar(30) , doc_type varchar(30) ,  date varchar(20), avs varchar(20));")
       #s.commit()
       
       
       #lient.messages.create(to='+91'+phon,from_=+18148882474, body=f"your slot is booked {str(ap)}")

       #p = pd.read_sql("select * from medtech2" , t)
       s = sq.connect("medtech6.db")
       p2 = pd.read_sql("select * from medtech6 ; " , s)
       if str(date) in list(p2["date"]) and str(avs) in list(p2["avs"]) and str(doc_type) in list(p2["doc_type"]) and str(doc_name) in list(p2["doc_name"]):
           s5 = 0 
           p1 = pd.read_sql(f"select avs from medtech6 where doc_type = '{str(doc_type)}' and avs = '{str(avs)}' ;", s)
           l = list(p1["avs"])
           l1 = ["09:00 AM","10:30 AM","12:30 AM","1:30 PM","02:00 PM","04:30 PM"]
           av_slot = []
           for a in l1:
               if a not in l:
                  av_slot.append(a)
           return render_template("yug.html" , solt = s5 , form_submitted = True, av_slot = av_slot)
       else:
           s5 = 1
          
           s.execute(f"insert into medtech6 (pat , phone , doc_name , doc_type , date , avs) values ('{pat}' , '{phon}' , '{doc_name}','{doc_type}' , '{date}' , '{avs}' ) ; ")
           s.commit()
           return render_template("yug.html" , solt = s5 ,form_submitted = True)
           
           
    return render_template("yug.html")

    
    
   
@app.route('/login',methods = ["GET","POST"])
def login():
    #s.execute("create table login (phone integer , password varchar(20) , check integer) ;")
    #s.commit()
    #s.execute("insert into login (phone , password, check) values (8000735960 , 'hax12@' ,  1")
    #s.commit()
    if request.method == "POST":
       phone = request.form.get("phone")
       password = request.form.get("password")
       s1 = sq.connect("medtech7.db")
       #s1.execute("create table login1 (phone varchar(20) , password varchar(20) , status integer ) ;")
       #s1.commit()
       #s1.execute("insert into login1 (phone , password, status) values ('8000735960' , 'hax12@' ,  1) ; ")
       #s1.commit()
       #s1.execute("insert into login1 (phone , password, status) values ('8875017836' , 'hax11@' ,  1) ; ")
       #s1.commit()
       l = pd.read_sql(f"select status from login1 where phone = '{phone}' and password = '{password}' ; " ,s1 )
       
       if l["status"].iloc[0] == 1:
          session["phone"] = str(phone)
          return redirect(url_for('dashboard'))
       else:
           return render_template("login.html" , status = l["status"].iloc[0])
            
       
    return render_template("login.html")
        
        
@app.route('/dashboard' , methods = ["GET","POST"])
def dashboard():
    
   
    phone = session.get("phone")
    print(f"Phone from session: {phone}")
   
    s2 = sq.connect("medtech6.db")
    q = pd.read_sql(f"select doc_type , date , avs  from medtech6  where phone = '{phone}'; " , s2)
    print(q)
    appointments = list(zip(q["doc_type"], q["date"], q["avs"]))
    return render_template("dashboard.html", appointments=appointments)
    
@app.route("/upload",methods = ["POST","GET"])
def dermato():
    if request.method == "POST":
       file = request.files['file']
       
       file.save("1.png")
       s = load_model("sk.h5")
       s.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
       l = ["Acne","Comedo","Clear"]


       c = cv2.imread("1.png")



       r = cv2.resize(c, (128, 128) )


       t = np.array(r) 

       t = t.astype('float32') / 255.0 

       t_input = np.expand_dims(t, axis=0)


       pr = s.predict(t_input)
       #pr = l[np.argmax(pr)]
       if l[np.argmax(pr)] == "Comedo":
           pr = f"The Disease is {l[np.argmax(pr)]} (Not 100% sure) , Please Book an Appointment with doctor . The Cure of this deases is this medications like salicylic acid and retinoids, a consistent cleansing and moisturizing routine, and avoiding harsh activities like squeezing. For stubborn cases, chemical peels or professional extraction"
       if l[np.argmax(pr)] == "Acne":
           pr = f"The Disease is {l[np.argmax(pr)]} (Not 100% sure) , Please Book an Appointment with doctor . The Cure of this deases is this Common treatments include topical creams and gels (like retinoids and benzoyl peroxide), oral medications (such as antibiotics, hormonal therapies, or isotretinoin for severe cases), and lifestyle adjustments like consistent cleansing and sun protection."
       if l[np.argmax(pr)] == "Clear":
           pr = f"The skin is {l[np.argmax(pr)]} . Stay Safe and Stay Clean"
 

       return render_template("dermato.html",result = pr)
    return render_template("dermato.html")
       
@app.route("/upload_xray",methods = ["POST","GET"])
def xray():
    if request.method == "POST":
       file = request.files['file']
       
       file.save("2.png")
       s = load_model("xray.h5")
       s.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
       l= ["factured","Non factureed"]

       c = cv2.imread("2.png")



       r = cv2.resize(c, (128, 128) )


       t = np.array(r) 

       t = t.astype('float32') / 255.0 

       t_input = np.expand_dims(t, axis=0)


       pr = s.predict(t_input)
       #pr = l[np.argmax(pr)]
       pri = l[np.argmax(pr)]
       pri = f"The Result of Prediction Image is {pri}"

       return render_template("xray.html",result1 = pri)
    return render_template("xray.html")   
 
@app.route('/ment')
def ment():
    return render_template("ment.html")
@app.route('/vit')
def vit():
    return render_template('vit.html')
vitals_data = [
    {"date": "2025-10-08", "bp": 120, "hr": 78, "spo2": 98},
    {"date": "2025-10-09", "bp": 124, "hr": 80, "spo2": 99},
    {"date": "2025-10-10", "bp": 118, "hr": 76, "spo2": 97},
    {"date": "2025-10-11", "bp": 130, "hr": 82, "spo2": 96},
    {"date": "2025-10-12", "bp": 122, "hr": 79, "spo2": 98},
]



@app.route('/api/vitals')
def get_vitals():
    return jsonify(vitals_data)

@app.route('/api/add', methods=['POST'])
def add_vital():
    data = request.get_json()
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "bp": data.get("bp"),
        "hr": data.get("hr"),
        "spo2": data.get("spo2")
    }
    vitals_data.append(entry)
    return jsonify({"message": "Vital added", "data": entry})

@app.route('/api/simulate')
def simulate_device():
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "bp": random.randint(115, 135),
        "hr": random.randint(70, 90),
        "spo2": random.randint(96, 99)
    }
    vitals_data.append(entry)
    return jsonify({"message": "Simulated device reading", "data": entry})

@app.route('/api/insight')
def get_insight():
    if not vitals_data:
        return jsonify({"score": 0, "advice": "No data"})
    last = vitals_data[-1]
    score = 100
    advice = []
    if last["bp"] > 130:
        score -= 10
        advice.append("Blood pressure is slightly high.")
    if last["hr"] > 85:
        score -= 5
        advice.append("Heart rate above normal range.")
    if last["spo2"] < 96:
        score -= 10
        advice.append("Oxygen level slightly low.")
    if not advice:
        advice.append("All vitals are stable ✅")
    return jsonify({"score": score, "advice": advice})

app.run(debug=True)
       
    