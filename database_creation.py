import mysql.connector
import datetime
mydb=mysql.connector.connect(host="localhost",user="root",passwd="nayankrishna13@gmail.com")
c=mydb.cursor()
c.execute("show databases")
l=c.fetchall()
for i in l:
   if i[0]=="railway":
      c.execute("drop database railway")
      mydb.commit()
c.execute("create database railway")
mydb.close()
def dates():
   import datetime
   from datetime import timedelta
   import random
   t_date=datetime.date.today()
   list_dates=[t_date]
   fut_date=t_date+timedelta(days=14)
   while t_date!=fut_date:      
      t_date+=timedelta(days=1)
      list_dates.append(t_date) 
   return list_dates  
def creation():
   import mysql.connector
   import random
   mydb=mysql.connector.connect(host="localhost",user="root",passwd="nayankrishna13@gmail.com",database="railway")
   c=mydb.cursor(prepared=True)
   c.execute('''create table routes(
                    train_id char(20),
                    cost float(20),
                    Starting_Location char(90),
                    Destination char(90),                   
                    Departure_date date)''')
   d=dates()
   #l=(),)
   l=[("2100",2000,"Ahemdabad","Delhi",random.choice(d)),("2102",2000,"Lucknow","Patna",random.choice(d)),
      ("2103",6000,"Trivandrum",'Delhi',random.choice(d)),
      ("2113",5000,"Goa","Chennai",random.choice(d)),
      ("2123",6000,"varanasi","Banglore",random.choice(d)),
      ("2023",3000,"Banaras","Lucknow",random.choice(d))]
      
   for i in l:
      c.execute("insert into routes(train_id,cost,Starting_Location,Destination,Departure_date) values (?,?,?,?,?)",i)
      mydb.commit()
creation() 
def feedback_table():
   import mysql.connector
   mydb=mysql.connector.connect(host="localhost",user="root",passwd="nayankrishna13@gmail.com",database="railway")
   c=mydb.cursor()
   c.execute('''create table feedback(
             comment char(120),
             author char(20),
             Date date)''')
feedback_table()
def menu_creation():   
   import mysql.connector
   mydb=mysql.connector.connect(host="localhost",user="root",passwd="nayankrishna13@gmail.com",database="railway")
   c=mydb.cursor(prepared=True)
   c.execute('''create table menu(
                sno integer,
                item char(200),
                cost integer(20))''')
   c.execute('''insert into menu values(1,'Traditonal Indian-Roti with lentils and other vegetables,along with bread and butter',200),
                (2,"Maharaja's Choice-Chicken Biryani along with lassi,vada pav",400),
                (3,'Western Classic-Hot dogs, Burgers,Pizza alongwith coke/pepsi',1000)''')
   mydb.commit()                
menu_creation()           
def passenger_list_creation():
   import mysql.connector
   mydb=mysql.connector.connect(host="localhost",user="root",passwd="nayankrishna13@gmail.com",database="railway")
   c=mydb.cursor()
   c.execute('''create table passenger_list(
                uniq_id char(50),
                passenger_name char(20),
                phone_no char(20),
                gender char(5),
                age integer,
                starting_location char(30),                
                destination char(30),
                train_id char(10),
                Total_cost integer,
                seating char(20),
                Departure_date date,
                Departure_Time time)''')                
passenger_list_creation()                

             
   



                    



                 
