# Importing The Required Libaries
from django.shortcuts import render
import os.path
import urllib.request
from tkinter.filedialog import askdirectory
from django.views.decorators.csrf import csrf_exempt
import pyrebase
import pdfkit
import pandas as pd
import numpy as np
import excel2json
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import json
from pandas import read_csv,read_excel
from django.utils.datastructures import MultiValueDictKeyError
import firebase_admin
import pdfkit
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import js2py
import io





# Configuartion Data from firebase
config={
    "apiKey": "AIzaSyC47G0gYz3-QCSEfC0TiQdFqJowN8ELUiM",
    "authDomain": "mini-4fe76.firebaseapp.com",
    "databaseURL": "https://mini-4fe76-default-rtdb.firebaseio.com",
    "projectId": "mini-4fe76",
    "storageBucket": "mini-4fe76.appspot.com",
    "messagingSenderId": "637724120943",
    "appId": "1:637724120943:web:abca20a30e9c80a5b27a9a",
    "measurementId": "G-37KZ3XXN14"
    
  }
# For firebase configuration
firebase=pyrebase.initialize_app(config)

#Aucthication      
authe=firebase.auth()

#To store the datavalues in firebase[RealTime database]
db=firebase.database()

#To store the datavalues in firebase[Storage]
storage= firebase.storage()

#Retrive data from database
user1 =db.child("USERS").child("CONTACTS").get()

@csrf_exempt
def singIn(request):
    return render(request,"authication.html")
@csrf_exempt
def postsign(request):
    list1=[]
    email=request.POST.get('form3Example3')
    passw=request.POST.get('form3Example4')
    try:
         user=authe.sign_in_with_email_and_password(email,passw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"authication.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    try:
        for i in user1.each():
                list1.append(i.val())
        nam="Welcome {}".format(email)
        return render(request,'dashboard.html',{"e":nam,"allitems":list1})
    except Exception as e:
        nam="Welcome {}".format(email)
        return render(request,'dashboard.html',{"e":nam,"allitems":list1})
@csrf_exempt
def post_create(request):
    list1=[]
    if request.method == 'POST':
        file = request.FILES["data_file"]
        xlx =pd.read_excel(file)
        print(xlx.head())
        for i in range(len(xlx)):
            x=xlx.iloc[i]
            data={"Name":x[0],"Mail_Id":x[1],"Phone_No":int(x[2]),
            "CRE_Name":x[3],"Source":x[4],"Call_Status":x[5],"Budget":x[6],
            "State":x[7],"Location":x[8],"Remarks":x[9],"Status":x[10],"BDM_Name":x[11]}
            try:
                list1.clear()
                user1 =db.child("USERS").child("CONTACTS").get()
                for i in user1.each():
                    list1.append(i.val())
                phonenum=[]
                for t in list1:
                    phonenum.append(t.get("Phone_No"))
                    c=int(x[2])
                if c in phonenum:
                    n=x[0]
                    m=x[1]
                    cre=x[3]
                    sou=x[4]
                    cas=x[5]
                    bud=x[6]
                    s=x[7]
                    loc=x[8]
                    rem=x[9]
                    sta=x[10]
                    bdm=x[11]
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    duptex="{} Already Taken ".format(c)
                    return render(request,'dashboard2.html', {"already":c,"allitems":list1,"name":n,"em":m,"cre_name":cre,
                        "source":sou,"call_status":cas,"budget":bud,"state":s,"location":loc,"remark":rem,"status":sta,"BDM_Name":bdm,"dup":duptex})
                else:
                    db.child("USERS").child("CONTACTS").push(data)                      
            except:
                db.child("USERS").child("CONTACTS").push(data)
        user1 =db.child("USERS").child("CONTACTS").get()
        list1.clear()
        for i in user1.each():
            list1.append(i.val())    
            tex="{} Succussfully uploaded".format(file)
    print("#####################################################")
    return render(request,'dashboard.html', {"allitems":list1})
        
@csrf_exempt
def Download(request):
    list1=[]
    user1 =db.child("USERS").child("CONTACTS").get()
    list1.clear()
    for i in user1.each():
        list1.append(i.val())
    df = pd.DataFrame(data=list1)
    path = askdirectory()
    df.to_csv(os.path.join(path,r'student.csv'))
    return render(request,'dashboard.html', {"allitems":list1,"pdf1":df})

@csrf_exempt
def DownloadPdf(request):
    list1=[]
    user1 =db.child("USERS").child("CONTACTS").get()
    list1.clear()
    for i in user1.each():
        list1.append(i.val())
    df = pd.DataFrame(data=list1) 
    fig, ax =plt.subplots(figsize=(12,4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
    path = askdirectory()
    pp = PdfPages(os.path.join(path,r'table.pdf'))
    pp.savefig(fig, bbox_inches='tight')
    pp.close()


    return render(request,'dashboard.html', {"allitems":list1,"pdf1":df})

@csrf_exempt
def DuplicatesValues(request):
    a = request.POST.get('Name1')
    b = request.POST.get('Mail1')
    c = request.POST.get('Phone_No1')
    d = request.POST.get('Cre_Name')
    e = request.POST.get('Source')
    f = request.POST.get('Call_Status')
    g = request.POST.get('Budget')
    h = request.POST.get('State')
    i = request.POST.get('Location')
    j = request.POST.get('Remarks')
    k = request.POST.get('Status')
    l = request.POST.get("BDM_Name")
    data={"Name":a,"Mail_Id":b,"Phone_No":c,
            "CRE_Name":d,"Source":e,"Call_Status":f,"Budget":g,
            "State":h,"Location":i,"Remarks":j,"Status":k,"BDM_Name":l}
    list1=[]
    list1.clear()
    print("This is data:",data)
    db.child("USERS").child("CONTACTS").push(data)
    user1 =db.child("USERS").child("CONTACTS").get()
    for i in user1.each():
        list1.append(i.val())
    return render(request,'dashboard.html', {"allitems":list1})

        
        

                        
                        
                        
