from ast import Try
from tkinter.tix import INTEGER
from models import (Base, session, 
                    Product, Brand, engine)

import datetime
import csv
import time


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
    try: 
        month = int(date_str.split('/')[0])
        day = int(date_str.split('/')[1])
        year = int(date_str.split('/')[2])
        return_date = datetime.date(year, month, day)

    except ValueError: 
        input('''\n Please enter a valid date and time in the format 6/8/2018. 
                \r Hit enter to try again ''')
    else: 
        return return_date

def clean_price(price_str):
    try: 
        price_float = float(price_str[1:])
        return_price = int(price_float * 100)
    except ValueError: 
        input('''\n Please enter a valid price in the format $8.14 . 
                \r Hit enter to try again ''')
    else: 
        return return_price

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


def add_csv_brands():
    with open('brands.csv', "r") as csvfile:
        data = csv.reader(csvfile)
        #skips the first row of the csv file
        next(data)

        for row in data:
            brand_in_db = session.query(Brand).filter(Brand.brand_name == row[0]).one_or_none()
            if brand_in_db == None:
                brand_name = row[0]
                new_brand = Brand(brand_name=brand_name)
                session.add(new_brand)
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
            product_name = input('Product Name: ')
            price_error = True
            while price_error:
                product_price = input('Product Price(Ex: $4.60 ): ')
                product_price = clean_price(product_price)
                if type(product_price) == int:
                    price_error = False
            product_quantity = input('Product Quantity(Ex: 44): ')
            date_error = True
            while date_error: 
                date_updated = input('Date Updated(Ex:1/20/2018): ')
                date_updated = clean_date(date_updated)
                if type(date_updated) == datetime.date:
                    date_error = False
            brand_name = input('Brand Name: ')
            #this needs to be updated eventually
            brand_id = 1
            new_product = Product(product_name=product_name, product_price=product_price,
                                product_quantity=product_quantity, date_updated=date_updated,
                                brand_id=brand_id)
            session.add(new_product)
            session.commit()
            print('Book added!')
            time.sleep(1.5)
            
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

    add_csv_brands()
    add_csv_inventory()
    app()

    for product in session.query(Product):
        print(product)

