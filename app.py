from models import (Base, session, 
                    Product, Brand, engine)

import datetime
import csv


def menu():
    while True: 
        print('''
            \nINVENTORY
            \r1. Enter the letter 'V' to view the details of a single product in the database
            \r2. Enter the letter 'N' to add a new product to the database
            \r3. Enter the letter 'A' to view an analysis
            \r4. Enter the letter 'B' to make a backup of the entire contents of the database
            \r5. Enter the letter 'E' to exit the menu
        ''')
        choice = input("What would you like to do? ")
        if choice in ['V', 'N', 'A', 'B', 'E']: 
            return choice
        else: 
            input('''\rPlease choose one of the options above and hit enter''')

def clean_date(date_str):
    month = int(date_str.split('/')[0])
    day = int(date_str.split('/')[1])
    year = int(date_str.split('/')[2])
    return datetime.date(year,month,day)

def clean_price(price_str):
    price_float = float(price_str[1:])
    return int(price_float * 100)

def add_csv_inventory():
    with open('inventory.csv', "r") as csvfile:
        data = csv.reader(csvfile)
        #skips the first row of the csv file
        next(data)

        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = row[2]
                date_updated = clean_date(row[3])
                brand_name = row[4]
                #this needs to be updated eventually
                brand_id = 1
                new_product = Product(product_name=product_name, product_price = product_price, 
                                            product_quantity = product_quantity, date_updated = date_updated, 
                                            brand_id = brand_id)
                session.add(new_product)
        session.commit()



def app():
    app_running = True
    while app_running: 
        choice = menu()
        if choice == 'V': 
            #view details of a single product
            pass
        elif choice == 'N':
            #add new product to database
            pass
        elif choice == 'A':
            #view analysis
            pass
        elif choice == 'B':
            #make a backup of the entire database
            pass
        else:
            print('Good Bye')
            app_running = False
        



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #app()
    add_csv_inventory()

    for product in session.query(Product):
        print(product)
