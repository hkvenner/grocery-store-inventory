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
            \r4. Enter the letter 'B' to make a backup of the entire inventory
            \r5. Enter the letter 'E' to exit the menu
        ''')
        choice = input("What would you like to do? ")
        if choice in ['V', 'N', 'A', 'B', 'E']: 
            return choice
        else: 
            input('''\rYou did not choose a valid option. Please press enter to be prompted again. ''')

def clean_date(date_str):
    try: 
        month = int(date_str.split('/')[0])
        day = int(date_str.split('/')[1])
        year = int(date_str.split('/')[2])
        return_date = datetime.date(year, month, day)

    except ValueError: 
        input('''\n Please enter a valid date and time in the format 6/8/2018. 
                \r Hit enter to try again ''')
        return
    else: 
        return return_date

def clean_price(price_str):
    try: 
        price_float = float(price_str[1:])
        return_price = int(price_float * 100)
    except ValueError: 
        input('''\n Please enter a valid price in the format $8.14 . 
                \r Hit enter to try again ''')
        return
    else: 
        return return_price

def clean_id(id_str, id_choices):
    try: 
        product_id = int(id_str)
    except ValueError: 
        input('''\n Please enter a valid ID that is a number (Ex: 3). 
                \r Hit enter to try again ''')
        return
    else:
        if product_id in id_choices: 
            return product_id
        else: 
            input(f'''\n Please enter a valid ID that is on the list of existing IDs. 
                        \r Hit enter to try again ''')
            return

def add_csv_inventory():
    with open('inventory.csv', "r") as csvfile:
        data = csv.reader(csvfile)
        #skips the first row of the csv file
        next(data)

        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                print(row[1])
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
                brand_id = session.query(Brand).filter(Brand.brand_name == brand_name).first().brand_id
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
            id_choices = []
            for product in session.query(Product):
                id_choices.append(product.product_id)
            id_error = True
            while id_error: 
                id_choice = input(f'''
                \nID Choices: {id_choices}
                \rID of product you'd like to view:  ''')
                id_choice = clean_id(id_choice, id_choices)
                if type(id_choice) == int: 
                    id_error = False
            chosen_product = session.query(Product).filter(Product.product_id == id_choice).first()
            print(f'''
            \n{chosen_product.product_id} | Name: {chosen_product.product_name} | Price: ${chosen_product.product_price/100} 
            \r  | Quantity: {chosen_product.product_quantity} Date Updated: {chosen_product.date_updated} | Brand ID: {chosen_product.brand_id} ''')
            input('\nPress Enter to return to the main menu ')

        elif choice == 'N':
            #add new product to database
            product_name = input('New Product Name: ')
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
            brand_id = session.query(Brand).filter(Brand.brand_name == brand_name).first().brand_id
            new_product = Product(product_name=product_name, product_price=product_price,
                                product_quantity=product_quantity, date_updated=date_updated,
                                brand_id=brand_id)
            session.add(new_product)
            session.commit()
            print('Product added!')
            time.sleep(1.5)
            
        elif choice == 'A':
            #view analysis
            least_expensive = session.query(Product).order_by(Product.product_price).first()
            print(f'''This is the least expensive product: {least_expensive}''')
            most_expensive = session.query(Product).order_by(Product.product_price.desc()).first()
            print(f'''This is the most expensive product: {most_expensive}''')
            highest_count = 0
            for brand in session.query(Brand): 
                count = session.query(Product).filter(Product.brand_id == brand.brand_id).count()
                if count > highest_count: 
                    highest_count = count
                    most_popular = brand
            print(f'''This is the most popular brand: {most_popular.brand_name}. There are {highest_count} products from this brand.''')
            time.sleep(1.5)

        elif choice == 'B':
            #make a backup of the entire database
            with open('backup_inventory.csv', 'a') as csvfile: 
                fieldnames = ['product_id','product_name','product_price','product_quantity','date_updated','brand_id']
                dbwriter = csv.DictWriter(csvfile, fieldnames = fieldnames)

                dbwriter.writeheader()
                for product in session.query(Product):
                    dbwriter.writerow({'product_id': product.product_id,
                                    'product_name': product.product_name,
                                    'product_price': product.product_price,
                                    'product_quantity':product.product_quantity,
                                    'date_updated': product.date_updated,
                                    'brand_id': product.brand_id})

            with open('backup_brands.csv', 'a') as csvfile:
                fieldnames = ['brand_id', 'brand_name']
                dbwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

                dbwriter.writeheader()
                for brand in session.query(Brand):
                    dbwriter.writerow({'brand_id': brand.brand_id,
                                    'brand_name': brand.brand_name})
        else:
            print('Good Bye')
            app_running = False
        



if __name__ == '__main__':
    Base.metadata.create_all(engine)

    add_csv_brands()
    add_csv_inventory()
    app()

    #for product in session.query(Product):
        #print(product)

