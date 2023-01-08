"""
To arxeio functions apoteleitai apo tiw aparaithtes sunarthseis gia thn swsth
leitourgia tou main mas programmatos
"""

import sqlite3 as sql
import pandas as pd


database = "restaurant.db"
connection = sql.connect(database)
connection.execute("PRAGMA foreign_keys = 1")
cursor = connection.cursor()

#------------------------------------------------------------------------------------------------------
def create_order(dishes):
    """dishes = {dish_id:quantity,...}
        dish_id should be integer
        quantity should be a number"""
    print("Payment method:")
    payment_method = input()
    cost = 0
    try:
        if cursor.execute("SELECT COUNT(*) FROM RESTAURANT_ORDER").fetchone()[0] != 0:
            cursor.execute(f"INSERT INTO RESTAURANT_ORDER(payment_method,cost) VALUES('{payment_method}',{cost})")
        else:
            cursor.execute(f"INSERT INTO RESTAURANT_ORDER(order_number,payment_method,cost) VALUES({0},'{payment_method}',{cost})")
            
        order_number = cursor.execute("SELECT order_number FROM RESTAURANT_ORDER ORDER BY order_number DESC LIMIT 1").fetchone()[0]
        for d,q in dishes.items():
            cursor.execute(f"INSERT INTO CONSISTS VALUES({order_number},{d},{q})")
            cost += q*cursor.execute(f"SELECT cost FROM DISH WHERE id = {d}").fetchone()[0]
        cursor.execute(f"UPDATE RESTAURANT_ORDER SET cost = {cost} WHERE order_number={order_number}")
    except sql.Error as err:
        cursor.execute(f"DELETE FROM RESTAURANT_ORDER WHERE order_number = {order_number}")
        cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ= 0 WHERE NAME='RESTAURANT_ORDER'")
        print("Error occured calling the create_order() function")
        if 'FOREIGN' in str(err):
            print("One or more dishes don't exist in the DISH table!")
        else:
            print("Insert parameters with the proper types!")
    connection.commit()
    return order_number

#------------------------------------------------------------------------------------------------------
def create_employee(tin,name,role,sex,birthday,email,address,phone_number,salary):

    if cursor.execute("SELECT COUNT(*) FROM EMPLOYEE").fetchone()[0]== 0:
        cursor.execute(f"INSERT INTO EMPLOYEE(tin,name,role,sex,birthday\
                        ,email,address,phone_number,salary) VALUES (?,?,?,?,?,?,?,?,?)",(tin,name,role,sex,birthday,email,address,phone_number,salary))
        print("Employee created Successful")

    else:
        check = cursor.execute("SELECT * FROM EMPLOYEE WHERE tin=? ",(tin,)).fetchall()
        
        if check:
            print("Same Tin with another Employee")
        else:   
            cursor.execute(f"INSERT INTO EMPLOYEE(tin,name,role,sex,birthday\
                            ,email,address,phone_number,salary)VALUES (?,?,?,?,?,?,?,?,?)",(tin,name,role,sex,birthday,email,address,phone_number,salary))
            print("Employee created Successful")
    cursor.execute("SELECT * FROM EMPLOYEE")
    print(cursor.fetchall())

    connection.commit()

#------------------------------------------------------------------------------------------------------ 
def create_customer(name,phone_number,email):

    if cursor.execute("SELECT COUNT(*) FROM CUSTOMER").fetchone()[0]== 0:
        cursor.execute(f"INSERT INTO CUSTOMER(id,name,phone_number,email)\
                       VALUES ('1',?,?,?)",(name,phone_number,email))
        print("Customer created Successful")

    else:
        cursor.execute(f"INSERT INTO CUSTOMER(name,phone_number,email)\
                        VALUES (?,?,?)",(name,phone_number,email))
        print("Customer created Successful")
    cursor.execute("SELECT * FROM CUSTOMER")
    print(cursor.fetchall())

    connection.commit()
    
#------------------------------------------------------------------------------------------------------        
def create_table(capacity):

    if cursor.execute("SELECT COUNT(*) FROM RESTAURANT_TABLE").fetchone()[0]== 0:
        cursor.execute(f"INSERT INTO RESTAURANT_TABLE(table_number,capacity)\
                       VALUES (1,?)",(capacity,))
        print("Restaurant Table created Successful")

    else:
        cursor.execute(f"INSERT INTO RESTAURANT_TABLE(capacity)\
                        VALUES (?)",(capacity,))
        print("Restaurant Table created Successful")

        
    cursor.execute("SELECT * FROM RESTAURANT_TABLE")
    print(cursor.fetchall())

    connection.commit()

#------------------------------------------------------------------------------------------------------        
def add_reservation(name,date,time,phone_number,people):
    
    if cursor.execute("SELECT COUNT(*) FROM RESERVATION").fetchone()[0] == 0:
        cursor.execute( f"INSERT INTO RESERVATION(reservation_number,date,phone_number,people,time,name)\
                    VALUES (1,'{date}','{phone_number}','{people}','{time}','{name}')")
        reservation_num = cursor.execute("SELECT reservation_number FROM RESERVATION ORDER BY reservation_number DESC LIMIT 1").fetchone()
        
        if cursor.execute("SELECT COUNT(*) FROM RESTAURANT_TABLE").fetchone()[0] !=0:
            try:
                reserved_table = cursor.execute("SELECT table_number FROM RESTAURANT_TABLE WHERE capacity>=? \
                                            and state='free'",people,).fetchone()

                state='reserved'
                cursor.execute('''UPDATE RESTAURANT_TABLE SET state =? WHERE table_number=?''',(state,reserved_table[0]))
                print("Your Reservation created Succefully")
            except:
                print("No tables available or too much people")
                cursor.execute("DELETE FROM RESERVATION WHERE reservation_number=?",reservation_num,)
                print("Your Reservation deleted SuccessullyS")

                           
        else:
            print("Error....No Restaurant_Tables in your Database,delete your reservation")
            cursor.execute("DELETE FROM RESERVATION WHERE reservation_number=?",reservation_num,)
            print("Your Reservation deleted Successully")

            
    else:
        cursor.execute( f"INSERT INTO RESERVATION(date,phone_number,people,time,name)\
                    VALUES ('{date}','{phone_number}','{people}','{time}','{name}')")
        
        reservation_num = cursor.execute("SELECT reservation_number FROM RESERVATION ORDER BY reservation_number DESC LIMIT 1").fetchone()
                
        if cursor.execute("SELECT COUNT(*) FROM RESTAURANT_TABLE").fetchone()[0] !=0:
            try:
                reserved_table = cursor.execute("SELECT table_number FROM RESTAURANT_TABLE WHERE capacity>=? \
                                                and state='free'",people,).fetchone()

                state='reserved'
                cursor.execute('''UPDATE RESTAURANT_TABLE SET state =? WHERE table_number=?''',(state,reserved_table[0]))
                print("Your Reservation created Succefully")
            except:
                print("No tables available or too much people")
                cursor.execute("DELETE FROM RESERVATION WHERE reservation_number=?",reservation_num,)
                print("Your Reservation deleted Successully")
        else:
            print("Error....No Restaurant_Tables in your Database,delete your reservation")
            cursor.execute("DELETE FROM RESERVATION WHERE reservation_number=?",reservation_num,)
            print("Your Reservation deleted Successully")


    cursor.execute("SELECT * FROM RESERVATION")
    print(cursor.fetchall())

    cursor.execute("SELECT * FROM RESTAURANT_TABLE")
    print(cursor.fetchall())

    connection.commit()
    
#------------------------------------------------------------------------------------------------------
def add_supplier(tin,name,phone_number,address,email = None):
    """
    tin should be integer
    phone_number should be integer
    """
    try:
        if email == None:
            query = f"INSERT INTO SUPPLIER(tin,name,phone_number,address) VALUES({tin},'{name}',{phone_number},'{address}')"
            cursor.execute(query)
            print("Supplier created Successfully")
        else:           
            query = f"INSERT INTO SUPPLIER VALUES({tin},'{name}',{phone_number},'{address}','{email}')"
            cursor.execute(query)
            print("Supplier created Successfully")
    except sql.Error as err:
        print("Error occured calling add_supplier() function")
        if 'UNIQUE' in str(err):
            print("A supplier with the given tin already exists!")
        else:
            print("Insert parameters with the proper types!")

    cursor.execute("SELECT * FROM SUPPLIER")
    print(cursor.fetchall())
    
    connection.commit()
    
#------------------------------------------------------------------------------------------------------
def create_dish(ingredients,dish_id,name,category,cost):
    """ingredients = {ingredient_id:quantity,...}
            ingredient_id should be integer
            quantity should be a number
       dish_id should be integer type
       cost should be a number"""
    try:
        cursor.execute(f"INSERT INTO DISH VALUES({dish_id},'{name}','{category}',{cost})")
        for i,q in ingredients.items():
            cursor.execute(f"INSERT INTO MADE_OF VALUES({dish_id},{i},{q})")
    except sql.Error as err:
        print("Error occured calling create_dish() function")
        if 'UNIQUE' in str(err):
            print("A dish with the given id already exists!")
        elif 'FOREIGN' in str(err):
            print("One or more of the ingredients don't exist in the INGREDIENT table!")
        else:
            print("Insert parameters with the proper types!")


    cursor.execute("SELECT * FROM DISH")
    print(cursor.fetchall())
    cursor.execute("SELECT * FROM MADE_OF")
    print(cursor.fetchall())
    
    connection.commit()
    
#------------------------------------------------------------------------------------------------------
def order_ingredients(ingredients,supplier_tin):
    """ingredients is a dictionary with the following format 
        ingredients = {id:[name,category,quantity,cost_per_unit,expiration_date],...}
            quantity should be integer
            cost_per_unit should be a number
        supplier_tin should be integer 
    """
    try:
        if cursor.execute("SELECT COUNT(*) FROM INGREDIENT_ORDER").fetchone()[0] != 0:
            cursor.execute(f"INSERT INTO INGREDIENT_ORDER(supplier_tin,cost) VALUES({supplier_tin},{0})")
            order_id = cursor.execute("SELECT id FROM INGREDIENT_ORDER ORDER BY id DESC LIMIT 1").fetchone()[0]
        else:
            cursor.execute(f"INSERT INTO INGREDIENT_ORDER(id,supplier_tin,cost) VALUES({1},{supplier_tin},{0})")
            order_id = 1
        for k,v in ingredients.items():    
            cursor.execute(f"INSERT INTO INGREDIENT_INCLUDED_IN_ORDER VALUES({k},{order_id},'{v[0]}','{v[1]}',{v[2]},{v[3]},'{v[4]}')")
        cost = cursor.execute(f"SELECT SUM(cost_per_unit*quantity) FROM INGREDIENT_INCLUDED_IN_ORDER WHERE ingredient_order_id = {order_id}").fetchone()[0]
        cursor.execute(f"UPDATE INGREDIENT_ORDER SET cost = {cost} WHERE id = {order_id}")
    except sql.Error as err:
        print("Error occured calling order_ingredients() function")
        if 'FOREIGN' in str(err):
            print("There is no supplier with the given tin in SUPPLIER table!")
        else:
            print("Insert parameters with the proper types!")

    cursor.execute("SELECT * FROM INGREDIENT_ORDER")
    print(cursor.fetchall())        

    connection.commit()
    
#------------------------------------------------------------------------------------------------------
def employee_handle_table():

    if cursor.execute("SELECT COUNT(*) FROM RESTAURANT_TABLE").fetchone()[0] == 0:
        print("No tables in your database")

    else:
        tables = cursor.execute("SELECT table_number FROM RESTAURANT_TABLE").fetchall()
        tables_list = []
        for i in tables:
            tables_list.append(i[0])
        print(tables_list)
        print("Select table to handle:")
        table_num = int(input())
        while table_num not in tables_list:
            print("Wrong Number...Try again")
            table_num = int(input())


        tins = cursor.execute("SELECT tin FROM EMPLOYEE ")
        tins_list=[]
        for j in tins:
            tins_list.append(j[0])
        print(tins_list)
        print("Give the tin of the employee:")
        tin_in = int(input())
        while tin_in not in tins_list:
            print("Wrong Number...Try again")
            tin_in = int(input())
        print("Starting time:")
        start_time = input()
        print("Ending time")
        end_time = input()
        print("Date:")
        date = input()
        check = cursor.execute("SELECT * FROM HANDLES WHERE start_time=? AND end_time=? AND date=? \
                        AND table_number=? AND employee_tin=?",(start_time,end_time,date,table_num,tin_in)).fetchall()
        
        if check:
            print("This data is already in our base")
        else:
            cursor.execute(f"INSERT INTO HANDLES (start_time,end_time,date,table_number,employee_tin) \
                         VALUES (?,?,?,?,?)",(start_time,end_time,date,table_num,tin_in))



    cursor.execute("SELECT * FROM HANDLES")
    print(cursor.fetchall())


    connection.commit()

#------------------------------------------------------------------------------------------------------
def create_outside_order(dishes,name,phone_number,email=None,street=None,floor=None,number=None,area=None,customer_id=None):
    """dishes = {dish_id:quantity,...}
        dish_id should be integer
        quantity should be a number"""
    try:
        order_number = create_order(dishes)
        if customer_id == None:
            create_customer(name, phone_number, email)
            customer_id = cursor.execute("SELECT id FROM CUSTOMER ORDER BY id DESC LIMIT 1").fetchone()[0]  
        cursor.execute("INSERT INTO OUTSIDE_ORDER VALUES(?,?,?,?,?,?)",(order_number,street,floor,number,area,customer_id,))
    except:
        print("Error occured calling the function create_outside_order()")
        cursor.execute(f"DELETE FROM RESTAURANT_ORDER WHERE order_number = {order_number}")
        cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ= 0 WHERE NAME='RESTAURANT_ORDER'")
    connection.commit()
    
#------------------------------------------------------------------------------------------------------
def confirm_ingredient_order_arrival(order_id):
    state = cursor.execute(f"SELECT state FROM INGREDIENT_ORDER WHERE id = {order_id}").fetchone()[0]
    if state == 'finished':
        print("\nOrder already marked as finished!\n")
    else:
        cursor.execute(f"UPDATE INGREDIENT_ORDER SET state = 'finished',arrival_date = (date('now','localtime')),arrival_time = (time('now','localtime')) WHERE id = {order_id}")
        arrived_ingredients = cursor.execute(f"SELECT * FROM INGREDIENT_INCLUDED_IN_ORDER WHERE ingredient_order_id = {order_id}").fetchall()
        for i in arrived_ingredients:
            if cursor.execute(f"SELECT COUNT(*) FROM INGREDIENT WHERE id = {i[0]}").fetchone()[0] == 0:
                cursor.execute(f"INSERT INTO INGREDIENT VALUES({i[0]},'{i[2]}','{i[3]}',{i[4]},'plenty','{i[6]}')")
            else:
                cursor.execute(f"""
                UPDATE INGREDIENT 
                SET quantity = quantity + (SELECT quantity FROM INGREDIENT_INCLUDED_IN_ORDER WHERE ingredient_order_id = {order_id} AND ingredient_id = {i[0]})
                ,expiration_date = (SELECT expiration_date FROM INGREDIENT_INCLUDED_IN_ORDER WHERE ingredient_order_id = {order_id} AND ingredient_id = {i[0]})
                WHERE id = {i[0]}
                """)

    cursor.execute("SELECT * FROM INGREDIENT")
    print(cursor.fetchall())
    connection.commit()
    
#------------------------------------------------------------------------------------------------------
def create_inside_order(table_number,dishes):
    """dishes = {dish_id:quantity,...}
        dish_id should be integer
        quantity should be a number
        table _number should be a number"""
    try:
        order_number = create_order(dishes)
        cursor.execute(f"INSERT INTO INSIDE_ORDER VALUES({order_number},{table_number})")
    except:
        print("Error occured calling the function create_inside_order()")
        cursor.execute(f"DELETE FROM RESTAURANT_ORDER WHERE order_number = {order_number}")
        cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ= 0 WHERE NAME='RESTAURANT_ORDER'")
    connection.commit()
       
#------------------------------------------------------------------------------------------------------
def clear_reserved_tables():

    if cursor.execute("SELECT COUNT(*) FROM RESTAURANT_TABLE").fetchone()[0] == 0:
        print("No tables in your database")
        
    else:
        if cursor.execute("SELECT COUNT(*) FROM RESTAURANT_TABLE WHERE \
                            state='reserved'").fetchone()[0]==0:
            print("All the tables are free")
            
        else:
 
            reserved_tables_num = cursor.execute("SELECT table_number FROM RESTAURANT_TABLE WHERE state='reserved'").fetchall()
            print("The reserved table numbers are:" +','.join([str(i[0]) for i in reserved_tables_num]))
            print("Which table want to make free:")
            num = int(input())
            reserved_tables = []
            for i in reserved_tables_num:
                reserved_tables.append(i[0])
                
            while num not in reserved_tables:
                print("Wrong Number...Try again")
                num = int(input())
            state='free'
            cursor.execute('''UPDATE RESTAURANT_TABLE SET state=? WHERE \
                            table_number=?''',(state,num))
            print("Table number "+ str(num) +" is now free")
    connection.commit()

#------------------------------------------------------------------------------------------------------
def ingredient_orders_summary(start_date,end_date=None):
    if end_date ==None:
        print(f"From {start_date} :")
        print(cursor.execute(f"SELECT COUNT(*) FROM INGREDIENT_ORDER WHERE  date >= '{start_date}'").fetchone()[0],"ingredient orders where created.")
        print("The total cost of all the ingredient orders is ",cursor.execute(f"SELECT SUM(cost) FROM INGREDIENT_ORDER WHERE  date >= '{start_date}'").fetchone()[0],"euros")
        print(cursor.execute(f"SELECT COUNT(*) FROM INGREDIENT_ORDER WHERE state = 'processing' AND date >= '{start_date}'").fetchone()[0],"ingredient orders have not arrived yet.")
    else:
        print(f"From {start_date} to {end_date}:")
        print(cursor.execute(f"SELECT COUNT(*) FROM INGREDIENT_ORDER WHERE  date >= '{start_date}' AND date <= '{end_date}'").fetchone()[0],"ingredient orders where created.")
        print("The total cost of all the ingredient orders is ",cursor.execute(f"SELECT SUM(cost) FROM INGREDIENT_ORDER WHERE  date >= '{start_date}' AND date <= '{end_date}'").fetchone()[0],"euros")
        print(cursor.execute(f"SELECT COUNT(*) FROM INGREDIENT_ORDER WHERE state = 'processing' AND date >= '{start_date}' AND date <= '{end_date}'").fetchone()[0],"ingredient orders have not arrived yet.")

#------------------------------------------------------------------------------------------------------
def assign_delivery(order_number,employee_tin):
    try:
        cursor.execute(f"INSERT INTO DELIVER(order_number,employee_tin) VALUES({order_number},{employee_tin})")
        cursor.execute(f"UPDATE RESTAURANT_ORDER SET state = 'on the way' WHERE order_number = {order_number}")
    except:
        print("Error occured calling assign_delivery() function ")
        print("The order_number or the employee_tin do not exist.")
    connection.commit()

#------------------------------------------------------------------------------------------------------
def not_finished_restaurant_orders():
    print("Not finished orders:")
    nf_orders = cursor.execute("SELECT order_number FROM RESTAURANT_ORDER WHERE state != 'finished'").fetchall()
    for i in range(0,len(nf_orders)):
        print(nf_orders[i][0],end=" ")
    connection.commit()

#------------------------------------------------------------------------------------------------------
def restaurant_orders_summary(start_date,end_date=None):
    if end_date == None:
        print(f"From {start_date}:")
        print(cursor.execute(f"SELECT COUNT(*) FROM RESTAURANT_ORDER WHERE date >= '{start_date}'").fetchone()[0],"orders where created.")
        print("From these,",cursor.execute(f"SELECT COUNT(*) FROM RESTAURANT_ORDER WHERE date >= '{start_date}'\
             AND EXISTS (SELECT * FROM OUTSIDE_ORDER WHERE RESTAURANT_ORDER.order_number = OUTSIDE_ORDER.order_number)").fetchone()[0],"where outside orders and",\
             cursor.execute(f"SELECT COUNT(*) FROM RESTAURANT_ORDER WHERE date >= '{start_date}'\
             AND EXISTS (SELECT * FROM INSIDE_ORDER WHERE RESTAURANT_ORDER.order_number = INSIDE_ORDER.order_number) ").fetchone()[0],"where inside orders.")
        print("The total earnings from all the orders is",cursor.execute(f"SELECT SUM(cost) FROM RESTAURANT_ORDER WHERE date >= '{start_date}'").fetchone()[0],"euros")
        print("The earnings from outside orders is",cursor.execute(f"SELECT SUM(cost) FROM RESTAURANT_ORDER WHERE date >= '{start_date}'\
             AND EXISTS (SELECT * FROM OUTSIDE_ORDER WHERE RESTAURANT_ORDER.order_number = OUTSIDE_ORDER.order_number)").fetchone()[0],\
             "and from inside orders",cursor.execute(f"SELECT SUM(cost) FROM RESTAURANT_ORDER WHERE date >= '{start_date}'\
             AND EXISTS (SELECT * FROM INSIDE_ORDER WHERE RESTAURANT_ORDER.order_number = INSIDE_ORDER.order_number) ").fetchone()[0],"euros.")
    else:
        print(f"From {start_date} to {end_date}:")
        print(cursor.execute(f"SELECT COUNT(*) FROM RESTAURANT_ORDER WHERE date >= '{start_date}' AND date <= '{end_date}'").fetchone()[0],"orders where created.")
        print("From these,",cursor.execute(f"SELECT COUNT(*) FROM RESTAURANT_ORDER WHERE date >= '{start_date}' AND date <= '{end_date}'\
             AND EXISTS (SELECT * FROM OUTSIDE_ORDER WHERE RESTAURANT_ORDER.order_number = OUTSIDE_ORDER.order_number)").fetchone()[0],"where outside orders and",\
             cursor.execute(f"SELECT COUNT(*) FROM RESTAURANT_ORDER WHERE date >= '{start_date}' AND date <= '{end_date}'\
             AND EXISTS (SELECT * FROM INSIDE_ORDER WHERE RESTAURANT_ORDER.order_number = INSIDE_ORDER.order_number) ").fetchone()[0],"where inside orders.")
        print("The total earnings from all the orders is",cursor.execute(f"SELECT SUM(cost) FROM RESTAURANT_ORDER WHERE date >= '{start_date}' AND date <= '{end_date}'").fetchone()[0],"euros")
        print("The earnings from outside orders is",cursor.execute(f"SELECT SUM(cost) FROM RESTAURANT_ORDER WHERE date >= '{start_date}' AND date <= '{end_date}'\
             AND EXISTS (SELECT * FROM OUTSIDE_ORDER WHERE RESTAURANT_ORDER.order_number = OUTSIDE_ORDER.order_number)").fetchone()[0],\
             "and from inside orders",cursor.execute(f"SELECT SUM(cost) FROM RESTAURANT_ORDER WHERE date >= '{start_date}' AND date <= '{end_date}'\
             AND EXISTS (SELECT * FROM INSIDE_ORDER WHERE RESTAURANT_ORDER.order_number = INSIDE_ORDER.order_number) ").fetchone()[0],"euros.")

#------------------------------------------------------------------------------------------------------
def mark_restaurant_order_as_finished(order_number):
        try:
            if cursor.execute(f"SELECT state FROM RESTAURANT_ORDER WHERE order_number = {order_number}").fetchone()[0] == 'finished':
                raise Exception("The order is already marked as finished")
            cursor.execute(f"UPDATE RESTAURANT_ORDER SET state = 'finished' WHERE order_number = {order_number}")
        except Exception as e:
            print(e.message)
        except sql.Error as err:
            print("Error occured calling the confirm_restaurant_order_arrival() function")
            print("The order number is wrong!")
        connection.commit()
        
#------------------------------------------------------------------------------------------------------
def most_ordered_dish():
    query = """
    SELECT name
    FROM DISH
    WHERE id IN 
    (SELECT dish_id
    FROM CONSISTS 
    GROUP BY dish_id 
    ORDER BY COUNT(*) DESC
    LIMIT 1
    )
    """
    print("Most ordered dish is:",cursor.execute(query).fetchone()[0])
    connection.commit()
    
#------------------------------------------------------------------------------------------------------
def best_customer():
    query =cursor.execute("SELECT customer_id FROM OUTSIDE_ORDER \
                        GROUP BY customer_id ORDER BY COUNT(*) DESC LIMIT 1").fetchone()[0]
    
    query2 = cursor.execute("SELECT name FROM CUSTOMER WHERE id =(?)",(query,))
    
    print("Best Customer is:",query2.fetchone()[0])
    connection.commit()
    
#------------------------------------------------------------------------------------------------------
def todays_reservations():
    query = """  
    SELECT * 
    FROM RESERVATION
    WHERE date = (date("now","localtime"))
    """
    print(cursor.execute(query).fetchall())
    connection.commit()
