import psycopg2
import smtplib
import logging
import datetime
import requests
import json
from dateutil.relativedelta import relativedelta


SERVER = "smtp.gmail.com"
PORT = 587
FROM = "fitnessgaragehyd@gmail.com"
SUBJECT = "GYM SUBSCRIPTION ENDING"
smsURL = "https://www.fast2sms.com/dev/bulkV2"
numbersList = ""
aboutToEndData = {}
endsData = {}
subscriptionEndsList = []


try:
    logging.basicConfig(filename="CheckSubscriptionLog.log", format="%(asctime)s %(message)s", filemode="a")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
except:
    print("Unable to open log file")

try:
    con = psycopg2.connect(database="*********", user="*********", password="*********", host="127.0.0.1", port="5432")
except:
    logger.error("DB connection failed!!!")

cur = con.cursor()

detailsQuery = "select * from GymMembers;"

cur.execute(detailsQuery)

gymDetails = cur.fetchall()

for i in gymDetails:
    regNo = i[0]
    name = i[1]
    mobileNo = i[2]
    emailID = i[3]
    subscriptionDuration = i[5]
    subscriptionStartDate = datetime.datetime.fromtimestamp(int(i[4]))
    subscriptionStartDate = subscriptionStartDate.date()
    subscriptionEndDate = datetime.datetime.fromtimestamp(int(i[4])) + relativedelta(months=int(i[5]))
    subscriptionEndDate = subscriptionEndDate.date()
    reminderDate = subscriptionEndDate + relativedelta(days=-3)
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
            if int(str(today - subscriptionEndDate).split(" ")[0]) >= 3:
                cur.execute("delete from GymMembers where phonenumber=(%s)",(mobileNo,))
                con.commit()
        elif today < subscriptionEndDate:
            endsIndays = str(subscriptionEndDate - today).split(',')[0]
            aboutToEndData = {
                "route" : "v3",
                "sender_id" : "FitnessGarage",
                "message" : "\n" + name + "\n\nThis is to notify you that your gym subscription ends in " + endsIndays + ". Please renew your subscription.\n\nThanks & Regards\nPraveen Yadav\nFitness Garage\n\n",
                "language" : "english",
                "flash" : 0,
                "numbers" : mobileNo,
            }
            headers = {
                "authorization" : "************",
                "Content-Type" : "application/x-www-form-urlencoded",
                "Cache-Control" : "no-cache"
            }
            response = requests.request("POST", smsURL, data=aboutToEndData, headers=headers)
            msg = json.loads(response.text)
            print(msg)
            print("Ends in " + endsIndays)
            BODY = "\n\n\nHello " + name + ", \n\nThis is to notify you that your gym subscription ends in " + endsIndays + ". Please renew your subscription.\n\nThanks & Regards\nPraveen Yadav\nFitness Garage\n\n"
            message = """From: %s\r\nTo: %s\nSubject: %s\n\n\n%s""" % (FROM, emailID, SUBJECT, BODY)
            server = smtplib.SMTP_SSL(SERVER, 465)
            server.login(FROM, "********")
            server.sendmail(FROM, emailID, message)
            server.quit()
        else:
            endsData = {
                "route" : "v3",
                "sender_id" : "FitnessGarage",
                "message" : "\n" + name + "\n\nThis is to notify you that your gym subscription ends today. Please renew your subscription.\n\nThanks & Regards\nPraveen Yadav\nFitness Garage",
                "language" : "english",
                "flash" : 0,
                "numbers" : mobileNo,
            }
            headers = {
                "authorization" : "***********",
                "Content-Type" : "application/x-www-form-urlencoded",
                "Cache-Control" : "no-cache"
            }
            response = requests.request("POST", smsURL, data=endsData, headers=headers)
            msg = json.loads(response.text)
            print(msg)
            print("ENDS TODAY : ", subscriptionEndDate)
            subscriptionEndsList.append(name)
            BODY = "Hello " + name + ", \n\n\tThis is to notify you that your gym subscription ends today. Please renew your subscription.\n\nThanks & Regards\nPraveen Yadav\nFitness Garage"
            message = """From: %s\r\nTo: %s\nSubject: %s\n\n\n%s""" % (FROM, emailID, SUBJECT, BODY)
            server = smtplib.SMTP_SSL(SERVER, 465)
            server.login(FROM, "***********")
            server.sendmail(FROM, emailID, message)
            server.quit()
    else:
        print("SUBSCRIPTION NOT ENDING IN NEXT 7 DAYS!!")


subscriptionEndsString = ", ".join(subscriptionEndsList)
subscriptionEndsData = {
    "route" : "v3",
    "sender_id" : "FitnessGarage",
    "message" : "\nPraveen\n\nThis is to notify you that the following customer's gym subscription ends today.\n\nNames : "+ subscriptionEndsString +"\n\nThanks\nFitness Garage",
    "language" : "english",
    "flash" : 0,
    "numbers" : mobileNo,
}

headers = {
    "authorization" : "*************",
    "Content-Type" : "application/x-www-form-urlencoded",
    "Cache-Control" : "no-cache"
}

if subscriptionEndsList:
    response = requests.request("POST", smsURL, data=subscriptionEndsData, headers=headers)
    msg = json.loads(response.text)
    print("\n\n\n" + str(msg))
    BODY = "Hello Praveen\n\n\tThis is to notify you that the following customer's gym subscription ends today.\n\nNames : "+ subscriptionEndsString +"\n\nThanks\nFitness Garage"
    message = """From: %s\r\nTo: %s\nSubject: %s\n\n\n%s""" % (FROM, FROM, "SUBSCRIPTIONS ENDING TODAY", BODY)
    server = smtplib.SMTP_SSL(SERVER, 465)
    server.login(FROM, "**********")
    server.sendmail(FROM, FROM, message)
    server.quit()
