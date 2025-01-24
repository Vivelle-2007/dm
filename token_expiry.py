import datetime
import random
import string
import pymongo

MONGO_DB_URI = "your_mongo_connection_string"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client['disaster_management_db']
users_collection = db['users']


def generate_token(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def register_user(phone, location):
    activation_token = generate_token()
    
   
    token_expiry = datetime.datetime.now() + datetime.timedelta(hours=24)
    
    user_data = {
        "phone": phone,
        "location": location,
        "activation_token": activation_token,
        "token_expiry": token_expiry,
        "is_active": False,
    }

    try:
        users_collection.insert_one(user_data)
        print(f"User registered successfully! Activation token: {activation_token}")
        return activation_token
    except pymongo.errors.PyMongoError as e:
        print(f"Error occurred while registering user: {e}")
        return None


def activate_user(phone, token):
    user = users_collection.find_one({"phone": phone})
    
    if not user:
        return "User not found!"

    
    if user['activation_token'] == token:
        if datetime.datetime.now() > user['token_expiry']:
            return "Activation token has expired!"
        

        try:
            users_collection.update_one(
                {"phone": phone},
                {"$set": {"is_active": True}}
            )
            return "User activated successfully! Monitoring started."
        except pymongo.errors.PyMongoError as e:
            return f"Error occurred while activating user: {e}"
    else:
        return "Invalid activation token!"
