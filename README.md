# Weather System Exchange (WSX)

- [Weather System Exchange (WSX)](#weather-system-exchange-wsx)
  - [Overview](#overview)
  - [Research](#research)
  - [Steps](#steps)
  - [Running the Application](#running-the-application)
    - [Installation and Running - Local Development (Windows)](#installation-and-running---local-development-windows)
    - [Installation and Running - Local Development (Ubuntu)](#installation-and-running---local-development-ubuntu)
    - [Update Safely the Dependencies Located in Requirements.txt](#update-safely-the-dependencies-located-in-requirementstxt)
  - [Updating the Database Daily](#updating-the-database-daily)

## Overview

WSX is a system designed to gather, store, and manage weather data from various weather stations across Canada.

## Research

1. **List of Weather Stations Across Canada**
   - Access the list [here](https://open.canada.ca/data/en/dataset/9764d6c6-3044-450c-ac5a-383cedbfef17/resource/dfe03c61-36f1-45f1-962f-76095fc62b1f).

2. **Extracting Data from Weather Stations**
   - Detailed information on how to extract data can be found [here](https://api.weather.gc.ca/#:~:text=GeoMet%2DOGC%2DAPI%20provides%20public,application%20programming%20interfaces%20(API)).
   - API documentation: [OpenAPI Documentation](https://api.weather.gc.ca/openapi?f=html#/).

## Steps

1. **Read from CSV File and Write to Database (Station Table)**
   - Import weather station data from the provided CSV file and store it in the database under the `station` table.

2. **Retrieve and Store Weather Data**
   - Determine the start and end dates for data extraction.
   - Use the API to fetch and store weather data in the `weather` table, starting from 2015 (or less for testing purposes).

3. **Update Recent Weather Data**
   - Fetch the current date and overwrite the past 7 days of data in the `weather` table to ensure up-to-date information.

## Running the Application

### Installation and Running - Local Development (Windows)

1. **Clone** the repository for Staples FM Report
   - `git clone "SSH Key"`

2. **Navigate** to the repository folder for Staples FM Report
   - `cd ...`

3. **Create** a virtual python environment
   - `python -m venv venv`

4. **Activate** the virtual python environment
   - `.\venv\Scripts\activate`

5. **Install** the necessary requirements
   - `pip install -r requirements.in`
  
      Conditional Installation of uvloop
   - `python install_requirements.py`


6. **Starting** the Container and Connecting to PostgreSQL
   - To start the container and connect to the PostgreSQL database, navigate to the `containers` folder using the command `cd containers`. Then, start the container by running the command `docker-compose up`.

7. **Running** the FastAPI Server
    - To run the FastAPI server, use the command `uvicorn app:app --reload`.
  
8. **Writing** to the Database
    -To write the initial data to the database, run the script `main.py` using the command `python3 main.py`.

9. **Run** the Streamlit application
   - `streamlit run Home.py`

10. **Open** your **Internet Browser** to the localhost version of the Staples FM Report.
    - `http://localhost:8501/`

11. **Input** the **password** which you defined in the `.streamlit/secrets.toml`

### Installation and Running - Local Development (Ubuntu)

1. **Clone** the repository for Staples FM Report
   - `git clone "SSH Key"`

2. **Navigate** to the repository folder for Staples FM Report
   - `cd ...`

3. **Create** a virtual python environment
   - `python -m venv venv`

4. **Activate** the virtual python environment
   - `.\venv\Scripts\activate`

5. **Install** the necessary requirements
   - `pip install -r requirements.in`
  
     Conditional Installation of uvloop

   - `python install_requirements.py`
   - 
6. **Starting** the Container and Connecting to PostgreSQL
   - To start the container and connect to the PostgreSQL database, navigate to the `containers` folder using the command `cd containers`. Then, start the container by running the command `docker-compose up`.

7. **Running** the FastAPI Server
    - To run the FastAPI server, use the command `uvicorn app:app --reload`.
  
8. **Writing** to the Database
    -To write the initial data to the database, run the script `main.py` using the command `python3 main.py`.

9. **Run** the Streamlit application
   - `streamlit run Home.py`

10. **Open** your **Internet Browser** to the localhost version of the Staples FM Report.

- `http://localhost:8501/`

11. **Input** the **password** which you defined in the `.streamlit/secrets.toml`



### Update Safely the Dependencies Located in Requirements.txt

---

1. **Ensure** you install `pip-tools` in a **terminal window** via the following **terminal command**
   -`pip install pip-tools`

2. **Run** the process `pip-compile` to **update** the **requirements.txt** via the following **terminal command**
   - `pip-compile requirements.in`

3. **Ensure** your **requirements.txt** has been **updated** with the **latest versions**

4. **Commit & Push** the changes to the `main` branch via **Git**

## Updating the Database Daily

After running `main.py` once, you need to update the database daily with the latest 7 days of information. This can be done by running the script `daily_run.py` using the command `python3 daily_run.py`.
