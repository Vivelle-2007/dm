from db_manager import register_user, activate_user
from weather_notifier import start_monitoring 
import re

def validate_phone_number(phone):
    if phone.isdigit() and len(phone) == 10:
        return True
    else:
        print("Invalid phone number. It should be 10 digits.")
        return False

def validate_location(location):
    if location.strip():
        return True
    else:
        print("Location cannot be empty.")
        return False

def main():
    print("Welcome to the Disaster Management System!")
    print("1. Register")
    print("2. Activate System")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        phone = input("Enter your phone number: ")
        if not validate_phone_number(phone):
            return  

        location = input("Enter your location: ")
        if not validate_location(location):
            return  

        token = register_user(phone, location)
        print(f"Registration successful! Your activation token is: {token}")

    elif choice == "2":
        phone = input("Enter your registered phone number: ")
        token = input("Enter your activation token: ")
        result = activate_user(phone, token)
        print(result)

        if "activated successfully" in result:
            print("Starting disaster monitoring...")
            try:
                start_monitoring(phone)
            except Exception as e:
                print(f"Error during monitoring: {e}")

    else:
        print("Invalid choice. Please try again.")

# Ensure this script runs only if executed directly
if __name__ == "__main__":
    main()
