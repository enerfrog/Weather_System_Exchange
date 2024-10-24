from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select, create_engine
import pandas as pd
from scipy.spatial import cKDTree  # type: ignore
from tables import WeatherTable
import numpy as np

engine = create_engine("postgresql+psycopg2://admin:123@localhost/postgres")


# Load the CSV file into a pandas DataFrame
stations = pd.read_csv("data/ca_station_list.csv")


# Convert latitude and longitude to radians and add to new columns in the DataFrame
stations["latitude_rad"] = np.radians(stations["Latitude"])
stations["longitude_rad"] = np.radians(stations["Longitude"])

# Create a KDTree for fast querying of nearest neighbour
tree = cKDTree(stations[["latitude_rad", "longitude_rad"]].values)


def find_closest_station(lat: float, lon: float) -> str:
    # Convert input latitude and longitude to radians
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    # Find index of closest latitude and longitude in the DataFrame
    dist, idx = tree.query([(lat_rad, lon_rad)], 1)

    # Return the station name of the closest latitude and longitude
    return stations.iloc[idx[0]]["Name"]


print(find_closest_station(45.41386325690346, -75.68816832439495))

app = FastAPI()


@app.get("/weather")
def get_weather(lat: float, lon: float, date: str):
    station_name = find_closest_station(lat, lon)
    with Session(engine) as session:
        statement = select(WeatherTable).where(
            (WeatherTable.station == station_name) & (WeatherTable.date == date)
        )
        results = session.exec(statement).all()

    if not results:
        raise HTTPException(
            status_code=404, detail="No data found for the given date and location."
        )

    # Assuming results is a list of WeatherTable objects
    for result in results:
        return {
            "station": result.station,
            "date": result.date,
            "hdd": result.hdd,
            "cdd": result.cdd,
            "mean_temp": result.mean_temp,
        }
