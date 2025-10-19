from flask import Flask , render_template , request , redirect , url_for  ,session
import twilio 
import sqlite3 as sq
from twilio.rest import Client
import pandas as pd 
#t = sq.connect("medtech1.db")


# Your Account SID and Auth Token from twilio.com/console



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
       
       
       #s.execute("Create table medtech6 (pat varchar(30) , phone varchar(30)  , doc_name varchar(30) , doc_type varchar(30) ,  date varchar(20), avs varchar(20));")
       #s.commit()
       #s.execute(f"insert into medtech2 (patname , patphone , doctype , appodate , avaislot) values ('{pat}' , '{phon}' , '{doc_type}','{ap}' , '{avs}')")
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
       ##s1.execute("insert into login1 (phone , password, status) values ('8000735960' , 'hax12@' ,  1) ; ")
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
    

 
        
app.run(debug=True)
       

    
