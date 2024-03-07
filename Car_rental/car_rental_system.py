from configparser import ConfigParser
import mysql.connector

config = ConfigParser()
config.read("config.ini")

# Connect to the MySQL database
try:
    db = mysql.connector.connect(
        host=config.get('mysql', 'host'),
        database=config.get('mysql', 'database'),
        user=config.get('mysql', 'user'),
        password=config.get('mysql', 'password')
    )

except:
    print("Connection to DB went wrong!")

# Create a cursor to execute SQL commands
cursor = db.cursor()


# close connection
def close_connection():
    if db.is_connected():
        # Close cursor and database connection
        cursor.close()
        db.close()
        print("Database connection closed.")


# Add a new customer
def add_customer(name, phone):
    try:
        cursor.execute("INSERT INTO customer (name, phone) VALUES (%s, %s)", (name, phone))
        db.commit()
        customer_id = cursor.lastrowid  # Retrieve the ID of the inserted customer
        print("\nCustomer added successfully. Customer ID:", customer_id)

        # Retrieve and display the information of the added customer
        cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        print("\nCustomer Information:")
        print("ID:", customer[0])
        print("Name:", customer[1])
        print("Phone:", customer[2])

    except mysql.connector.Error as error:
        print("Failed to add customer:", error)


# Add a new car
def add_car(brand, model):
    try:
        cursor.execute("INSERT INTO cars (brand, model) VALUES (%s, %s)", (brand, model))
        car_id = cursor.lastrowid
        db.commit()
        print("\nCar added successfully.")
        print("Car ID:", car_id)

        # Retrieve and display the information of the newly added car
        cursor.execute("SELECT * FROM cars WHERE car_id = %s", (car_id,))
        car = cursor.fetchone()
        print("\nNew Car Information:")
        print("Car ID:", car[0])
        print("Brand:", car[1])
        print("Model:", car[2])

    except mysql.connector.Error as error:
        print("Failed to add car:", error)


# Rent a car
def rent_car(car_id, customer_id):
    try:
        # Check if the car exists
        cursor.execute("SELECT * FROM cars WHERE car_id = %s", (car_id,))
        car = cursor.fetchone()
        if not car:
            print("\nNo car found with the provided ID.")
            return

        # Check if the car is already rented
        cursor.execute("SELECT * FROM rental WHERE car_id = %s", (car_id,))
        rental = cursor.fetchone()
        if rental:
            print("\nThe car is already rented.")
            return

        # Check if the customer exists
        cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            print("\nNo customer found with the provided ID.")
            return

        # Rent the car
        cursor.execute("INSERT INTO rental (car_id, customer_id) VALUES (%s, %s)", (car_id, customer_id))
        db.commit()
        rental_id = cursor.lastrowid  # Get the ID of the last inserted row
        print("\nCar rented successfully.")

        # Show rented car information
        print("\nRented Car Information:")
        print("Rental ID:", rental_id)
        print("Car ID:", car[0])
        print("Brand:", car[1])
        print("Model:", car[2])

        # Show customer information
        print("\nCustomer Information:")
        print("Customer ID:", customer[0])
        print("Name:", customer[1])
        print("Phone:", customer[2])
    except mysql.connector.Error as error:
        print("Failed to rent car:", error)


# Return a car
def return_car(rental_id):
    try:
        cursor.execute("SELECT * FROM rental WHERE rental_id = %s", (rental_id,))
        result = cursor.fetchone()

        if result is None:
            print("\nNo rental record found with the provided ID.")
        else:
            cursor.execute("DELETE FROM rental WHERE rental_id = %s", (rental_id,))
            db.commit()
            print("\nCar returned successfully.")

            # Show the returned car in view_all_cars
            cursor.execute("SELECT * FROM cars WHERE car_id = %s", (result[1],))
            car = cursor.fetchone()
            if car is not None:
                print(f"Returned Car: {car[0]} - {car[1]} {car[2]}")

    except mysql.connector.Error as error:
        print("Failed to return car:", error)


# View all available cars
def view_all_cars():
    try:
        # Retrieve all cars that are not rented
        cursor.execute("""
            SELECT c.car_id, c.brand, c.model
            FROM cars c
            LEFT JOIN rental r ON c.car_id = r.car_id
            WHERE r.car_id IS NULL
        """)
        cars = cursor.fetchall()

        if not cars:
            print("\nNo available cars.")
            return

        print("\nAvailable Cars:")
        for car in cars:
            print("Car ID:", car[0])
            print("Make:", car[1])
            print("Model:", car[2])
            print("--------------------")
    except mysql.connector.Error as error:
        print("Failed to retrieve available cars:", error)


# Remove a car
def remove_car(car_id):
    try:
        cursor.execute("SELECT COUNT(*) FROM cars")
        count = cursor.fetchone()[0]
        if count == 0:
            print("No cars added yet.")
            return

        cursor.execute("SELECT * FROM cars WHERE car_id = %s", (car_id,))
        car = cursor.fetchone()
        if car is None:
            print("Car ID not found in the database.")
            return

        # Show car information
        print("Car Information:")
        print("ID:", car[0])
        print("Brand:", car[1])
        print("Model:", car[2])
        print("")

        # Ask for confirmation
        confirm = input("Are you sure you want to remove this car? (y/n): ")
        if confirm.lower() == "y":
            cursor.execute("DELETE FROM cars WHERE car_id = %s", (car_id,))
            db.commit()
            print("\nCar removed successfully.")
        else:
            print("\nCar removal canceled.")
    except mysql.connector.Error as error:
        print("Failed to remove car:", error)


# Remove a customer
def remove_customer(customer_id):
    try:
        cursor.execute("SELECT COUNT(*) FROM customer")
        count = cursor.fetchone()[0]
        if count == 0:
            print("\nNo customers found. Add customers first.")
            return

        cursor.execute("SELECT customer_id, name, phone FROM customer WHERE customer_id = %s", (customer_id,))
        result = cursor.fetchone()
        if not result:
            print("\nCustomer with the specified ID does not exist.")
            return

        print("\nCustomer Information:")
        print(f"ID: {result[0]}")
        print(f"Name: {result[1]}")
        print(f"Phone: {result[2]}")

        confirm = input("\nAre you sure you want to delete this customer? (Y/N): ")
        if confirm.lower() == "y":
            cursor.execute("DELETE FROM customer WHERE customer_id = %s", (customer_id,))
            db.commit()
            print("\nCustomer removed successfully.")
        else:
            print("\nDeletion canceled.")
    except mysql.connector.Error as error:
        print("Failed to remove customer:", error)


# View all customers
def view_all_customers():
    try:
        cursor.execute("SELECT COUNT(*) FROM customer")
        count = cursor.fetchone()[0]

        if count == 0:
            print("\nNo customers found.")
        else:
            cursor.execute("SELECT * FROM customer")
            result = cursor.fetchall()
            for row in result:
                print("\nCustomer ID: {}, Name: {}, Phone: {}".format(row[0], row[1], row[2]))
    except mysql.connector.Error as error:
        print("Failed to fetch customers:", error)


# View customer information
def view_customer_info(customer_id):
    try:
        cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
        result = cursor.fetchone()
        if result is None:
            print("\nNo customer found with ID:", customer_id)
        else:
            print("\nCustomer ID: {}, Name: {}, Phone: {}".format(result[0], result[1], result[2]))
    except mysql.connector.Error as error:
        print("Failed to fetch customer information:", error)


# View car information
def view_car_info(car_id):
    try:
        cursor.execute("SELECT * FROM cars WHERE car_id = %s", (car_id,))
        result = cursor.fetchone()
        if result:
            print("\nCar ID: {}, Brand: {}, Model: {}".format(result[0], result[1], result[2]))
        else:
            print("\nCar with ID {} not found.".format(car_id))
    except mysql.connector.Error as error:
        print("Failed to fetch car information:", error)


# View rental information
def view_rental_info(rental_id):
    try:
        cursor.execute(
            "SELECT rental.rental_id, rental.car_id, rental.customer_id, cars.brand, cars.model, customer.name, customer.phone FROM rental JOIN cars ON rental.car_id = cars.car_id JOIN customer ON rental.customer_id = customer.customer_id WHERE rental.rental_id = %s",
            (rental_id,))
        rental = cursor.fetchone()

        if rental is None:
            print("\nNo rental record found with the provided ID.")
        else:
            print("\nRental Information:")
            print(f"Rental ID: {rental[0]}")
            print(f"Car ID: {rental[1]}")
            print(f"Customer ID: {rental[2]}")
            print("\nCar Information:")
            print(f"Brand: {rental[3]}")
            print(f"Model: {rental[4]}")
            print("\nCustomer Information:")
            print(f"Name: {rental[5]}")
            print(f"Phone: {rental[6]}")
    except mysql.connector.Error as error:
        print("Failed to fetch rental information:", error)


# Reset the database (remove all data from tables)
def reset_database():
    try:
        confirm = input("Are you sure you want to reset the database? This action cannot be undone. (yes/no): ")
        if confirm.lower() == "yes":
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE rental")
            cursor.execute("TRUNCATE TABLE cars")
            cursor.execute("TRUNCATE TABLE customer")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            db.commit()
            print("Database reset successful. All data has been removed.")
        else:
            print("Database reset aborted.")
    except mysql.connector.Error as error:
        print("Failed to reset the database:", error)

