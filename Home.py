# type: ignore

import streamlit as st
import requests
from datetime import date

# Get user input
st.title("Weather Data")
lat = st.number_input("Enter latitude", min_value=-90.0, max_value=90.0)
lon = st.number_input("Enter longitude", min_value=-180.0, max_value=180.0)
date = st.date_input("Enter date", min_value=date(2015, 1, 1))

if st.button("Get Weather Data"):
    # Send GET request to FastAPI application
    response = requests.get(
        f"http://localhost:8000/weather?lat={lat}&lon={lon}&date={date}"
    )

    if response.status_code == 200:
        # If the request was successful, display the weather data
        data = response.json()
        st.write(f'Station: {data["station"]}')
        st.write(f'Date: {data["date"]}')
        st.write(f'HDD: {data["hdd"]}')
        st.write(f'CDD: {data["cdd"]}')
        st.write(f'Mean temperature: {data["mean_temp"]}')
    else:
        # If the request was not successful, display the error message
        st.write("Error: Could not get weather data.")
