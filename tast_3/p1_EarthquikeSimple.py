import aiohttp
import asyncio
import json
from datetime import datetime, timedelta

import ssl, certifi

# Assume FeatureCollection and other classes are defined elsewhere
class FeatureCollection:
    # ...
    def __init__(self, metadata, features):
        self.metadata = metadata
        self.features = features

   #classmethod
    def from_json(json_data):
        """
        Creates a FeatureCollection object from a JSON dictionary.
        """
        # Parse metadata
        metadata = json_data.get('metadata', {})

        # Parse each feature and convert it to an Earthquake object
        features = []
        for feature_json in json_data.get('features', []):
            # This is where you would handle different types of features
            feature = Earthquake.from_json(feature_json)
            features.append(feature)
        print(features)
        return features

class GeoPoint:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    @classmethod
    def from_json(cls, json_data):
        # The GeoPoint data is likely in a list of [longitude, latitude]
        coordinates = json_data.get('coordinates', [])
        return cls(longitude=coordinates[0], latitude=coordinates[1])
    
class Earthquake:
    def __init__(self, magnitude, place,X,Y):
        self.magnitude = magnitude
        self.place = place
        self.X=X
        self.Y=Y

    @classmethod
    def from_json(cls, json_data):
        # Earthquake properties are likely in a 'properties' dictionary
        print(json_data)
        
        properties = json_data.get('properties', {})
        geometry=json_data.get('geometry',{})
        coordinates=geometry.get('coordinates', [])
        
        print(coordinates)
        X=coordinates[0]
        Y=coordinates[1]
        print(X,Y)
        return cls(
            magnitude=properties.get('mag'),
            place=properties.get('place'),
            X=coordinates[0],
            Y=coordinates[1]
        )
    
async def read_earthquakes_async(start_time: datetime, end_time: datetime, min_magnitude: float):
    request_uri = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time}&endtime={end_time}&minmagnitude={min_magnitude}"
    print("url:",f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time}&endtime={end_time}&minmagnitude={min_magnitude}")

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            async with session.get(request_uri) as response:
                response.raise_for_status() # This is similar to C#'s EnsureSuccessStatusCode
                
                result = await response.json()
                
                # Assuming the JSON structure is similar
                status = result.get('metadata', {}).get('status', 0)
                print(status)
                if status not in (200, 0):
                    raise Exception(f"Error: Response Status {status}.")
                
                # This part is a guess, as the classes are not defined.
                # You'd need to create a FeatureCollection instance from the JSON data.
                return FeatureCollection.from_json(result)
               # return result

        except aiohttp.ClientError as e:
            print(f"HTTP Request Error: {e}")
        except Exception as e:
            print(f"General Error: {e}")
            
    return None

# Create a timedelta object for a duration of 7 days
async def main():
    # cls=FeatureCollection()
    one_week = timedelta(weeks=1)

    # встановимо інтервал вибірки землетрусів
    now = datetime.now() #кінець
    print(f"Current datetime: {now}")
    # початок
    last_week = now - one_week
    feature_collection = await read_earthquakes_async(last_week,now,6)
    if feature_collection:
        for _feat in feature_collection:
            print(_feat.magnitude,_feat.place,_feat.X,_feat.Y)
    else:
        print("Cannot read feature_collection!")

# Запуск головної асинхронної функції
if __name__ == "__main__":
    asyncio.run(main())
