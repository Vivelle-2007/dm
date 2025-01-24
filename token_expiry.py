import datetime
import random
import string
import pymongo

# MongoDB connection (replace with your actual connection string)
MONGO_DB_URI = "your_mongo_connection_string"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client['disaster_management_db']
users_collection = db['users']

# Function to generate a unique activation token
def generate_token(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Function to register a user
def register_user(phone, location):
    activation_token = generate_token()
    
    # Set token expiry time to 24 hours from now
    token_expiry = datetime.datetime.now() + datetime.timedelta(hours=24)
    
    user_data = {
        "phone": phone,
        "location": location,
        "activation_token": activation_token,
        "token_expiry": token_expiry,
        "is_active": False,
    }

    try:
        # Insert the user data into the MongoDB collection
        users_collection.insert_one(user_data)
        print(f"User registered successfully! Activation token: {activation_token}")
        return activation_token
    except pymongo.errors.PyMongoError as e:
        print(f"Error occurred while registering user: {e}")
        return None

# Function to activate a user
def activate_user(phone, token):
    user = users_collection.find_one({"phone": phone})
    
    if not user:
        return "User not found!"

    # Check if the token is valid and not expired
    if user['activation_token'] == token:
        if datetime.datetime.now() > user['token_expiry']:
            return "Activation token has expired!"
        
        # Update user to set them as active
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