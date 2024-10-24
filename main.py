import time
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from requests import get
from urllib.parse import quote
from datetime import datetime, timedelta
from tables import create_station_table, create_weather_table

create_station_table()

create_weather_table()


def get_station_names() -> list[str]:
    # Create a connection to the database
    engine = create_engine("postgresql+psycopg2://admin:123@localhost/postgres")

    # Execute a SQL query to get all station names from the StationTable
    df = pd.read_sql_table("StationTable", engine, schema="public")

    # Return the station names as a list
    return df["Name"].tolist()


url = "https://api.weather.gc.ca/collections/climate-daily/items?properties=COOLING_DEGREE_DAYS,HEATING_DEGREE_DAYS,MEAN_TEMPERATURE"

station_names = get_station_names()

dates = pd.date_range(
    start="2024-01-01",
    end=(datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
)


conn = psycopg2.connect(
    database="postgres",
    user="admin",
    password="123",
    host="127.0.0.1",
    port="5432",
    connect_timeout=10,
)


def insert_data(cur, data_to_insert):
    try:
        print("Inserting data into WeatherTable...")
        cur.executemany(
            """
            INSERT INTO WeatherTable (date, hdd, cdd, mean_temp, station) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            data_to_insert,
        )
        conn.commit()
        print("Data inserted.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting data: ", error)
        conn.rollback()


BATCH_SIZE = 10000
RETRY_DELAY = 60
MAX_RETRIES = 5


def store_weather_data(
    station_names, url, dates, conn, BATCH_SIZE, RETRY_DELAY, MAX_RETRIES
):
    print(f"Read {len(station_names)} stations.")
    print(f"For {len(dates)} dates from 2024-01-01 until now.")


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
            station = station_name
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    response = get(url, params=params)
                    data = response.json()
                    break  # If the request was successful, break out of the retry loop
                except Exception as e:
                    print(f"Error while making API request: {e}")
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                    retries += 1

            if retries == MAX_RETRIES:
                print("Maximum number of retries exceeded. Skipping this date.")
                continue  # Skip to the next date if the maximum number of retries was exceeded
            if data["features"]:
                first_feature = data["features"][0]
            else:
                print("No features found in the data for the date.")
                continue  # Skip to the next date if no features found

            hdd = first_feature["properties"]["HEATING_DEGREE_DAYS"]
            mean_temp = first_feature["properties"]["MEAN_TEMPERATURE"]
            cdd = first_feature["properties"]["COOLING_DEGREE_DAYS"]

            # If all three variables are None, skip this record
            if hdd is None and cdd is None and mean_temp is None:
                print("All data points are None for this date. Skipping...")
                continue

            else:  # Add the data to the list of data to insert
                data_to_insert.append(
                    (date.strftime("%Y-%m-%d"), hdd, cdd, mean_temp, station)
                )

            # If we've collected enough data for a batch, perform a bulk insert
            if len(data_to_insert) >= BATCH_SIZE:
                insert_data(cur, data_to_insert)
                conn.commit()
                data_to_insert = []

            time.sleep(1)

            # Insert any remaining data that didn't make up a full batch
            if data_to_insert:
                insert_data(cur, data_to_insert)
                conn.commit()

        cur.close()  # Close the cursor after processing all dates for a station

    conn.close()  # Close the connection
    print("Done.")


if __name__ == "__main__":
    create_station_table()
    create_weather_table()
    store_weather_data(
        station_names, url, dates, conn, BATCH_SIZE, RETRY_DELAY, MAX_RETRIES
    )
