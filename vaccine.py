import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import ssl
import psycopg2


def show_availability(state , district, choice , email):
    put_in_db(state,district,choice,email)
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': "Token token= "
    
        }

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    payload = {}

    response = requests.request("GET", url, headers=headers , data =payload)
    print(response)
    res = response.json()
    #print( res['states'])

    district_id = ""
    state_id = ""

    state_name =  state

    for i in res['states']:
        if state_name in i['state_name']:
            state_id = i['state_id']
            print(i['state_id'])

    get_district = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+str(state_id)
    
    choice = choice
    
    response = requests.request("GET", get_district, headers=headers , data =payload)
    res2 = response.json()
    #print(res2)

    district_name = district
    to_email =  email



    for i in res2['districts']:
        if district_name in i['district_name']:
            district_id = i['district_id']
            print(i['district_id'])
    
    run_first(choice, district_id, state_id, to_email, headers, payload)

    #https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=512&date= "11-05-2021"
def alert_me(center , date , min_age_limit , vaccine_name , available_slots , fee , address, to_email):
    msg = MIMEMultipart()
    email_to = to_email
    message = str(available_slots)+ " SLOTS AVAILABLE on "+ str(date) +" : at " + str(center) + " Address : " + str(address) + " for minimum age : " + str(min_age_limit) + " at cost: " + str(fee)
    send_from = "serviceid40@gmail.com"
    send_to = email_to
    cc_to = ""

    SUBJECT = "VACCINE SLOTS AVAILABLE!!!"
    SMTPSERVER = 'smtp.gmail.com:587'
    
    msg = 'Subject: {}\n\n{}'.format(SUBJECT, message)
   
    username = ''  
    password = ''  
    
    # The actual mail send  
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password) 
    

    server.sendmail(send_from, send_to, msg)
    server.quit()

    


def run_first(choice, district_id, state_id, to_email, headers, payload):
    z = 0
    for i in range(5):  
    
        one_year_from_now = datetime.datetime.now() + relativedelta(days=z)
        z = z+3  #date thing, need to be thinked over
        date_formated = one_year_from_now.strftime("%d-%m-%Y")
        print (date_formated)
        url3 = "https://www.cowin.gov.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(district_id) +"&date=" + str(date_formated)
        response3 = requests.request("GET", url3, headers=headers , data =payload)
        print(response3)
        res3 = response3.json()

        for j in res3['centers']:
            for k in j['sessions']:
                if choice == 1:
                    if (k['min_age_limit'] == "18"):
                        #print(j['name'], k['date'], k['min_age_limit'] ,k['vaccine'] , k['available_capacity'] , j['address'] , j['fee_type'] )
                        if (k['available_capacity'] > 0):
                            center = j['name']
                            date = k['date']
                            min_age_limit = k['min_age_limit']
                            vaccine_name = k['vaccine']
                            available_slots = k['available_capacity']
                            fee = j['fee_type']
                            address = j['address']
                            print("test")
                            #alert_me(center , date , min_age_limit , vaccine_name , available_slots , fee , address, to_email)
                        else:
                            print("test3")
                    else:
                        print("test4")
            
                if choice == 432:
                    #print(j['name'], k['date'], k['min_age_limit'] ,k['vaccine'] , k['available_capacity'] , j['address'] , j['fee_type'] )
                    if (k['available_capacity'] > 0):
                        center = j['name']
                        date = k['date']
                        min_age_limit = k['min_age_limit']
                        vaccine_name = k['vaccine']
                        available_slots = k['available_capacity']
                        fee = j['fee_type']
                        address = j['address']
                        #alert_me(center , date , min_age_limit , vaccine_name , available_slots , fee , address, to_email)
                        print("test2")

                        
                        
def put_in_db(state,district,choice,email):
    dbname=''
    user=''
    host=''
    password=''
    port='' 
    sslmode=''

    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)
    print("Connection established")
    conn.set_session(autocommit=True)
    cursor = conn.cursor()
    
    state = str(state)
    district = str(district)
    email = str(email)
    
    if choice == 1:
        choice = str(choice)
        sql = "INSERT INTO inventory(email, state, district, choice) VALUES(%s, %s, %s, %s)"
        val = (email, state, district, choice)
        cursor.execute(sql,val)
    
    if choice == 2:
        choice = str(choice)
        sql = "INSERT INTO inventory45(email, state, district, choice) VALUES(%s, %s, %s, %s)"
        val = (email, state, district, choice)
        cursor.execute(sql,val)

        
                        
if __name__ == '__main__':
    #put_in_db("state","district",1,"email")
    show_availability(state,district,choice,email)
            
            