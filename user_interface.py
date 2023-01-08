"""
Auto einai to main mas programma sto opoio ulopoieitai h "grafikh diepafh"
opws exei anaferthei kai sthn anafora mas.
"""
import sqlite3 as sql
from functions import *
import pandas as pd

while True:
    database = "restaurant.db"
    connection = sql.connect(database)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)


    print("\n\nWelcome to Restautant Database")
    print("If you want to ADD data PRESS 1")
    print("If you want to SEE data PRESS 2")
    print("If you want to UPDATE data PRESS 3")
    print("For EXTRA'S PRESS 4")
    print("If you want to EXIT from the database PRESS ENTER")

    choice = input()

    match choice:
        case "1":
            print("\n\n\n\nTo create CUSTOMER PRESS 1")
            print("To create OUTSIDE ORDER PRESS 2")
            print("To create INSIDE ORDER PRESS 3")
            print("To create RESTAURANT TABLE PRESS 4")
            print("To create RESERVATION PRESS 5")
            print("To create DISH PRESS 6")
            print("To create INGRIDIENT ORDER PRESS 7")
            print("To create SUPPLIER PRESS 8")
            print("To create EMPLOYEE PRESS 9")
            print("To assign TABLE TO EMPLOYEE PRESS 10")
            print("To assign DELIVERY TO EMPLOYEE PRESS 11")


            choice = input()
            match choice:
                case "1":
                    print("\n\nName:")
                    name = input()
                    print("Phone Number:")
                    phone_number = input()
                    print("Email:")
                    email = input()
                    create_customer(name,phone_number,email)

                case "2":
                    dishes = {}
                    dishes_list=[]
                    print("\n   LIST OF AVAILABLE DISHES")
                    print(pd.read_sql_query("SELECT * FROM DISH", connection))
                    print("How many dishes do you want?")
                    quant = int(input())
                    print("Select the dish ID:")
                    dishes_id = int(input())
                    dishes_list.append(dishes_id)
                    count=1
                    while count<quant:
                        print("Select the dish ID:")
                        dishes_id = int(input())
                        dishes_list.append(dishes_id)
                        count = count + 1

                    while dishes_list !=[]:
                        print("How many do you want from the dish(id="+str(dishes_list[0])+")")
                        quantity = int(input())
                        dishes[dishes_list[0]] = quantity
                        dishes_list.pop(0)
                    print("delivery or takeaway?")
                    choice = input()
                    if choice == "delivery":
                        print("Customer ID:")
                        customer_id = input()
                        if customer_id =="":
                            print("Name:")
                            name = input()
                            print("Phone Number:")
                            phone_number  = int(input())
                            print("Email:")
                            email  = input()
                            print("Street:")
                            street = input()
                            print("Floor:")
                            floor = input()
                            print("Number:")
                            number = input()
                            print("Area:")
                            area = input()
                            create_outside_order(dishes,name,phone_number,email,street,floor,number,area)
                        else:
                            print("Name:")
                            name = input()
                            print("Phone Number:")
                            phone_number  = int(input())
                            create_outside_order(dishes,name,phone_number,customer_id=int(customer_id))
                           
                    elif choice == "takeaway":
                        print("Name:")
                        name = input()
                        print("Phone Number:")
                        phone_number  = int(input())
                        print("Customer ID:")
                        customer_id_in = input()
                        if customer_id_in =="":
                            create_outside_order(dishes,name,phone_number,email=None,street=None,floor=None,number=None,area=None,customer_id=None)
                        else:
                            create_outside_order(dishes,name,phone_number,customer_id=int(customer_id_in))
                    else:
                        print("Try Again..")
                

                case "3":
                    dishes = {}
                    dishes_list=[]
                    print("\n   LIST OF AVAILABLE DISHES")
                    print(pd.read_sql_query("SELECT * FROM DISH", connection))
                    print("How many dishes do you want?")
                    quant = int(input())
                    print("Select the dish ID:")
                    dishes_id = int(input())
                    dishes_list.append(dishes_id)
                    count=1
                    while count<quant:
                        print("Select the dish ID:")
                        dishes_id = int(input())
                        dishes_list.append(dishes_id)
                        count = count + 1

                    while dishes_list !=[]:
                        print("How many do you want from the dish(id="+str(dishes_list[0])+")")
                        quantity = int(input())
                        dishes[dishes_list[0]] = quantity
                        dishes_list.pop(0)
                    print(dishes)
                    print("Table:")
                    table_number = int(input())
                    create_inside_order(1,dishes)
                    
                        

                case "4":
                    print("Capacity:")
                    capacity = int(input())
                    create_table(capacity)
                    

                case "5":
                    print("\n\nName:")
                    name = input()
                    print("Date")
                    date = input()
                    print("Time")
                    time = input()
                    print("Phone Number:")
                    phone_number = input()
                    print("People:")
                    people = input()
                    add_reservation(name,date,time,phone_number,people)


                case "6":
                    ingredients={}
                    ingredients_id_list =[]
                    print("How many ingredients this dish needs")
                    howm = int(input())
                    print("\n   LIST OF AVAILABLE INGREDIENTS")
                    print(pd.read_sql_query("SELECT * FROM INGREDIENT", connection))
                    print("Ingredient id:")
                    ingredient_id = int(input())
                    ingredients_id_list.append(ingredient_id)
                    count = 1
                    while count<howm:
                        print("Ingredient id:")
                        ingredient_id = int(input())
                        ingredients_id_list.append(ingredient_id)
                        count = count + 1
                    while ingredients_id_list !=[]:
                        print("How many do you want from the ingredient(id="+str(ingredients_id_list[0])+")")
                        quantity = int(input())
                        ingredients[ingredients_id_list[0]] = quantity
                        ingredients_id_list.pop(0)
                    print(ingredients)
                    print("Dish ID:")
                    dish_id = int(input())
                    print("Name:")
                    name = input()
                    print("Category:")
                    category = input()
                    print("Cost:")
                    cost = input()                
                    create_dish(ingredients,dish_id,name,category,cost)
                    

     
                            

                case "7":
                    ingredients = {}
                    list_ID = []
                    list_char = []
                    print("Supplier Tin:")
                    supplier_tin = int(input())
                    print("How many ingredient do you want to order..?")
                    how_many = int(input())
                    print("Ingridient ID:")
                    id_ = int(input())
                    list_ID.append(id_)
                    count = 1
                    while count<how_many:
                        print("Ingridient ID:")
                        id_ = int(input())
                        list_ID.append(id_)
                        count = count + 1
                    
                    while list_ID != []:
                        print("Name:")
                        name = input()
                        list_char.append(name)
                        print("Category:")
                        category =input()
                        list_char.append(category)
                        print("Quantity:")
                        quantity = int(input())
                        list_char.append(quantity)
                        print("Cost Per Unit:")
                        cpu = float(input())
                        list_char.append(cpu)
                        print("Expiration Date:")
                        expiration_date = input()
                        list_char.append(expiration_date)
                        ingredients[list_ID[0]] = list_char
                        list_ID.pop(0)
                        list_char=[]
                        print(ingredients)
                    order_ingredients(ingredients,supplier_tin)


                              

                case "8":
                    print("\n\nTin:")
                    tin = int(input())
                    print("Name:")
                    name = input()
                    print("Phone Number:")
                    phone_number = int(input())
                    print("Address:")
                    address = input()
                    print("Email:")
                    email = input()
                    if email=="":
                        add_supplier(tin,name,phone_number,address)

                    else:
                        add_supplier(tin,name,phone_number,address,email)

                        

                case "9":
                    print("\n\nTin:")
                    tin = int(input())
                    print("Name:")
                    name = input()
                    print("Role:")
                    role = input()
                    print("Sex:")
                    sex = input()
                    print("Birthday:")
                    birthday = input()
                    print("Email:")
                    email = input()
                    print("Address:")
                    address = input()
                    print("Phone Number:")
                    phone_number = int(input())
                    print("Salary:")
                    salary = float(input())
                    create_employee(tin,name,role,sex,birthday,email,address,phone_number,salary)

                case "10":
                    employee_handle_table()

                case "11":
                    print("Order Number:")
                    order_number = int(input())
                    print("Employee Tin:")
                    employee_tin =int(input())
                    assign_delivery(order_number,employee_tin)

                    
                case _:
                    print("Oops...Run the program AGAIN")
                    
                         
        case "2":
            print("\n\n\nTo see CUSTOMER TABLE PRESS 1")
            print("To see EMPLOYEE TABLE PRESS 2")
            print("To see RESERVATION TABLE PRESS 3")
            print("To see SUPPLIER TABLE PRESS 4")
            print("To see RESTAURANT_TABLE TABLE PRESS 5")
            print("To see DISH TABLE PRESS 6")
            print("To see HANDLES TABLE PRESS 7")
            print("To see ORDER_INGREDIENTS TABLE PRESS 8")
            print("To see INGREDIENT TABLE PRESS 9")
            print("To see ORDER TABLE PRESS 10")
            print("To see MADE_OF TABLE PRESS 11")
            print("To see INGREDIENT_INCLUDED_IN_ORDER TABLE PRESS 12")
            print("To see INSIDE_ORDER TABLE PRESS 13")
            print("To see OUTSIDE_ORDER TABLE PRESS 14")
            print("To see CONSISTS TABLE PRESS 15")
            print("To see DELIVERY TABLE PRESS 16")

            choice = input()
            match choice:
                case "1":
                    print("\n   LIST OF CUSTOMERS")
                    print(pd.read_sql_query("SELECT * FROM CUSTOMER", connection))

                case "2":
                    print("\n   LIST OF EMPLOYEES")
                    print(pd.read_sql_query("SELECT * FROM EMPLOYEE", connection))

                case "3":
                    print("\n   LIST OF RESERVATIONS")
                    print(pd.read_sql_query("SELECT * FROM RESERVATION", connection))

                case "4":
                    print("\n   LIST OF SUPPLIERS")
                    print(pd.read_sql_query("SELECT * FROM SUPPLIER", connection))

                case "5":
                    print("\n   LIST OF RESTAURANT_TABLES")
                    print(pd.read_sql_query("SELECT * FROM RESTAURANT_TABLE", connection))

                case "6":
                    print("\n   LIST OF AVAILABLE DISHES")
                    print(pd.read_sql_query("SELECT * FROM DISH", connection))

                case "7":
                    print("\n   LIST OF HANDLES")
                    print(pd.read_sql_query("SELECT * FROM HANDLES", connection))

                case "8":
                    print("\n   LIST OF ORDERS_INGREDIENTS")
                    print(pd.read_sql_query("SELECT * FROM INGREDIENT_ORDER", connection))

                case "9":
                    print("\n   LIST OF AVAILABLE INGREDIENTS")
                    print(pd.read_sql_query("SELECT * FROM INGREDIENT", connection))
            
                case "10":
                    print("\n   LIST OF ORDERS")
                    print(pd.read_sql_query("SELECT * FROM RESTAURANT_ORDER", connection))
        
                case "11":
                    print("\n   LIST OF MADE OF")
                    print(pd.read_sql_query("SELECT * FROM MADE_OF", connection))
                    
                case "12":
                    print("\n   LIST OF INGREDIENTS_INCLUDED_IN_ORDER")
                    print(pd.read_sql_query("SELECT * FROM INGREDIENT_INCLUDED_IN_ORDER", connection))
                    
                case "13":
                    print("\n   LIST OF INSIDE_ORDER")
                    print(pd.read_sql_query("SELECT * FROM INSIDE_ORDER", connection))

                case "14":
                    print("\n   LIST OF OUTSIDE_ORDER")
                    print(pd.read_sql_query("SELECT * FROM OUTSIDE_ORDER", connection))

                case "15":
                    print("\n   LIST OF CONSISTS")
                    print(pd.read_sql_query("SELECT * FROM CONSISTS GROUP BY order_number ", connection))

                case "16":
                    print("\n   LIST OF DELIVERY")
                    print(pd.read_sql_query("SELECT * FROM DELIVER ", connection))

                case _:
                    print("Oops...Run the program AGAIN")
                    
            
        case "3":
            print("\n\n\n\nTo update CUSTOMER PRESS 1")
            print("To update OUTSIDE ORDER PRESS 2")
            print("To update INSIDE ORDER PRESS 3")
            print("To update RESTAURANT TABLE PRESS 4")
            print("To update RESERVATION PRESS 5")
            print("To update DISH PRESS 6")
            print("To update INGRIDIENT PRESS 7")
            print("To update SUPPLIER PRESS 8")
            print("To update EMPLOYEE PRESS 9")
            print("To update TABLE TO EMPLOYEE PRESS 10")
            print("To update ORDER PRESS 11")

            choice = input()
            match choice:
                case "1":
                    print("Customer's ID who want to change:")
                    id_=int(input())
                    print("\n\nNew Name:")
                    name = input()
                    print("New Phone Number:")
                    phone_number = input()
                    print("New Email:")
                    email = input()
                    cursor.execute("UPDATE CUSTOMER SET name=?,phone_number=?,email=? WHERE id=?",(name,phone_number,email,id_))
                    connection.commit()
                
                case "2":
                    print("Order's Number who want to change:")
                    order_number = int(input())
                    print("New Street:")
                    street =input()
                    print("New Floor:")
                    floor =int(input())
                    print("New Number:")
                    number =int(input())
                    print("New Area:")
                    area =input()
                    order_number = int(input())
                    cursor.execute("UPDATE OUTSIDE_ORDER SET street=?,floor=?,number=?,area=? WHERE order_number=?",(street,floor,number,area,order_number))
                    connection.commit()


                case "3":
                    print("Order's Number who want to change:")
                    order_number = int(input())
                    print("New Table Number:")
                    table_number =int(input())
                    cursor.execute("UPDATE INSIDE_ORDER SET table_number=? WHERE order_number=?",(stable_number,order_number))
                    connection.commit()

                case "4":
                    print("\n\nNew Capacity:")
                    capacity=int(input())
                    cursor.execute("UPDATE RESTAURANT_TABLE SET capacity=? WHERE table_number=?",(capacity,table_number))
                    connection.commit()

                case "5":
                    print("Reservation's Number who want to change:")
                    reservation_number ==int(input())
                    print("\n\nNew Name:")
                    name = input()
                    print("New Phone Number:")
                    phone_number = input()
                    print("New Date")
                    date  = input()
                    print("New Time")
                    time = input()
                    print("New Number of people")
                    people = int(input())
                    cursor.execute("UPDATE RESERVATION SET date=?,phone_number=?,people=?,time=?,name=?\
                                WHERE reservation_number=?",(date,phone_number,people,time,name,reservation_number))
                    connection.commit()

                case "6":
                    print("Dish's ID who want to change:")
                    id_ =int(input())
                    print("\n\nNew Name:")
                    name = input()
                    print("\n\nNew Categoty:")
                    category = input()
                    print("\n\nNew Cost:")
                    cost = float(input())
                    cursor.execute("UPDATE DISH SET name=?,category=?,cost=? WHERE id=?",(name,category,cost,id_))
                    connection.commit()

                case "7":
                    print("Ingredient's ID who want to change:")
                    id_=int(input())
                    print("New Name:")
                    name=input()
                    print("New Category:")
                    category = input()
                    print("New Expiration Date:")
                    expiration_date = input()
                 
                    cursor.execute("UPDATE INGREDIENT SET name=?,category=?,expiration_date=? WHERE id=? ",(name,category,expiration_date,id_))
                    connection.commit()
       

                case "8":
                    print("\n\nSupplier's Tin who want to change:")
                    tin = int(input())
                    print("New Name:")
                    name = input()
                    print("New Phone Number:")
                    phone_number = int(input())
                    print("New Address:")
                    address = input()
                    print("New Email:")
                    email = input()
                    cursor.execute("UPDATE SUPPLIER SET name=?,email=?,\
                                    address=?,phone_number=? WHERE tin=?",(name,email,address,phone_number,tin))
                    connection.commit()

                case "9":
                    print("Employee's Tin who want to change:")
                    tin = int(input())
                    print("New Name:")
                    name = input()
                    print("New Role:")
                    role = input()
                    print("New Sex:")
                    sex = input()
                    print("New Birthday:")
                    birthday = input()
                    print("New Email:")
                    email = input()
                    print("New Address:")
                    address = input()
                    print("New Phone Number:")
                    phone_number = int(input())
                    print("New Salary:")
                    salary = float(input())
                    cursor.execute("UPDATE EMPLOYEE SET name=?,role=?,sex=?,birthday=?,email=?,\
                                    address=?,phone_number=?,salary=? WHERE tin=?",(name,role,sex,birthday,email,address,phone_number,salary,tin))
                    connection.commit()

                case "10":
                    print("Old Employee's Tin:")
                    old_tin = int(input())
                    print("Old Table's Number:")
                    old_tn = int(input())
                    print("Old Starting Time:")
                    old_st = input()
                    print("Old Ending Time:")
                    old_et = input()
                    print("Old Date:")
                    old_date = input()
                    print("New Employee's Tin:")
                    new_tin = int(input())
                    print("New Table's Number:")
                    new_tn = int(input())
                    print("New Starting Time:")
                    new_st = input()
                    print("New Ending Time:")
                    new_et = input()
                    print("New Date:")
                    new_date = input()
                    
                    cursor.execute("UPDATE HANDLES SET start_time=?,end_time=?,date=?,employee_tin=?,table_number=?\
                                WHERE start_time=? AND end_time=? AND date=? AND employee_tin=? AND table_number=?",(new_st,new_et,new_date,new_tin,new_tn,old_st,old_et,old_date,old_tin,old_tn))
                    connection.commit()

                case _:
                    print("Oops...Run the program AGAIN")

                    
                    
                    


            
        case "4":
            print("\n\n\nIf an INGREDIENT ORDER HAS ARRIVED PRESS 1")
            print("If an ORDER HAS ARRIVED PRESS 2")
            print("If you want to CLEAR A RESERVED TABLE PRESS 3")
            print("If you want to SUM UP THE INGREDIENT_ORDERS FROM....UNTIL... PRESS 4")
            print("If you want to SUM UP THE RESTAURANT_ORDERS FROM....UNTIL... PRESS 5")
            print("If you want to SEE THE UNFINISHED ORDERS PRESS 6")
            print("If you want to SEE THE MOST POPULAR DISH PRESS 7")
            print("If you want to SEE THE BEST CUSTOMER PRESS 8")
            print("If you want to SEE TODAY'S ORDERS ONLY PRESS 9")
            choice = input()
            match choice:
                case "1":
                    ids = cursor.execute("SELECT id FROM INGREDIENT_ORDER WHERE state!='finished'").fetchall()
                    print(ids)
                    print("Select the id from order which has arrived:")
                    order_id = int(input())
                    confirm_ingredient_order_arrival(order_id)

                case "2":
                    print("Order Number:")
                    order_number = int(input())
                    mark_restaurant_order_as_finished(order_number)

                case "3":
                    clear_reserved_tables()

                case "4":
                    print("Starting date:")
                    start_date = input()
                    print("Ending date:")
                    end_date= input()
                    if end_date =="" :
                        ingredient_orders_summary(start_date,end_date=None)
                    else:
                        ingredient_orders_summary(start_date,end_date)
                        
                case "5":
                    print("Starting date:")
                    start_date = input()
                    print("Ending date:")
                    end_date= input()
                    if end_date =="" :
                        restaurant_orders_summary(start_date,end_date=None)
                    else:
                        restaurant_orders_summary(start_date,end_date)


                case "6":
                    not_finished_restaurant_orders()

                case "7":
                    most_ordered_dish()

                case "8":
                    best_customer() 

                case "9":
                    todays_reservations()
                    
                case _:
                    print("Oops...Run the program AGAIN")
                    

        case _:
            print("GoodBye")



    if choice=="":
        break
    connection.close()



