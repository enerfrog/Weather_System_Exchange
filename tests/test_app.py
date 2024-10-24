from fastapi.testclient import TestClient
from app import app, find_closest_station
from sqlmodel import Session, create_engine
from tables import WeatherTable


engine = create_engine("postgresql+psycopg2://admin:123@localhost/postgres")
client = TestClient(app)


def test_get_weather():
    # Arrange
    lat = 45.41386325690346
    lon = -75.68816832439495
    date = "2022-01-01"
    station_name = find_closest_station(lat, lon)

    # Insert a test record into the test database
    with Session(engine) as session:
        session.add(
            WeatherTable(station=station_name, date=date, hdd=10, cdd=5, mean_temp=15)
        )
        session.commit()

    # Act
    response = client.get(f"/weather?lat={lat}&lon={lon}&date={date}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "station": station_name,
        "date": "2022-01-01T00:00:00",
        "hdd": 10,
        "cdd": 5,
        "mean_temp": 15,
    }


def test_no_data_found():
    response = client.get(
        "/weather",
        params={
            "lat": 0,
            "lon": 0,
            "date": "2015-03-24",
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "No data found for the given date and location."
    }
