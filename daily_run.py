from datetime import datetime, timedelta
import pandas as pd
import psycopg2
from main import get_station_names
from requests import get
from urllib.parse import quote


# Get today's date
today = datetime.today()

# Generate dates for the past seven days up to the day before today
dates = pd.date_range(start=today - timedelta(days=7), end=today - timedelta(days=1))

print("Connecting to the PostgreSQL database...")
conn = psycopg2.connect(
    database="postgres",
    user="admin",
    password="123",
    host="127.0.0.1",
    port="5432",
    connect_timeout=10,
)
print("Connected to the PostgreSQL database.")

station_names = get_station_names()

url = "https://api.weather.gc.ca/collections/climate-daily/items?properties=COOLING_DEGREE_DAYS,HEATING_DEGREE_DAYS,MEAN_TEMPERATURE"


def process_stations_daily(station_names, url, dates, conn):
    data_to_insert = []
    for station_name in station_names:
        print(f"Processing station {station_name}...")
        cur = conn.cursor()

        for date in dates:
            print(f"Processing date {date.strftime('%Y-%m-%d')}...")
            params = {
                "f": "json",
                "STATION_NAME": quote(station_name),
                "LOCAL_DATE": quote(date.strftime("%Y-%m-%d")),
            }
            response = get(url, params=params)
            data = response.json()
            if data["features"]:
                first_feature = data["features"][0]
            else:
                print("No features found in the data for the date.")
                continue  # Skip to the next date if no features found

            hdd = first_feature["properties"]["HEATING_DEGREE_DAYS"]
            mean_temp = first_feature["properties"]["MEAN_TEMPERATURE"]
            cdd = first_feature["properties"]["COOLING_DEGREE_DAYS"]

            if hdd is None and cdd is None and mean_temp is None:
                print("All data points are None for this date. Skipping...")
                continue

            data_to_insert.append(
                (hdd, cdd, mean_temp, date.strftime("%Y-%m-%d"), station_name)
            )

        try:
            cur.executemany(
                """
                UPDATE WeatherTable SET hdd = %s, cdd = %s, mean_temp = %s
                WHERE date = %s AND station = %s
                """,
                data_to_insert,
            )
            conn.commit()
            print("Data updated.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while updating data: ", error)
            conn.rollback()

        cur.close()

    conn.close()
    print("Done.")


if __name__ == "__main__":
    process_stations_daily(station_names=station_names, url=url, dates=dates, conn=conn)
