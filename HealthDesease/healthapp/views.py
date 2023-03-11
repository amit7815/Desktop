from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from .forms import DoctorForm
from .models import *
from django.contrib.auth import authenticate, login, logout
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from scipy.stats import mode
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def Home(request):
    return render(request,'home.html')

def Admin_Home(request):
    dis = Search_Data.objects.all()
    pat = Patient.objects.all()
    doc = Doctor.objects.all()
    feed = Feedback.objects.all()

    d = {'dis':dis.count(),'pat':pat.count(),'doc':doc.count(),'feed':feed.count()}
    return render(request,'admin_home.html',d)

@login_required(login_url="login")
def assign_status(request,pid):
    doctor = Doctor.objects.get(id=pid)
    if doctor.status == 1:
        doctor.status = 2
        messages.success(request, 'Selected doctor are successfully withdraw his approval.')
    else:
        doctor.status = 1
        messages.success(request, 'Selected doctor are successfully approved.')
    doctor.save()
    return redirect('view_doctor')

@login_required(login_url="login")
def Patient_Home(request):
    return render(request,'patient_home.html')

@login_required(login_url="login")
def Doctor_Home(request):
    return render(request,'doctor_home.html')

def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            try:
                sign = Patient.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "pat1"
                messages.success(request,"login successfully")
                return render(request,"home.html")
            else:
                pure=False
                try:
                    pure = Doctor.objects.get(status=1,user=user)
                except:
                    pass
                if pure:
                    login(request, user)
                    error = "pat2"
                    messages.success(request,"login successfully")
                    return render(request,"home.html")
                else:
                    login(request, user)
                    error="notmember"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'login.html', d)

def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            error="pat"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'admin_login.html', d)

def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        # d = request.POST['dob']
        con = request.POST['contact']
        add = request.POST['add']
        type = request.POST['type']
        # im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        if type == "Patient":
            Patient.objects.create(user=user,contact=con,address=add)
        else:
            Doctor.objects.create(user=user,contact=con,address=add,status=2)
        error = "create"
        messages.success(request, 'You have registered successfull')

        return render(request,'home.html')
    d = {'error':error}
    return render(request,'register.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

import smtplib

from email.mime.text import MIMEText
def send_email(addo,patient,disease=''):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    s.login("yadavamit14801@gmail.com","zsisxdavycstplqz")

    sender = 'yadavamit14801@gmail.com' 
    rec = 'prince14801@gmail.com'


    # breakpoint()
    if disease == '':
        msg = MIMEText('Patient' +patient.user.get_full_name() + 'is in stage 3 please contact on this number as soon as possible' + patient.contact )
    else:
        msg = MIMEText('Patient '+ patient.user.get_full_name() +' is unhealthy having symptoms of ' + disease +" please contact on this number as soon as possible " + patient.contact )
    msg['Subject'] = 'Hello'
    msg['From']    = sender
    msg['To']      = addo
    msg['sub'] = disease


    s.sendmail("yadavamit14801@gmail.com",addo, msg.as_string())
    # print("sjgkldsfkl")
    s.quit()

def prdict_heart_disease(list_data):
    csv_file = Admin_Helath_CSV.objects.get(id=1)
    df = pd.read_csv(csv_file.csv_file)

    X = df[['age','sex','cp',  'trestbps',  'chol',  'fbs',  'restecg',  'thalach',  'exang',  'oldpeak',  'slope',  'ca',  'thal']]
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.808, random_state=0)
    nn_model = GradientBoostingClassifier(n_estimators=100,learning_rate=1.0,max_depth=1, random_state=0)
    final_svm_model = SVC()
    final_nb_model = GaussianNB()
    final_knn_model = KNeighborsClassifier(n_neighbors=5)
    final_svm_model.fit(X_train, y_train)
    final_nb_model.fit(X_train, y_train)
    final_knn_model.fit(X_train, y_train)
    nn_model.fit(X_train, y_train)
    pred = nn_model.predict([list_data])
    pred1 = final_svm_model.predict([list_data])
    pred2 = final_nb_model.predict([list_data])
    pred5 = final_knn_model.predict([list_data])
    print("Neural Network Accuracy: {:.2f}%".format(nn_model.score(X_test, y_test) * 100))
    print("SVM Accuracy: {:.2f}%".format(final_svm_model.score(X_test, y_test) * 100))
    print("Naive Bayes Accuracy: {:.2f}%".format(final_nb_model.score(X_test, y_test) * 100))
    print("Knn Accuracy: {:.2f}%".format(final_knn_model.score(X_test, y_test) * 100))
    print("Prdicted Value is : ", format(pred))
    print("Prdicted Value is 1: ", format(pred1))
    print("Prdicted Value is 2: ", format(pred2))
    print("Prdicted Value is 5: ", format(pred5))
    dataframe = str(df.head())
    d = {'GradientBoosting classifier':" {:.2f}%".format(nn_model.score(X_test, y_test) * 100),'SupportVector Classifier':" {:.2f}%".format(final_svm_model.score(X_test, y_test) * 100),'NaiveBayes Classifier':"{:.2f}%".format(final_nb_model.score(X_test, y_test) * 100),'KNearestNeighbor Classifier':"{:.2f}%".format(final_knn_model.score(X_test, y_test) * 100)}

    return (d,(pred))

@login_required(login_url="login")
def add_doctor(request,pid=None):
    doctor = None
    if pid:
        doctor = Doctor.objects.get(id=pid)
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES, instance = doctor)
        if form.is_valid():
            new_doc = form.save()
            new_doc.status = 1
            if not pid:
                user = User.objects.create_user(password=request.POST['password'], username=request.POST['username'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                new_doc.user = user
            new_doc.save()
            return redirect('view_doctor')
    d = {"doctor": doctor}
    return render(request, 'add_doctor.html', d)

def severity_level(values):
    values['trestbps'] = int(values['trestbps'][0])
    values['chole'] = int(values['chole'][0])
    values['fbs'] = int(values['fbs'][0])
    values['age'] = int(values['age'][0])
    values['cp'] = int(values['cp'][0])
    values['old_peak'] = float(values['old_peak'][0])

    print(values)

    if values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] == 1:
        return "Stage 1"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] == 1:
        return "Stage 1"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] == 1:
        return "Stage 1"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] == 1:
        return "Stage 1"   
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 1"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] < 2:
        return "Stage 1"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] < 2:
        return "Stage 1"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 1"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 1"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] < 2:
        return "Stage 1"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 1"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 1"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 1"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 1"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 1"

    # stage2
    elif values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] == 1:
        return "Stage 2"
    elif values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] == 1:
        return "Stage 2"
    elif values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] == 1:
        return "Stage 2"
    
    elif values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 2"
    
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] < 2:
        return "Stage 2"
    
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 2"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 2"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 2"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 2"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 2"
    
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] < 2:
        return "Stage 2"
    
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 2"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 2"
    
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 2"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 2"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 2"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 2"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 2"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 2"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 2"

    # stage 3
    elif values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] < 2:
        return "Stage 3"
    elif values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 3" 
    elif values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 3"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 3"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 3"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 3"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 3"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 3"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] < 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 3"
    elif values['age'] < 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 3"
    elif values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] < 2:
        return "Stage 3"
    elif values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] < 120 and values['old_peak'] < 2 and values['cp'] >= 2:
        return "Stage 3"
    elif values['age'] >= 45 and values['trestbps'] < 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 3"
    elif values['age'] < 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 3"
    elif values['age'] >= 45 and values['trestbps'] >= 80 and values['chole'] >= 150 and values['fbs'] >= 120 and values['old_peak'] >= 2 and values['cp'] >= 2:
        return "Stage 3"

    return 'Stage 3'


    
@login_required(login_url="login")
def predict_desease(request, pred, accuracy):
    try:
        doctor = Doctor.objects.filter(address__icontains=Patient.objects.get(user=request.user).address)
        # send_email(doctor.user.email,predictiondata["Final Prediction"],doctor.user)
        d = {'pred': pred, 'accuracy':accuracy, 'doctor':doctor,"severity":severity}
    except:
        d = {'pred': pred, 'accuracy':accuracy,'doctor':""}
    return render(request, 'predict_disease.html', d)

@login_required(login_url="login")
def add_heartdetail(request):
    if request.method == "POST":
        list_data = []
        values = eval(str(request.POST)[12:-1])
        count = 0
        for key,value in values.items():
            if count == 0:
                count =1
                continue        # breakpoint()

            if key == "sex" and value[0] == "M" or value[0] == 'm' or value[0]=='Male' or value[0] == 'male':
                list_data.append(0)
                values['sex'] = 0
                continue
            elif key == "sex":
                list_data.append(1)
                values['sex'] = 1
                continue
            list_data.append(value[0])

        accuracy,pred = prdict_heart_disease(list_data)
        try:
            patient = Patient.objects.get(user=request.user)
            Search_Data.objects.create(patient=patient, prediction_accuracy=round(accuracy['SVM'],2), result=pred[0], values_list=list_data,predict_for="Heart Prediction")
        except:
            pass
        rem = int(pred[0])
        print("Result = ",rem)
            
        if pred[0] == 0:
            pred = "<span style='color:green'>You are healthy</span>"
            severity=''
        else:
            pred = "<span style='color:red'>You are Unhealthy, Need to Checkup.</span>"
            severity = severity_level(values)
            # breakpoint()
            if severity == "Stage 3":
                try:
                    doctor = Doctor.objects.get(address__icontains=Patient.objects.get(user=request.user).address)
                    send_email(doctor.user.email,patient)
                    messages.success(request, 'Mail sent successfully to doctor '+ doctor.user.username)
                except:
                    pass
        accuracy['severity'] = severity
        return redirect('predict_desease', str(rem),accuracy)
    return render(request, 'add_heartdetail.html')

@login_required(login_url="login")
def predict_desease(request, pred, accuracy):
    try:
        doctor = Doctor.objects.filter(address__icontains=Patient.objects.get(user=request.user).address)
        # send_email(doctor.user.email,predictiondata["Final Prediction"],doctor.user)
        d = {'pred': pred, 'accuracy':accuracy, 'doctor':doctor}
    except:
        d = {'pred': pred, 'accuracy':accuracy,'doctor':""}
    return render(request, 'predict_disease.html', d)




@login_required(login_url="login")
def view_history(request):
    doc = None
    try:
        doc = Doctor.objects.get(user=request.user)
        data = Search_Data.objects.filter(patient__address__icontains=doc.address).order_by('-id')
    except:
        try:
            doc = Patient.objects.get(user=request.user)
            data = Search_Data.objects.filter(patient=doc).order_by('-id')
        except:
            data = Search_Data.objects.all().order_by('-id')
    return render(request,'view_history.html',{'data':data})

@login_required(login_url="login")
def delete_doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    doc.delete()
    return redirect('view_doctor')

@login_required(login_url="login")
def delete_feedback(request,pid):
    doc = Feedback.objects.get(id=pid)
    doc.delete()
    return redirect('view_feedback')

@login_required(login_url="login")
def delete_patient(request,pid):
    doc = Patient.objects.get(id=pid)
    doc.delete()
    return redirect('view_patient')

@login_required(login_url="login")
def delete_searched(request,pid):
    doc = Search_Data.objects.get(id=pid)
    doc.delete()
    return redirect('view_search_pat')

@login_required(login_url="login")
def View_Doctor(request):
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html',d)

@login_required(login_url="login")
def View_Patient(request):
    patient = Patient.objects.all()
    d = {'patient':patient}
    return render(request,'view_patient.html',d)

@login_required(login_url="login")
def View_Feedback(request):
    dis = Feedback.objects.all()
    d = {'dis':dis}
    return render(request,'view_feedback.html',d)

@login_required(login_url="login")
def Profile_Doctor(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    d = {'error': error,'pro':sign}
    return render(request,'profile_doctor.html',d)

@login_required(login_url="login")
def Edit_Doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        cat = request.POST['type']
        try:
            im = request.FILES['image']
            doc.image=im
            doc.save()
        except:
            pass
        dat = datetime.date.today()
        doc.user.first_name = f
        doc.user.last_name = l
        doc.user.email = e
        doc.contact = con
        doc.category = cat
        doc.address = add
        doc.user.save()
        doc.save()
        error = "create"
    d = {'error':error,'doc':doc,'type':type}
    return render(request,'edit_doctor.html',d)

@login_required(login_url="login")
def Edit_My_deatail(request):
    terror = ""
    print("Hii welvome")
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        try:
            im = request.FILES['image']
            sign.image = im
            sign.save()
        except:
            pass
        to1 = datetime.date.today()
        sign.user.first_name = f
        sign.user.last_name = l
        sign.user.email = e
        sign.contact = con
        if error != "pat":
            cat = request.POST['type']
            sign.category = cat
            sign.save()
        sign.address = add
        sign.user.save()
        sign.save()
        terror = "create"
    d = {'error':error,'terror':terror,'doc':sign}
    return render(request,'edit_profile.html',d)

@login_required(login_url='login')
def sent_feedback(request):
    error = None
    if request.method == "POST":
        username = request.POST['uname']
        message = request.POST['msg']
        username = User.objects.get(username=username)
        Feedback.objects.create(user=username, messages=message)
        error = "create"
    return render(request, 'sent_feedback.html',{'terror':error})



def add_genralhealth(request):
    predictiondata = None
    symptomList = []           # selected symptoms
    patient = ''
    doctor = ''
    if request.method=="POST":
        for i,j in request.POST.items():
            if "csrfmiddlewaretoken" != i:
                symptomList.append(i)
        # training.csv
        DATA_PATH = Admin_Helath_CSV.objects.get(id=2)
        data = pd.read_csv(DATA_PATH.csv_file).dropna(axis = 1)

        # Checking whether the dataset is balanced or not
        disease_counts = data["prognosis"].value_counts()
        temp_df = pd.DataFrame({
            "Disease": disease_counts.index,
            "Counts": disease_counts.values
        })

        encoder = LabelEncoder()
        data["prognosis"] = encoder.fit_transform(data["prognosis"])   # encoding


        X = data.iloc[:,:-1]    # rows except last column
        y = data.iloc[:, -1]    #last column
        X_train, X_test, y_train, y_test =train_test_split(
        X, y, test_size = 0.2, random_state = 24)
        symptoms = X.columns.values  
        symptom_index = {}
        for index, value in enumerate(symptoms):
            symptom = " ".join([i.capitalize() for i in value.split("_")])
            symptom_index[symptom] = index
        
        data_dict = {
            "symptom_index":symptom_index,
            "predictions_classes":encoder.classes_    # array of disease
        }
        # breakpoint()
# 
        final_svm_model = SVC()
        final_nb_model = GaussianNB()
        final_rf_model = RandomForestClassifier(random_state=18)
        final_ds_model = DecisionTreeClassifier(random_state=20)
        final_knn_model = KNeighborsClassifier(n_neighbors=5)
        final_svm_model.fit(X, y)
        final_nb_model.fit(X, y)
        final_rf_model.fit(X, y)
        final_ds_model.fit(X,y)
        final_knn_model.fit(X,y)
        

        #Testing.csv
        # DATA_PATH2 = Admin_Helath_CSV.objects.get(id=3)
        # test_data = pd.read_csv(DATA_PATH2.csv_file).dropna(axis=1)

        # test_X = test_data.iloc[:, :-1]
        # test_Y = encoder.transform(test_data.iloc[:, -1])

        svm_preds = final_svm_model.predict(X_test)
        nb_preds = final_nb_model.predict(X_test)
        rf_preds = final_rf_model.predict(X_test)
        ds_preds = final_ds_model.predict(X_test)
        knn_preds = final_knn_model.predict(X_test)

        final_preds = [mode([i,j,k,l,m])[0][0] for i,j,
                    k,l,m in zip(svm_preds, nb_preds, rf_preds,ds_preds,knn_preds)]

        print(f"Accuracy on Test dataset by the combined model\
        : {accuracy_score(y_test, final_preds)*100}")

        def predictDisease(symptoms):
            input_data = [0] * len(data_dict["symptom_index"])
            for symptom in symptoms:
                index = data_dict["symptom_index"][symptom]
                input_data[index] = 1
           
            input_data = np.array(input_data).reshape(1,-1)
            # generating individual outputs
            rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
            nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
            svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]
            ds_prediction = data_dict["predictions_classes"][final_ds_model.predict(input_data)[0]]
            knn_prediction = data_dict["predictions_classes"][final_knn_model.predict(input_data)[0]]
            
            # making final prediction by taking mode of all predictions
            final_prediction = mode([rf_prediction, nb_prediction, svm_prediction,ds_prediction,knn_prediction])[0][0]
            predictions = {
                "RandomForestClassifier Prediction": rf_prediction,
                "GaussianNB Prediction": nb_prediction,
                "SVC Prediction": svm_prediction,
                "Decision Tree": ds_prediction,
                "KNN Prediction": knn_prediction,
                "Final Prediction":final_prediction
            }
            return predictions

        # Testing the function
        predictiondata = predictDisease(symptomList)
        patient = Patient.objects.get(user=request.user)
        doctor = Doctor.objects.get(address__icontains=Patient.objects.get(user=request.user).address)
        send_email(doctor.user.email,patient,predictiondata["Final Prediction"])
        # print(doctor.user,)
        messages.success(request, 'Email sent to doctor ' + doctor.user.get_full_name() + " successfully" )
        Search_Data.objects.create(patient=patient, prediction_accuracy=round(accuracy_score(y_test, final_preds)*100,2), result=predictiondata["Final Prediction"], values_list=symptomList, predict_for="General Health Prediction")
        

        # print(deseaseli)
    alldisease = ['Watering From Eyes','Increased Appetite','Polyuria','Family History','Mucoid Sputum','Rusty Sputum','Irregular Sugar Level','Cough','High Fever','Sunken Eyes','Breathlessness','Sweating','Dehydration','Indigestion','Headache','Yellowish Skin','Dark Urine','Nausea','Loss Of Appetite','Pain Behind The Eyes','Back Pain','Constipation','Abdominal Pain','Diarrhoea','Mild Fever','Yellow Urine','Yellowing Of Eyes','Acute Liver Failure','Fluid Overload','Swelling Of Stomach','Swelled Lymph Nodes','Malaise','Blurred And Distorted Vision','Phlegm','Throat Irritation','Redness Of Eyes','Sinus Pressure','Runny Nose','Congestion','Chest Pain','Weakness In Limbs','Lack Of Concentration','Visual Disturbances','Receiving Blood Transfusion','Receiving Unsterile Injections','Coma','Stomach Bleeding','Distention Of Abdomen','History Of Alcohol Consumption','Fluid Overload','Blood In Sputum','Prominent Veins On Calf','Palpitations','Painful Walking','Pus Filled Pimples', 'Blackheads','Scurring','Skin Peeling','Silver Like Dusting','Small Dents In Nails','Inflammatory Nails','Blister','Itching','Skin Rash','Nodal Skin Eruptions','Continuous Sneezing','Shivering','Chills','Joint Pain','Stomach Pain','Acidity','Ulcers On Tongue','Muscle Wasting','Vomiting','Burning Micturition','Fatigue','Weight Gain','Anxiety','Cold Hands And Feets','Mood Swings','Weight Loss','Restlessness','Lethargy','Patches In Throat','Fast Heart Rate',	'Pain During Bowel Movements','Pain In Anal Region','Bloody Stool','Irritation In Anus','Neck Pain','Dizziness','Cramps','Bruising','Obesity','Swollen Legs','Swollen Blood Vessels','Puffy Face And Eyes','Enlarged Thyroid','Brittle Nails','Swollen Extremeties','Excessive Hunger','Extra Marital Contacts','Drying And Tingling Lips','Slurred Speech','Knee Pain','Hip Joint Pain','Muscle Weakness','Stiff Neck','Swelling Joints','Movement Stiffness','Spinning Movements','Loss Of Balance','Unsteadiness','Weakness Of One Body Side','Loss Of Smell','Bladder Discomfort','Continuous Feel Of Urine','Passage Of Gases','Internal Itching','Toxic Look (Typhos)',	'Depression','Irritability','Muscle Pain','Altered Sensorium','Red Spots Over Body','Belly Pain','Abnormal Menstruation','Anorexia','Asthenia','Musculoskeletkl Pain','Muscle Aches And Backache','Swollen Lymph Nodes','Chills','Exhaustion','Rash','Muscle Pain','Weakness And Fatigue','Sore Throat','Abdominal Pain','Bleeding','Bruising','Aches And Pain' ]
    return render(request,'add_genralhealth.html', {'doctor':doctor,'alldisease':alldisease, 'predictiondata':predictiondata,'patient':patient})

