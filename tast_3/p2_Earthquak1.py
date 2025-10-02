from pymongo import MongoClient

# Create a connection to the MongoDB server
client = MongoClient()

# You can also specify the host and port explicitly
# client = MongoClient('localhost', 27017)
# or use the MongoDB URI format
client = MongoClient('mongodb://localhost:27017/')

# Get a database (it will be created if it doesn't exist)
db = client['EarthData']

# Get a collection within the database
collection = db['EarthQuake']

# Check the connection by listing databases
print(client.list_database_names())
query = {
    'features.properties.magType': 'mww',
    # змінив проміжки features.properties.mag з 8-9 на 6-7, щоб програма вивела колекцію
    "$and": [{"features.properties.mag": {"$gt": 6}}, {"features.properties.mag": {"$lt": 7}}]
}

for dok in collection.find(query):
    print("\n"+str(dok))
