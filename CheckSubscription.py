import psycopg2
import smtplib
import logging
import datetime
import requests
import json
from dateutil.relativedelta import relativedelta

SERVER = 'smtp.gmail.com'
PORT = 587
FROM = "fitnessgaragehyd@gmail.com"
SUBJECT = "GYM SUBSCRIPTION ENDING"
smsURL = "https://www.fast2sms.com/dev/bulk"
numbersList = ""
aboutToEndData = {}
endsData = {}

try:
    logging.basicConfig(filename="CheckSubscriptionLog.log", format="%(asctime)s %(message)s", filemode="a")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
except:
    print("Unable to open log file")

try:
    con = psycopg2.connect(database="FitnessGarage", user="GymAdmin", password="IamAdmin@1235", host="127.0.0.1", port="5432")
except:
    logger.error("DB connection failed!!!")

cur = con.cursor()

detailsQuery = "select * from GymMembers;"

cur.execute(detailsQuery)

gymDetails = cur.fetchall()

for i in gymDetails:
    print(i)
    regNo = i[0]
    name = i[1]
    mobileNo = i[2]
    emailID = i[3]
    subscriptionDuration = i[5]
    subscriptionStartDate = datetime.datetime.fromtimestamp(int(i[4]))
    subscriptionStartDate = subscriptionStartDate.date()
    subscriptionEndDate = datetime.datetime.fromtimestamp(int(i[4])) + relativedelta(months=int(i[5]))
    subscriptionEndDate = subscriptionEndDate.date()
    reminderDate = subscriptionEndDate + relativedelta(days=-7)
    today = datetime.datetime.now().date()
    print("RECEIPT NO : ", regNo)
    print("NAME : ", name)
    print("MOBILE NUMBER : ", mobileNo)
    print("EMAIL ID : ", emailID)
    print("SUBSCRIPTION START : ", subscriptionStartDate)
    print("SUBSCRIPTION END : ", subscriptionEndDate)
    print("REMINDER DATE : ", reminderDate)
    print("TODAY : ", today)
    if today >= reminderDate:
        if today > subscriptionEndDate:
            print("ENDED ON : ", subscriptionEndDate)
        elif today < subscriptionEndDate:
            endsIndays = str(subscriptionEndDate - today).split(',')[0]
            aboutToEndData = {
                "sender_id" : "FitnessGarage",
                "message" : "Hello " + name + ", \n\nThis is to notify you that your gym subscription ends in " + endsIndays + ". Please renew your subscription.\n\nThanks & Regards\nPraveen Yadav\nFitness Garage\n\n\n\n",
                "language" : "english",
                "route" : "p",
                "numbers" : mobileNo
            }
            headers = {
                "authorization" : "AXkp5NdE0JL9votFqmYMIWTUhceiQ8D1GOlH2rw4jySn67RgPxlAHthDOr4nbJQo3qzgRCW96V1KIGP8",
                "Content-Type" : "application/x-www-form-urlencoded",
                "Cache-Control" : "no-cache"
            }
            response = requests.request("POST", smsURL, data=aboutToEndData, headers=headers)
            msg = json.loads(response.text)
            BODY = "Hello " + name + ", \n\nThis is to notify you that your gym subscription ends in " + endsIndays + ". Please renew your subscription.\n\nThanks & Regards\nPraveen Yadav\nFitness Garage\n\n"
            message = """From: %s\r\nTo: %s\nSubject: %s\n\n\n%s""" % (FROM, emailID, SUBJECT, BODY)
            print(message)
            server = smtplib.SMTP_SSL(SERVER, 465)
            server.login(FROM, "Fitnessgarage")
            server.sendmail(FROM, emailID, message)
            server.quit()
        else:
            endsData = {
                "sender_id" : "FitnessGarage",
                "message" : "Hello " + name + ", \n\n\tThis is to notify you that your gym subscription ends today. Please renew your subscription.\n\nThanks & Regards\nPraveen Yadav\nFitness Garage\n\n\n\n",
                "language" : "english",
                "route" : "p",
                "numbers" : mobileNo
            }
            headers = {
                "authorization" : "AXkp5NdE0JL9votFqmYMIWTUhceiQ8D1GOlH2rw4jySn67RgPxlAHthDOr4nbJQo3qzgRCW96V1KIGP8",
                "Content-Type" : "application/x-www-form-urlencoded",
                "Cache-Control" : "no-cache"
            }
            response = requests.request("POST", smsURL, data=aboutToEndData, headers=headers)
            msg = json.loads(response.text)
            print("ENDS TODAY : ", subscriptionEndDate)
            BODY = "Hello " + name + ", \n\n\tThis is to notify you that your gym subscription ends today. Please renew your subscription.\n\nThanks & Regards\nPraveen Yadav\nFitness Garage"
            message = """From: %s\r\nTo: %s\nSubject: %s\n\n\n%s""" % (FROM, emailID, SUBJECT, BODY)
            print(message)
            server = smtplib.SMTP_SSL(SERVER, 465)
            server.login(FROM, "Fitnessgarage")
            server.sendmail(FROM, emailID, message)
            server.quit()
    else:
        print("SUBSCRIPTION NOT ENDING IN NEXT 7 DAYS!!")
    