from django.shortcuts import redirect, render
from django.contrib import messages

import psycopg2
import logging
import datetime
import time
import re
from dateutil.relativedelta import relativedelta
from json import dumps

# Create your views here.

plansDict = {"one": 1, "three": 3, "six": 6, "twelve": 12}

try:
    con = psycopg2.connect(database="FitnessGarage", user="GymAdmin", password="IamAdmin@1235", host="127.0.0.1", port="5432")
except:
    print("DB Connectivity failed!!!")

cur = con.cursor()

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        registrationNo = request.POST['regNo']
        custName = request.POST['name']
        mobileNo = request.POST['mobileNo']
        emailID = request.POST['emailID']
        subscriptionDuration = request.POST['plans']
        subscriptionType = request.POST['subscriptionType'] 
        personalTraining = request.POST['personaltraining']        
        subscriptionDuration = plansDict.get(subscriptionDuration)
        startDate = int(time.time())        
        subscriptionType = subscriptionType.capitalize()
        personalTraining = personalTraining.capitalize()
        print()
        print(registrationNo, type(registrationNo))
        print(custName, type(custName))
        print(mobileNo, type(mobileNo))
        print(emailID, type(emailID))
        print(startDate)
        print(subscriptionDuration, type(subscriptionDuration))
        print(subscriptionType, type(subscriptionType))
        print(personalTraining, type(personalTraining))
        print()
        cur.execute("""INSERT INTO GymMembers 
        (regno, membername, phonenumber, email, startdate, subscription, subscriptiontype, personaltraining) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s)""", 
        (registrationNo, custName, mobileNo, emailID, startDate, subscriptionDuration, subscriptionType, personalTraining))
        con.commit()
        return redirect('/')
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
    print(gymStats)
    print(totalMembers)
    print(personalTraining)
    print(cardioMembers)
    print(weightsMembers)
    return render(request, 'dashboard.html', {'data': stats})