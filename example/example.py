from requests import get
from urllib.parse import quote

url = "https://api.weather.gc.ca/collections/climate-daily/items?properties=COOLING_DEGREE_DAYS,HEATING_DEGREE_DAYS,MEAN_TEMPERATURE"

# Define the query string parameters
params = {
    "f": "json",
    "STATION_NAME": quote("KEMPTVILLE CS"),
    "LOCAL_DATE": quote("2015-01-01"),
}

# Send a GET request to the API with the query string parameters
response = get(url, params=params)

print(response.url)
# Print the status code and the response text
print("Status code:", response.status_code)
print("Response text:", response.json())


{
    "type": "FeatureCollection",
    "features": [
        {
            "id": "6104027.2015.1.1",
            "type": "Feature",
            "geometry": {"coordinates": [-75.63333333333334, 45], "type": "Point"},
            "properties": {
                "HEATING_DEGREE_DAYS": 23.1,
                "MEAN_TEMPERATURE": -5.1,
                "COOLING_DEGREE_DAYS": 0,
            },
        }
    ],
    "numberMatched": 1,
    "numberReturned": 1,
    "links": [
        {
            "type": "application/geo+json",
            "rel": "self",
            "title": "This document as GeoJSON",
            "href": "https://api.weather.gc.ca/collections/climate-daily/items?f=json&properties=COOLING_DEGREE_DAYS,HEATING_DEGREE_DAYS,MEAN_TEMPERATURE&STATION_NAME=KEMPTVILLE%2520CS&LOCAL_DATE=2015-01-01",
        },
        {
            "rel": "alternate",
            "type": "application/ld+json",
            "title": "This document as RDF (JSON-LD)",
            "href": "https://api.weather.gc.ca/collections/climate-daily/items?f=jsonld&properties=COOLING_DEGREE_DAYS,HEATING_DEGREE_DAYS,MEAN_TEMPERATURE&STATION_NAME=KEMPTVILLE%2520CS&LOCAL_DATE=2015-01-01",
        },
        {
            "type": "text/html",
            "rel": "alternate",
            "title": "This document as HTML",
            "href": "https://api.weather.gc.ca/collections/climate-daily/items?f=html&properties=COOLING_DEGREE_DAYS,HEATING_DEGREE_DAYS,MEAN_TEMPERATURE&STATION_NAME=KEMPTVILLE%2520CS&LOCAL_DATE=2015-01-01",
        },
        {
            "type": "application/json",
            "title": "Daily Climate Observations",
            "rel": "collection",
            "href": "https://api.weather.gc.ca/collections/climate-daily/items",
        },
    ],
    "timeStamp": "2024-03-22T18:13:37.500539Z",
}
