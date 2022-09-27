from pymongo import MongoClient

# establish connection to MongoDB
MONGO_DB_URL = "mongodb://127.0.0.1:27017"
client = MongoClient(MONGO_DB_URL)

# TODO: old?
# connect to webex_instant_connect db
instant_connect_db = client["webex_instant_connect"]

# clear patient collection
patient_collection = instant_connect_db["patients"]
patient_collection.drop()

# clear provider collection
provider_collection = instant_connect_db["providers"]
provider_collection.drop()

# clear appointment collection
appointment_collection = instant_connect_db["appointments"]
appointment_collection.drop()