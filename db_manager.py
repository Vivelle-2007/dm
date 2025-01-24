import pymongo
import random
import string

# MongoDB connection
MONGO_DB_URI = "mongodb+srv://vivek931tiwari:<db_password>@users.hdn7g.mongodb.net/?retryWrites=true&w=majority&appName=users"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client['disaster_management_db']
users_collection = db['users']

# Function to generate a unique activation token
def generate_token(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Function to register a user
def register_user(phone, location):
    activation_token = generate_token()
    user_data = {
        "phone": phone,
        "location": location,
        "activation_token": activation_token,
        "is_active": False,
    }
    users_collection.insert_one(user_data)
    print(f"User registered successfully! Activation token: {activation_token}")
    return activation_token

# Function to activate a user
def activate_user(phone, token):
    user = users_collection.find_one({"phone": phone})
    if not user:
        return "User not found!"

    if user['activation_token'] == token:
        users_collection.update_one(
            {"phone": phone},
            {"$set": {"is_active": True}}
        )
        return "User activated successfully! Monitoring started."
    else:
        return "Invalid activation token!"