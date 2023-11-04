import mysql.connector
import datetime
from tabulate import tabulate
import random
mydb=mysql.connector.connect(host="localhost",user="root",passwd="nayankrishna13@gmail.com",database='railway')
mycursor=mydb.cursor()
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
def reserve():
    mycursor1=mydb.cursor(prepared=True)
    mycursor1.execute("select* from routes")
    c1=mycursor1.fetchall()
    l1=[]
    for i in c1:
        l1.append(i)
    print("-------------------------------------------")
    print("Ticket Reservation")
    n=input("Refer to the table given under train details and carefully enter the train id  mentioned with your selected route")
    starting_point=""
    destination=""                  
    n1=int(input("Enter the number of tickets required"))
    for i in l1:
        if i[0]==n:
            starting_point=i[2]
            destination=i[3]
            cost_of_ticket=i[1]
            train_id=i[0]
            t_date=i[4]
    if destination=="" or starting_point=="":
        c="INVALID INPUT"
        return c               
    total=cost_of_ticket*n1         
    d={}
    for i in range(n1):
        c=str(i+1)
        name2=input("Enter name Of passengers (including you if you are travelling)")
        age=int(input("Enter ages of passenger"))
        gender=input("Enter gender of passenger , m for male and f for female")
        d[name2]=[age,gender]
    count=0
    for i in d.values():
        if i[0]<=10:
            count+=1
    discount=count*100
    phno=input("Enter your phone number")
    print('''Which of the following seating compartments would you like?
             1.First Class
             2.Second Class
             3.Ac Sleeper
             4.General
             ''')
    ch=int(input("Enter adjacent no. of your selected compartment"))
    if ch==1:
        total+=500
        seating="First Class"
    elif ch==2:
        total+=250
        seating="Second  Class"
    elif ch==3:
        seating="Ac sleeper"
    elif ch==4:
        seating="General"
    else:
        print("Enter valid number for seating arrangement")
        reserve()
    total=total-discount
    food_choice=input("Would you like to experience our MEALS ON WHEELS facilities?Enter y for yes and n for no")
    if food_choice.lower()=='y':
        t=food()
        cost_of_food=t[1]*t[2]
        total+=cost_of_food
    from random import randint
    time=datetime.time(randint(0,24),randint(0,59),randint(0,59))
    mycursor1.execute("select count(passenger_name) from passenger_list")
    c=mycursor1.fetchall()    
    sno=str(c[0][0]+1)
    list_final=[]
    for i in d.keys():
        uniqid=sno+"-"+chr(random.randint(65,90))+chr(random.randint(65,90))+"-"+str(random.randint(1000,9999))
        mycursor1.execute("insert into passenger_list values(?,?,?,?,?,?,?,?,?,?,?,?)",(uniqid,i,phno,d[i][1],d[i][0],starting_point,destination,train_id,total,seating,t_date,time))
        list_final.append([uniqid,i,phno,d[i][1],d[i][0],starting_point,destination,train_id,total,seating,t_date,time])
    list_final_header=['UNIQID','NAME','PHONE NO.','GENDER','AGE','STARTING POINT','DESTINATION','TRAIN ID','TOTAL COST','SEATING','DEPARTURE DATE','DEPARTURE TIME']
    print(tabulate(list_final,headers=list_final_header,tablefmt="grid"))
    if food_choice.lower()=='y':
       print("Food Choice :",t[0])
       print("Number of meals :",t[2])
    choice=input("Enter y to confirm whether data is correct")
    print("KINDLY REMEMBER YOUR UNIQUE ID FOR ANY CANCELLATION OF TICKETS, IF LOST NO REFUND WILL BE POSSIBLE")
    if choice=='y':
        mydb.commit()
        intro()
    else:
        mydb.rollback()
        reserve()
def cancel():
    c=mydb.cursor(prepared=True)
    c.execute("select * from passenger_list")
    l=c.fetchall()
    n=input("Enter Passenger name")
    ch="y"
    while True:
            for i in l:
                if i[1].lower()==n.lower():
                    c1=input("Enter unique code given at the time of reservation.For example you code will be in the form 12-KC-2345")
                    query=("delete from passenger_list where uniq_id like %s")
                    if c1.lower()==i[0].lower():
                        c.execute(query,(c1,))
                        mydb.commit()
                    else:
                        print("Entered id entered was not found to be matching")                                     
                else:
                    print("Name not found")
                ch=input("Enter y if you wish to cancel another ticket and n for no")
                if ch=='y':
                    cancel()
                else:
                    intro()    
    
    
def food():
    from tabulate import tabulate
    mycursor=mydb.cursor()
    mycursor.execute("select * from menu")
    l1=mycursor.fetchall()
    l=[]
    for i in l1:
        l.append(i)
    head=["SNO.","ITEM","COST"]
    print(tabulate(l, headers=head, tablefmt="grid"))
    ch=input("Would you like to to pre book on any of the above items?Enter y for yes and no for n")
    if ch.lower()=='y':
        j=int(input("Enter the sno. of the food item of your choice"))
        num=int(input("Enter the number of meals required"))
        l2=[]
        for i in range(len(l)):
            if l[i][0]==j:
                l2.extend([l[i][1],l[i][2],num])
                return l2            
  
def train_details():
    from tabulate import tabulate
    print(" Availble rail routes are displayed below:")       
    mycursor.execute("select * from routes")
    c=mycursor.fetchall()
    l=[]
    for i in c:
        l.append(i)
    head=["SNO.","STARTING LOCATION","DESTINATION","COST","DATE OF DEPARTURE","TRAIN ID"]
    l=[]
    count=1
    for i in c:
        l.append([count,i[2],i[3],i[1],i[4],i[0]])
        count+=1
    print(tabulate(l, headers=head, tablefmt="grid"))
    r=input("Would you like to reserve a ticket for any of these routes? Enter y for yes and n for no")
    if r.lower()=='y':
        reserve()
    else:
        intro()
        
def feedback():
   c=mydb.cursor(prepared=True)
   s=input("Hello There! Tell us about your experience")
   if len(s)>120:
      print("Comments cannot be longer than 120 characters")
      feedback()        
   else:
       c2=input("Would you like to remain anonymous? Enter y for yes and n for no")
       n=""
       if c2.lower()=="n":
          n=input("Enter your name")
       else:
          n='Anonymous'
       t_date=datetime.date.today()
       l=(s,n,t_date)
       c.execute("insert into feedback(comment,author,Date) values(?,?,?)",l)
       mydb.commit()
def feedback_view():
    mycursor.execute("select * from feedback")
    c=mycursor.fetchall()
    l=[]
    for i in c:
        l.append(i)
    h=['Feedback','Author','DATE']
    print(tabulate(l,headers=h,tablefmt="grid"))
def display_passenger():
    mycursor.execute("select * from passenger_list")
    c=mycursor.fetchall()
    l=[]
    list_final_header=['UNIQID','NAME','PHONE NO.','GENDER','AGE','STARTING POINT','DESTINATION','TRAIN ID','TOTAL COST','SEATING','DEPARTURE DATE','DEPARTURE TIME']
    for i in c:
        l.append(i)
    print(tabulate(l,headers=list_final_header,tablefmt="grid"))
def update():
    print("Which of the following tables would you like to update?")
    print("1.Railway Routes")
    print("2.Meals on wheels menu")
    print("3.Passenger list")
    ch=int(input("Enter your choice"))
    if ch==1:
        print('''Press
                 1 to update
                 2 to delete elements
                 3 to add elements''')
        d=int(input("Enter your choice"))
        if d==1:
            print('''What would you like to update?
                     1.Train_id
                     2.Cost
                     3.Starting Location and destination
                     4.Departure date''')
            choice=int(input("Enter your choice"))
            if choice==1:
               mycursor.execute("select train_id from routes")
               routes=mycursor.fetchall()
               currentid=input("Enter current ID")
               for i in routes:
                   if i[0]==currentid:
                       newid=input("Enter new train_id")
                       query=('''update routes
                                           set train_id=%s
                                           where train_id=%s''')
                       mycursor.execute(query,(newid,currentid))
                       mydb.commit()
                       break
                   else:
                        print("Given tain_id is not availiable")
                        choice2=input("Enter y if you would like to add more updates and n if not")
                        if choice2=='y':
                            update()
                        else:
                            intro()
                
            elif choice==2:
                mycursor.execute("select cost,train_id from routes")
                cost=mycursor.fetchall()
                currentid=input("Enter current ID")
                newcost=int(input("Enter new cost"))
                for i in cost:
                   if i[1]==currentid:                       
                       query=('''update routes
                                           set cost=%s
                                           where train_id=%s''')
                       mycursor.execute(query,(newcost,currentid))
                       mydb.commit()
                       break
                   else:
                        print("Given train_id is not available")
                        choice2=input("Enter y if you would like to add more updates and n if not")
                        if choice2=='y':
                            update()
                        else:
                            intro()
            elif choice==3:
                mycursor.execute("select starting_location,destination,train_id from routes")
                cost=mycursor.fetchall()
                currentid=input("Enter current ID")
                newstarting=input("Enter starting location")
                destination=input("Enter destination")                
                for i in routes:
                   if i[2]==currentid:
                       query=('''update routes
                                           set starting_location=%s,destination=%s
                                           where train_id=%s''')
                       mycursor.execute(query,(newstarting,destination,currentid))
                       mydb.commit()
                       break
                   else:
                        print("Given train_id is not availiable")
                        choice2=input("Enter y if you would like to add more updates and n if not")
                        if choice2=='y':
                            update()
                        else:
                            intro()
            elif choice==4:
                mycursor.execute("select Departure_date,train_id from routes")
                date=mycursor.fetchall()
                currentid=input("Enter id of train")
                try:
                    from datetime import datetime
                    my_string = str(input('Enter date(yyyy-mm-dd): '))
                    my_date = datetime.strptime(my_string,"%Y-%m-%d")
                except ValueError:
                    print("Incorrect date format")
                    update()
                for i in date:
                    if i[1]==currentid:
                        query=('''update routes
                                           set departure_date=%s
                                           where train_id=%s''')
                        mycursor.execute(query,(my_date,currentid))
                        mydb.commit()
                        break
                    else:
                        print("Given train_id is not availiable")
                        choice2=input("Enter y if you would like to add more updates and n if not")
                        if choice2=='y':
                            update()
                        else:
                            intro()
        elif d==2:            
            mycursor.execute("select train_id from routes")
            c=mycursor.fetchall()
            for i in c:
                print(i)
            id1=input("Enter train_id of the route which you want to cancel")
            query=('''delete from routes
                  where train_id=%s''')
            mycursor.execute(query,(id1,))
            mydb.commit()
        
        elif d==3:            
            choice='y'
            d=dates()
            while True:
                train_id=input("Enter train id")
                cost=int(input("Enter cost"))
                starting_location=input("Enter the starting location")
                destination=input("Enter the destination")
                departure_date=random.choice(d)
                query=("insert into routes values(%s,%s,%s,%s,%s)")
                mycursor.execute(query,(train_id,cost,starting_location,destination,departure_date))
                mydb.commit()
                choice=input("Enter y if you would you like to add more routes and n if not")
                if choice!='y':
                    break
        else:
            print("invalid choice")
            intro()
    elif ch==2:
        mycursor.execute("select * from menu")
        c=mycursor.fetchall()
        for i in c:
            print(i)
        l=len(c)
        print('''press
                 1. To add
                 2. To delete
                 ''')
        choice=int(input("Enter your choice"))
        if choice==1:
            ct='y'
            while True:
                item=input("Enter item")
                cost=input("Enter cost")
                query=("insert into menu values(%s,%s,%s)")
                mycursor.execute(query,(l+1,item,cost))
                mydb.commit()
                l+=1
                ct=input("If you would like to enter more food items enter y , if not enter n")
                if ct!='y':
                    break
        elif choice==2:
            sno=int(input("Enter the sno of the food item you want to delete"))
            for i in c:
                if i[0]==sno:
                    query=("delete from menu where sno=%s")
                    mycursor.execute(query,(sno,))
                    mydb.commit()
                    break
                else:
                    if c[len(c)-1]==i:                        
                        print("No such item found ")
                        intro()         
        else:
            print("Invalid choice")
            intro()
    elif ch==3:
       mycursor.execute("select * from passenger_list")
       c=mycursor.fetchall()
       for i in c:
          print(i)
       currentid=input("Enter the id of the user")
       for i in c:
          if i[0]==currentid:
             query=("delete from passenger_list where uniq_id=%s")
             mycursor.execute(query,(currentid,))
             mydb.commit()
             break
          else:
             if c[len(c)-1]==i:
               print("No such item found ")
               intro()       
    
def intro():
    print("1. User Mode(for customers)                      2.Administrator Mode")
    print("Which mode do you prefer?")
    c=int(input("Enter 1 for User mode and 2 for administrator mode"))
    if c==1:
        print('''Welcome To The Indian Railways!!!       
                1.Train Detail
                2.Reservation of Ticket
                3.Cancellation of Ticket
                4.Give us Feedback
                5.Quit''')           
        ch=int(input("Enter the number given with option"))
        if ch==1:
            train_details()
        elif ch==2:
            reserve()                
        elif ch==3:
            cancel()
        elif ch==4:
            feedback()
        elif ch==5:           
           print("exit")      
        else:
            print("Invalid Choice")
    elif c==2:
        password=input("Enter administrator password")
        if password=="alphabravocharlie123":
            print("1.Display list of passengers")
            print("2.Update information tables")
            print("3.View feedback")
            ch=int(input("Enter the number given woth your option"))
            if ch==1:
                display_passenger()
            elif ch==2:
                update()
            elif ch==3:               
                feedback_view()
            else:
               print("Invalid Input")
               intro()               
        else:
            print("incorrect password")
            intro()
    else:
       print("Invalid Input")
try:
   intro()
except Exception:
   print("INVALID INPUT")
   intro()

    
   
 

            
        
        
            










