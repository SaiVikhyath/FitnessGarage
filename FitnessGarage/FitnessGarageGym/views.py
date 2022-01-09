from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages

import psycopg2
import time
import json
import smtplib
import requests
import datetime
from dateutil.relativedelta import relativedelta
from json import dumps


# Create your views here.

SERVER = "smtp.gmail.com"
PORT = 587
FROM = "fitnessgaragehyd@gmail.com"
SUBJECT = "WELCOME TO FITNESS GARAGE"
plansDict = {"one": 1, "three": 3, "six": 6, "twelve": 12}
smsURL = "https://www.fast2sms.com/dev/bulkV2"

try:
    con = psycopg2.connect(database="FitnessGarage", user="**********", password="*********", host="127.0.0.1", port="5432")
except:
    print("DB Connectivity failed!!!")

cur = con.cursor()

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        custName = request.POST['name']
        cur.execute("select phonenumber from GymMembers")
        phnNoList = cur.fetchall()
        phnNoList = [phnNo[0] for phnNo in phnNoList]
        print(phnNoList)
        mobileNo = request.POST['mobileNo']
        print(mobileNo)
        if mobileNo not in phnNoList:
            emailID = request.POST['emailID']
            subscriptionDuration = request.POST['plans']
            subscriptionType = request.POST['subscriptionType'] 
            personalTraining = request.POST['personaltraining']        
            subscriptionDuration = plansDict.get(subscriptionDuration)
            startDate = int(time.time())        
            subscriptionType = subscriptionType.capitalize()
            personalTraining = personalTraining.capitalize()
            cur.execute("""INSERT INTO GymMembers 
            (membername, phonenumber, email, startdate, subscription, subscriptiontype, personaltraining) 
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s)""", 
            (custName, mobileNo, emailID, startDate, subscriptionDuration, subscriptionType, personalTraining))
            con.commit()
            # welcomeData = {
            #     "route" : "v3",
            #     "sender_id" : "FitnessGarage",
            #     "message" : "\n" + custName + "\n\nWelcome to FitnessGarage. Thank you for " + subscriptionType + " subscription.\n\nPraveen Yadav\nFitness Garage\n\n",
            #     "language" : "english",
            #     "flash" : 0,
            #     "numbers" : mobileNo,
            # }
            # headers = {
            #     "authorization" : "***************",
            #     "Content-Type" : "application/x-www-form-urlencoded",
            #     "Cache-Control" : "no-cache"
            # }
            # response = requests.request("POST", smsURL, data=welcomeData, headers=headers)
            # msg = json.loads(response.text)
            # print(msg)
            # BODY = "\n\n\nHello " + custName + "\n\nWelcome to FitnessGarage. Thank you for " + subscriptionType + " subscription.\n\nPraveen Yadav\nFitness Garage\n\n"
            # message = """From: %s\r\nTo: %s\nSubject: %s\n\n\n%s""" % (FROM, emailID, SUBJECT, BODY)
            # server = smtplib.SMTP_SSL(SERVER, 465)
            # server.login(FROM, "*********")
            # server.sendmail(FROM, emailID, message)
            # server.quit()
            #return render(request, 'register.html')
            return HttpResponse('''<script>
                if (window.confirm("User registered successfully...Do you want to register another user?"))
                {
                    window.location.href = "http://127.0.0.1:8000/register.html"
                }
                else
                {
                    window.location.href = "http://127.0.0.1:8000/"
                }
                </script>''')
            return render(request, 'status.html')
        else:
            #return render(request, 'register.html')
            return HttpResponse('''<script>
                if (window.confirm("Duplicate phone number, Cannot register the user...You want to register the user again?"))
                {
                    window.location.href = "http://127.0.0.1:8000/register.html"
                }
                else
                {
                    window.location.href = "http://127.0.0.1:8000/"
                }
                </script>''')
    else:
        return render(request, 'register.html')

def dashboard(request):
    cur.execute("select * from GymStats")
    gymStats = cur.fetchall()
    gymStats = gymStats[0]
    totalMembers = gymStats[0]
    personalTraining = gymStats[1]
    cardioMembers = gymStats[2]
    weightsMembers = gymStats[3]
    stats ={"personalTraining": int(personalTraining), 
    "noPersonalTraining": int(str(int(totalMembers) - int(personalTraining))),
    "cardioMembers": int(cardioMembers),
    "weightsMembers": int(weightsMembers)}
    stats = dumps(stats)
    return render(request, 'dashboard.html', {'data': stats})


def personalTraining(request):
    cur.execute("select * from PersonalTraining")
    pt = cur.fetchall()
    details = []
    for r in pt:
        r = list(r)
        r[3] = time.strftime("%d-%m-%Y", time.localtime(int(r[3])))
        details.append(tuple(r))
    return render(request, 'personalTraining.html', {'pt': details})

def cardioMembers(request):
    cur.execute("select * from CardioMembers")
    pt = cur.fetchall()
    details = []
    for r in pt:
        r = list(r)
        r[3] = time.strftime("%d-%m-%Y", time.localtime(int(r[3])))
        details.append(tuple(r))
    return render(request, 'cardioMembers.html', {'pt': details})

def weightsMembers(request):
    cur.execute("select * from WeightMembers")
    pt = cur.fetchall()
    details = []
    for r in pt:
        r = list(r)
        r[3] = time.strftime("%d-%m-%Y", time.localtime(int(r[3])))
        details.append(tuple(r))
    return render(request, 'weightsMembers.html', {'pt': details})

def allMembers(request):
    cur.execute("select * from GymMembers")
    pt = cur.fetchall()
    details = []
    for r in pt:
        r = list(r)
        r[3] = time.strftime("%d-%m-%Y", time.localtime(int(r[3])))
        details.append(tuple(r))
    return render(request, "allMembers.html", {"pt": details})
