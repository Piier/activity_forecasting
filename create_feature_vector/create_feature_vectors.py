import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime
import re
import csv
import pandas as pd


case=['HH122']
case2=['hh122']

name_db="casas"
username_db="postgres"
password_db="admin"
host_db="127.0.0.1"
port_db="5432"

try:
    connection = psycopg2.connect(user=username_db,
                                password=password_db,
                                host=host_db,
                                port=port_db,
                                database=name_db)
    cursor = connection.cursor()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


def is_business_day(date):
    return bool(len(pd.bdate_range(date, date)))


def createDataset(fileName):
    with open(fileName,"r") as fileCASAS:
        dataset=[riga.strip().split("\t") for riga in fileCASAS]
    return dataset

def create_sensor():
    query_sensor="select name from activity.sensor where house='"+house+"'"
    cursor.execute(query_sensor)
    sensor= [x[0] for x in cursor]
    
    return sensor

def create_activity():
    query_activity="select distinct name from activity.activity where house='"+house+"'"
    cursor.execute(query_activity)
    activity= [x[0] for x in cursor]
    
    return activity

def printMatrixList(list):
    for element in list:
        print(*element)


def discret_sensor(times, events,start_time):
    val=0
    n=0
    sec=0
    time_last_val=start_time.strftime("%Y-%m-%d %H:%M:%S")
    for i in range(len(events)):
        if val!=events[i]:
            val=events[i]
            time_last_val=times[i]
            n+=1
    
    sec=int(((start_time+datetime.timedelta(0, 60*60))- datetime.datetime.strptime(time_last_val,"%Y-%m-%d %H:%M:%S")).total_seconds())

    return [val,n,sec] 


def sample_sensor(times, events, start_time):

    massimo = max(events)
    minimo  = min(events)
    diff    = massimo-minimo
    #print(start_time)
    time_last_val=start_time.strftime("%Y-%m-%d %H:%M:%S")
    val=0
    avg=0
    sec=0
    
    for i in range(len(events)):
        
        if i != 0:
            avg+=events[i]+(events[i-1]* (int((datetime.datetime.strptime(times[i],"%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(times[i-1],"%Y-%m-%d %H:%M:%S")).total_seconds())-1))
        else:
            avg+events[i]
        if val!=events[i]: 
            val=events[i]
            time_last_val=times[i]
            
    
    avg+=(int(((start_time+datetime.timedelta(0, 60*60))- datetime.datetime.strptime(times[-1],"%Y-%m-%d %H:%M:%S")).total_seconds())-1)*events[-1]
    avg/=3600
    #print(times)
    sec=int(((start_time+datetime.timedelta(0, 60*60))- datetime.datetime.strptime(time_last_val,"%Y-%m-%d %H:%M:%S")).total_seconds())

    return [massimo,minimo,avg,diff,sec]

def create_header(sensors, activity, file_csv):
    header = list()
    header.append("Minutes from midnight")
    header.append("Days")
    header.append("Is business")
    for sensor in sensors:
        if re.findall(r"^ZB",sensor) or re.findall(r"^M",sensor) or re.findall(r"^F",sensor) or re.findall(r"^D",sensor) or (re.findall(r"^L",sensor) and not re.findall(r"^LL",sensor) and not re.findall(r"^LS",sensor)):
            header.append("VAL "+sensor)
            header.append("N "+sensor)
            header.append("SEC "+sensor)
        else:
            header.append("MAX "+sensor)
            header.append("MIN "+sensor)
            header.append("AVG "+sensor)
            header.append("DIFF "+sensor)
            header.append("SEC "+sensor)
    for act in activity:
        header.append("TIME "+act )
    
    header.append("TO PREDICT")
    employee_writer = csv.writer(file_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    employee_writer.writerow(header)


def activity_times(activities,considerd_hour):
    query="select name, startdate, enddate from activity.activity where house='"+house+"' and id not in(select id from activity.activity where(enddate<'"+considerd_hour.strftime("%Y-%m-%d %H:%M:%S")+"'or startdate>'"+(considerd_hour+datetime.timedelta(0, 60*60)).strftime("%Y-%m-%d %H:%M:%S")+"'))"
    act_time=[0 for x in range(len(activities))]

    cursor.execute(query)
    for act in cursor:
        activity=list(act)
        
        if activity[1]<considerd_hour:
            activity[1]=considerd_hour
        if activity[2]>(considerd_hour+datetime.timedelta(0, 60*60)):
            activity[2]=(considerd_hour+datetime.timedelta(0, 60*60))   
        act_time[activities.index(activity[0])]+=int((activity[2]-activity[1]).total_seconds())

    query="select name from activity.activity where house='"+house+"' AND startdate>'"+(considerd_hour+datetime.timedelta(0, 60*60)).strftime("%Y-%m-%d %H:%M:%S")+"'"
    cursor.execute(query)
    risp=cursor.fetchone()
    if risp==None:
        query="select name from  activity.activity where id=(select max(id) from  activity.activity where house='"+house+"')"
        cursor.execute(query)
        risp=cursor.fetchone()
    act_time.append(risp[0])

    return act_time




for w in range(len(case)):
    house=case[w]
    house2=case2[w]
    print("Casa ", house)
    file_csv=open("feature_vector"+house+".csv","w",newline="")

    dataset=createDataset("formatted"+house2+".txt")#Creo il dataset
    sensor=create_sensor()#Creo i sensori
    activities=create_activity()#Creo le attivita
    create_header(sensor, activities, file_csv)

    start_time=dataset[0][0]#Orario primo evento
    end_time=dataset[-1][0]#Orario ultimo evento

    print("Fine lettura")

    #hour_table_vector=list()
    start_time=datetime.datetime.strptime(dataset[0][0]+" "+dataset[0][1], '%Y-%m-%d %H:%M:%S.%f')#Orario evento


    #for i in range(len(dataset)):
    k=0
    i=0
    #considerd_hour=list()

    appHour=start_time.strftime("%H:%M:%S")

    print("Inizio creazione table")
    cont=0
    while i<len(dataset):
        
        start_time=datetime.datetime.strptime(dataset[i][0]+" "+dataset[i][1], '%Y-%m-%d %H:%M:%S.%f')
        print(i,start_time)
        if cont%10==0:
            print("Feature vector fatti: ",cont)
        considerd_hour = start_time
        previouse_row= [0 for i in sensor]
        previouse_row.insert(0,datetime.datetime.strptime("1970-01-01 01:00:00","%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"))
        table_vector=list()
        while datetime.datetime.strptime(dataset[i][0]+" "+dataset[i][1], '%Y-%m-%d %H:%M:%S.%f') <= start_time+datetime.timedelta(0, 60*60):
            
            appHour=datetime.datetime.strptime(dataset[i][1],"%H:%M:%S.%f").strftime("%H:%M:%S")
        
            previouse_row[sensor.index(dataset[i][2])+1]=dataset[i][3]
            
            if (appHour!=previouse_row[0].split(" ")[1] and i<len(dataset)-1 and appHour!=datetime.datetime.strptime(dataset[i+1][1],'%H:%M:%S.%f').strftime("%H:%M:%S")) or (i==len(dataset)-1):
                
                previouse_row[0]=datetime.datetime.strptime(dataset[i][0]+" "+dataset[i][1],'%Y-%m-%d %H:%M:%S.%f').strftime("%Y-%m-%d %H:%M:%S")
                table_vector.append(list(previouse_row))
                if i==len(dataset)-1:
                    i+=1
                    break
            i+=1
            
        hour_table_vector=list(table_vector) 

        #---------------------------------

        #print("Feature vector n: ",cont)
        feature_vector=list()
        times=list()

        if len(hour_table_vector)!=0:
        
            for k in range(len(hour_table_vector)):
                times.append(hour_table_vector[k][0])
            
            for j in range(len(sensor)):
                events = list()
                result = list()
                

                if re.findall(r"^ZB",sensor[j]) or re.findall(r"^M",sensor[j]) or re.findall(r"^F",sensor[j]) or re.findall(r"^D",sensor[j]) or (re.findall(r"^L",sensor[j]) and not re.findall(r"^LL",sensor[j]) and not re.findall(r"^LS",sensor[j])):
                    for k in range(len(hour_table_vector)):
                        events.append(hour_table_vector[k][j+1])
                    result=discret_sensor(times,events,considerd_hour)
                
                else:
                    #print(sensor[j])
                    for k in range(len(hour_table_vector)):
                        events.append(int(hour_table_vector[k][j+1]))
                    result= sample_sensor(times,events,considerd_hour)

                for r in result:
                    feature_vector.append(r)

            act_time=activity_times(activities,considerd_hour)

                
            for r in act_time:
                feature_vector.append(r)
            

            feature_vector.insert(0,is_business_day(considerd_hour))
            feature_vector.insert(0,(considerd_hour-considerd_hour.replace(month=1,day=1)).days)
            
            feature_vector.insert(0,int((considerd_hour-considerd_hour.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()//60))

            employee_writer = csv.writer(file_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(feature_vector)
        else:
            pass
        cont+=1 
        #---------------------------------
         
    print("Finito creazione table con n: ",len(hour_table_vector))

    file_csv.close()


cursor.close()
connection.close()
