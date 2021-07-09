import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime
import csv
import pandas as pd


a101 = ['Morning_Meds','Read','Cook_Lunch','Eat_Dinner','Eat_Breakfast','Phone','Groom','Wash_Lunch_Dishes','Eat_Lunch','Eat','Cook']
a102 = ['Eat_Dinner', 'Bathe', 'Morning_Meds', 'Wash_Lunch_Dishes', 'Eat_Breakfast','Eat','Wash_Dishes','Watch_TV', 'Work_At_Table','Wash_Breakfast_Dishes','Take_Medicine']
a103 = ['Morning_Meds', 'Sleep', 'Eat_Lunch','Eat_Dinner', 'Eat_Breakfast', 'Read','Work_At_Table', 'Relax','Cook_Breakfast','Phone','Sleep_Out_Of_Bed']
a104 = ['Morning_Meds', 'Wash_Dishes', 'Dress','Cook_Lunch', 'Work_At_Table', 'Eat_Breakfast', 'Phone', 'Groom', 'Wash_Dinner_Dishes', 'Cook_Breakfast', 'Wash_Breakfast_Dishes', 'Sleep_Out_Of_Bed', 'Wash_Lunch_Dishes', 'Take_Medicine', 'Entertain_Guests', 'Eat_Dinner']
a105 = ['Eat_Dinner', 'Eat_Breakfast', 'Cook_Breakfast', 'Eat_Lunch', 'Groom', 'Wash_Dishes', 'Evening_Meds', 'Wash_Breakfast_Dishes','Wash_Lunch_Dishes','Wash_Dinner_Dishes']
a106 = ['Wash_Dinner_Dishes', 'Work_At_Table','Eat_Dinner', 'Wash_Dishes', 'Eat_Breakfast', 'Eat_Lunch', 'Wash_Lunch_Dishes', 'Cook_Lunch','Work', 'Cook', 'Entertain_Guests', 'Relax', 'Eat', 'Groom', 'Evening_Meds' ]
a108 = ['Wash_Lunch_Dishes','Read', 'Morning_Meds', 'Entertain_Guests', 'Cook', 'Eat', 'Eat_Dinner', 'Wash_Dishes', 'Evening_Meds', 'Eat_Lunch', 'Eat_Breakfast','Groom']
a109 = ['Eat_Lunch', 'Evening_Meds', 'Cook', 'Read', 'Bathe', 'Eat_Breakfast', 'Eat_Dinner', 'Wash_Breakfast_Dishes', 'Relax', 'Eat', 'Take_Medicine', 'Entertain_Guests', 'Work', 'Wash_Dishes', 'Groom', 'Phone']
a110 = ['Dress', 'Eat_Dinner', 'Eat_Breakfast', 'Sleep_Out_Of_Bed', 'Cook_Dinner', 'Drink', 'Wash_Dinner_Dishes']
a111 = ['Wash_Dishes','Wash_Dinner_Dishes','Cook_Breakfast','Morning_Meds','Work_At_Desk','Eat_Breakfast','Evening_Meds','Eat_Dinner','Phone','Work_At_Table','Wash_Lunch_Dishes','Eat_Lunch','Cook','Groom','Work','Eat']
a112 = ['Read','Work_At_Table','Cook_Lunch','Wash_Dinner_Dishes','Cook','Relax','Wash_Breakfast_Dishes','Wash_Dishes','Eat_Lunch','Eat','Eat_Breakfast','Eat_Dinner','Entertain_Guests','Morning_Meds','Wash_Lunch_Dishes']
a113 = ['Read', 'Entertain_Guests', 'Eat_Lunch','Cook_Dinner','Wash_Lunch_Dishes','Cook_Lunch','Eat_Dinner','Watch_TV','Eat','Eat_Breakfast', 'Wash_Dinner_Dishes','Cook','Work','Sleep_Out_Of_Bed']
a114 = ['Eat_Breakfast', 'Relax', 'Cook_Lunch', 'Eat_Lunch', 'Eat_Dinner', 'Wash_Lunch_Dishes', 'Take_Medicine', 'Bathe', 'Step_Out']
a116 = ['Eat_Breakfast', 'Bathe', 'Take_Medicine', 'Phone', 'Cook_Breakfast', 'Morning_Meds', 'Work_On_Computer', 'Eat_Lunch', 'Eat_Dinner', 'Work_At_Table', 'Watch_TV', 'Eat', 'Relax', 'Read','Groom']
a117 = ['Morning_Meds', 'Cook_Breakfast', 'Cook', 'Eat', 'Bathe', 'Wash_Lunch_Dishes', 'Work', 'Evening_Meds', 'Phone', 'Sleep_Out_Of_Bed', 'Groom', 'Relax', 'Wash_Breakfast_Dishes', 'Work_At_Table', 'Eat_Breakfast']
a118 = ['Eat_Breakfast', 'Watch_TV', 'Dress', 'Phone', 'Cook_Breakfast', 'Enter_Home', 'Leave_Home', 'Sleep', 'Housekeeping', 'Groom', 'Wash_Dishes']
a119 = ['Entertain_Guests', 'Work_At_Table', 'Phone', 'Wash_Dishes', 'Evening_Meds', 'Morning_Meds', 'Eat_Dinner', 'Sleep_Out_Of_Bed', 'Read','Step_Out']
a120 = ['Eat_Breakfast', 'Read', 'Eat', 'Work_At_Table', 'Eat_Lunch', 'Cook', 'Sleep_Out_Of_Bed', 'Cook_Breakfast', 'Cook_Dinner', 'Phone', 'Eat_Dinner', 'Wash_Dinner_Dishes', 'Relax', 'Wash_Breakfast_Dishes', 'Cook_Lunch', 'Groom', 'Wash_Lunch_Dishes']
a122 = ['Work', 'Relax', 'Read', 'Phone', 'Cook_Dinner', 'Entertain_Guests', 'Wash_Lunch_Dishes', 'Wash_Dishes', 'Eat', 'Cook_Breakfast', 'Eat_Dinner', 'Bathe', 'Work_At_Table', 'Cook_Lunch', 'Cook']
a123 = ['Wash_Lunch_Dishes', 'Cook_Lunch', 'Eat_Dinner', 'Eat_Lunch', 'Wash_Breakfast_Dishes', 'Cook', 'Relax', 'Entertain_Guests']
a124 = ['Personal_Hygiene', 'Work', 'Dress', 'Wash_Breakfast_Dishes', 'Wash_Dishes', 'Work_On_Computer', 'Cook_Dinner', 'Sleep', 'Work_At_Table', 'Eat_Dinner']
a125 = ['Morning_Meds', 'Step_Out', 'Cook_Breakfast', 'Work', 'Relax', 'Take_Medicine', 'Read', 'Eat_Dinner', 'Phone', 'Sleep', 'Entertain_Guests', 'Cook', 'Bathe', 'Eat_Breakfast', 'Wash_Lunch_Dishes', 'Eat']
a126 = ['Step_Out', 'Cook_Lunch', 'Phone', 'Wash_Dishes', 'Wash_Lunch_Dishes', 'Wash_Dinner_Dishes', 'Morning_Meds', 'Eat_Dinner', 'Eat_Breakfast', 'Wash_Breakfast_Dishes', 'Relax', 'Eat_Lunch', 'Sleep_Out_Of_Bed']
a127 = ['Wash_Dishes', 'Bathe', 'Step_Out', 'Eat_Lunch', 'Sleep_Out_Of_Bed', 'Work_At_Table', 'Eat_Breakfast','Eat']
a128 = ['Evening_Meds', 'Cook', 'Eat_Breakfast', 'Take_Medicine', 'Entertain_Guests', 'Eat_Dinner', 'Groom', 'Wash_Lunch_Dishes', 'Eat', 'Eat_Lunch', 'Cook_Lunch','Step_Out']
a129 = ['Eat_Dinner', 'Cook', 'Wash_Dinner_Dishes', 'Step_Out', 'Wash_Lunch_Dishes', 'Sleep_Out_Of_Bed', 'Wash_Dishes', 'Evening_Meds', 'Eat_Lunch', 'Relax', 'Eat', 'Work_At_Desk', 'Phone']
a130 = ['Cook_Lunch', 'Work_At_Table', 'Bathe', 'Wash_Dishes', 'Step_Out', 'Cook', 'Work', 'Eat_Lunch', 'Eat']

case=['HH130']


attivita_sbagliate=a130



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



pezzo_query="and name not in("
print(len(attivita_sbagliate))
for act in attivita_sbagliate:
    pezzo_query+="'"+act+"'"
    if act!=attivita_sbagliate[-1]:
        pezzo_query+=","
pezzo_query+=')'


w=0

house=case[w]
house2=house.lower()
print("Casa ", house)

dataset=createDataset("formatted"+house2+".txt")#Creo il dataset
sensor=create_sensor()#Creo i sensori
activities=create_activity()#Creo le attivita

start_time=dataset[0][0]#Orario primo evento
end_time=dataset[-1][0]#Orario ultimo evento


start_time=datetime.datetime.strptime(dataset[0][0]+" "+dataset[0][1], '%Y-%m-%d %H:%M:%S.%f')#Orario evento

k=0
i=0

appHour=start_time.strftime("%H:%M:%S")

print("Inizio creazione table")
cont=0
cont2=-1
cont3=0

da_cambiare_att  = list()
da_cambiare_riga = list()

while i<len(dataset):

    cont2+=1
    

    start_time=datetime.datetime.strptime(dataset[i][0]+" "+dataset[i][1], '%Y-%m-%d %H:%M:%S.%f')
    
    query="select id,name from activity.activity where house='"+house+"' AND startdate>'"+(start_time+datetime.timedelta(0, 60*60)).strftime("%Y-%m-%d %H:%M:%S")+"' order by id"
    cursor.execute(query)
    
    try:
        risp1=cursor.fetchone()[1]
        #print(risp1, start_time)

    except:
        break
    
    try:
        if risp1 in attivita_sbagliate:
            risp=cursor.fetchone()[1]
            while risp in attivita_sbagliate:
                risp=cursor.fetchone()[1]
            #print(cont2+2, '\t',risp1,'\t' ,start_time+datetime.timedelta(0, 60*60),'\t', risp)
            da_cambiare_att.append(risp)
            da_cambiare_riga.append(cont2)
            #print(cont2+2,risp)
            cont3+=1
    except:
        break
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

print(cont3)
print(da_cambiare_riga)


file_csv_write=open("feature_vector_new"+house+".csv","w",newline="")

cont5=0
with open('feature_vector'+house+'.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if cont5<len(da_cambiare_riga):
            if da_cambiare_riga[cont5]+1==line_count:
                row[-1]=da_cambiare_att[cont5]
                cont5+=1

        employee_writer = csv.writer(file_csv_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(row)
        line_count += 1
    print(f'Processed {line_count} lines.')


cursor.close()
connection.close()
