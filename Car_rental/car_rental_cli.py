import car_rental_system
import os

# Function to clear the screen
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# Main program loop
def main():
    while True:
        clear_screen()
        print("\nCAR RENTAL MANAGEMENT SYSTEM")
        print("1. Add Customer")
        print("2. Add Car")
        print("3. Rent Car")
        print("4. Return Car")
        print("5. View All Cars")
        print("6. Remove Car")
        print("7. Remove Customer")
        print("8. View All Customers")
        print("9. View Customer Information")
        print("10. View Car Information")
        print("11. View Rental Info")
        print("12. Reset Database")
        print("13. Exit")
        print("*" * 30)  # Asterisks added
        choice = input("Enter your choice: ")

        clear_screen()  # Clear the screen before executing the choice

        if choice == "1":
            clear_screen()
            print("*" * 30)  # Asterisks added
            name = input("Enter complete name: ")
            phone = input("Enter customer phone number: ")
            car_rental_system.add_customer(name, phone)
        elif choice == "2":
            clear_screen()
            print("*" * 30)  # Asterisks added
            brand = input("Enter car brand: ")
            model = input("Enter car model: ")
            car_rental_system.add_car(brand, model)
        elif choice == "3":
            clear_screen()
            print("*" * 30)  # Asterisks added
            car_id = input("Enter car ID: ")
            customer_id = input("Enter customer ID: ")
            car_rental_system.rent_car(car_id, customer_id)
        elif choice == "4":
            clear_screen()
            print("*" * 30)  # Asterisks added
            rental_id = input("Enter rental ID: ")
            car_rental_system.return_car(rental_id)
        elif choice == "5":
            clear_screen()
            print("*" * 30)  # Asterisks added
            car_rental_system.view_all_cars()
        elif choice == "6":
            clear_screen()
            print("*" * 30)  # Asterisks added
            car_id = input("Enter car ID: ")
            car_rental_system.remove_car(car_id)
        elif choice == "7":
            clear_screen()
            print("*" * 30)  # Asterisks added
            customer_id = input("Enter customer ID: ")
            car_rental_system.remove_customer(customer_id)
        elif choice == "8":
            clear_screen()
            print("*" * 30)  # Asterisks added
            car_rental_system.view_all_customers()
        elif choice == "9":
            clear_screen()
            print("*" * 30)  # Asterisks added
            customer_id = input("Enter customer ID: ")
            car_rental_system.view_customer_info(customer_id)
        elif choice == "10":
            clear_screen()
            print("*" * 30)  # Asterisks added
            car_id = input("Enter car ID: ")
            car_rental_system.view_car_info(car_id)
        elif choice == "11":
            clear_screen()
            print("*" * 30)  # Asterisks added
            rental_id = input("Enter rental ID: ")
            car_rental_system.view_rental_info(rental_id)
        elif choice == "12":
            clear_screen()
            print("*" * 30)  # Asterisks added
            car_rental_system.reset_database()
        elif choice == "13":
            break
        else:
            clear_screen()
            print("*" * 30)  # Asterisks added
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")  # Wait for user input to continue

# Run the program
if __name__ == "__main__":
    main()
