import mysql.conncector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="nayankrishna13@gmail.com")
mycursor=mydb.cursor()
mycursor.execute("create database railway")
mycursor.execute('''create table routes(
                    Starting_Location char(90),
                    Destination char(90),
                    Departure_date date)''')
mycursor.execute('''insert into railway values("
                    



                 
