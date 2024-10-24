from sqlmodel import create_engine, SQLModel, Field
import pandas as pd
from typing import Optional
from datetime import datetime


class WeatherTable(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    date: datetime = Field(nullable=False)
    hdd: Optional[int] = Field(nullable=True, default=None)
    cdd: Optional[int] = Field(nullable=True, default=None)
    mean_temp: Optional[int] = Field(nullable=True, default=None)
    station: str = Field(nullable=False)


def create_station_table():
    # Create a connection to the database
    engine = create_engine("postgresql+psycopg2://admin:123@localhost/postgres")

    # Load the data into a pandas DataFrame
    df = pd.read_csv("data/ca_station_list.csv")

    # Use to_sql function to write the DataFrame to a new table in the database
    df.to_sql("StationTable", engine, if_exists="replace", index=False)


def create_weather_table():
    engine = create_engine("postgresql+psycopg2://admin:123@localhost/postgres")
    SQLModel.metadata.create_all(engine)


create_station_table()
