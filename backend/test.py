from ast import Not
from flask import Flask, redirect, url_for, render_template, request,jsonify,flash
from sqlalchemy import false
import json
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patient_progict1.db'
db = SQLAlchemy(app)
class Patient(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(50),nullable=false)
     age = db.Column(db.String(255))
     phone=db.Column(db.Integer)
     Albumin=db.Column(db.Integer)
     Platelets=db.Column(db.Integer)
     AFP=db.Column(db.Integer)
     ALP=db.Column(db.Integer)
     MCV=db.Column(db.Integer)
     Iron=db.Column(db.Integer)
    #  result1=db.Column(db.Integer)
     def __repr__(self):
        return f"""{self.name}-{self.age}-{self.phone}{self.AFP}{self.MCV}{self.Platelets}{self.Albumin}
        {self.ALP}{self.Iron}
        """
@app.route("/", methods=["POST", "GET"])
def home():
    admin_id ="0109200"
    # user_name="eman318"
    # id = request.form["id"]
    if request.method == "POST":
        if admin_id == request.form["id"] :
           return render_template("login1.html")  
        else:
            
             return redirect(url_for("get_pat",id=request.form["id"]))
          
                  
    return render_template("login.html")         
@app.route("/patient")
def get_id():
     patients=Patient.query.all()
     output=[]
     for patient in patients:
        pat_data= {'id':patient.id,'name':patient.name,'age':patient.age,
        'phone':patient.phone,'Albumin':patient.Albumin,'Platelets':patient.Platelets,'AFP':patient.AFP,
         'ALP':patient.ALP,'MCV':patient.MCV, 'Iron':patient.Iron}
        output.append(pat_data)
     return {"patients" :output}
       
@app.route("/patient/<id>")  
def get_pat(id): 
    patient=Patient.query.get(id)
    if patient is None:
         return{"error":"not found"}
    else:     
       return {'id':patient.id,'name':patient.name,'age':patient.age,
        'phone':patient.phone,'Albumin':patient.Albumin,'Platelets':patient.Platelets,'AFP':patient.AFP,
         'ALP':patient.ALP,'MCV':patient.MCV, 'Iron':patient.Iron}
@app.route("/patient", methods=["POST"])  
def add_pat():
    id=request.json['id']
    patient=Patient.query.get(id)
    if request.method == "POST":
       
        if patient is None:
                
                patient=Patient (id=request.json['id'],name=request.json['name'],age=request.json['age'],phone=request.json['phone'], 
                Albumin=request.json['Albumin'], Platelets=request.json['Platelets'],
               AFP=request.json['AFP'], ALP=request.json['ALP'],MCV=request.json['MCV'],
               Iron=request.json['Iron'] )
                db.session.add(patient) 
                db.session.commit()
                return{'id':patient.id,"massage":"the patient is added"}
        else:
             return{"error":"already  found"}
      
# @app.route("/addpatient/<id>", methods=["PUT"])  
# def add_patient(id):
#     patient=Patient.query.get(id)
#     name=request.json['name']
#     age=request.json['age']
#     phone=request.json['phone']
#     patient.name=name
#     patient.age=age
#     patient.phone=phone
#     db.session.commit() 
#     return{'id':patient.id,'name':patient.name,'age':patient.age,
#         'phone':patient.phone }
@app.route("/patient/<id>",methods=['DELETE'])  
def delete_pat(id): 
    patient=Patient.query.get(id)
    if patient is None:
         return{"error":"not found"}
    db.session.delete(patient)
    db.session.commit()
    return{"massage":"the patient is deleted"}
@app.route("/patient/<id>", methods=["PUT"])  
def updata_pat(id):
    patient=Patient.query.get(id)
    if patient is None:
         return{"error":"not found"}
    id=request.json['id']
    name=request.json['name']
    age=request.json['age']
    phone=request.json['phone']
    Albumin=request.json['Albumin']
    Platelets=request.json['Platelets']
    AFP=request.json['AFP']
    ALP=request.json['ALP']
    MCV=request.json['MCV']
    Iron=request.json['Iron']
    # patient.id=id
    patient.name=name
    patient.age=age
    patient.phone=phone
    patient.Albumin=Albumin
    patient.Platelets=Platelets
    patient.AFP=AFP
    patient.ALP=ALP
    patient.MCV=MCV
    patient.Iron=Iron
    # db.session.updata(drink) 
    db.session.commit()
    # return{'id':patient.id,'name':patient.name,'age':patient.age} 
    return {'id':patient.id,'name':patient.name,'age':patient.age,
        'phone':patient.phone,'Albumin':patient.Albumin,'Platelets':patient.Platelets,'AFP':patient.AFP,'ALP':patient.ALP,
        'MCV':patient.MCV,'Iron':patient.Iron
        ,"massage":"the patient is updated"}    
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,port=9000)