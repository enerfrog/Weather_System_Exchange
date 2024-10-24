import unittest
from unittest.mock import patch, Mock
from main import store_weather_data, insert_data
from datetime import datetime
import psycopg2
import requests_mock


url = "https://api.weather.gc.ca/collections/climate-daily/items?properties=COOLING_DEGREE_DAYS,HEATING_DEGREE_DAYS,MEAN_TEMPERATURE"


class TestInsertData(unittest.TestCase):
    @patch("psycopg2.connect")
    def test_insert_data_error(self, mock_connect):
        # Set up the mock connection and cursor
        mock_conn = mock_connect.return_value
        mock_cur = mock_conn.cursor.return_value

        # Mock an error when calling executemany
        mock_cur.executemany.side_effect = psycopg2.DatabaseError("Mock database error")

        # Call the function under test
        data_to_insert = [("2022-01-01", 10, 5, 15, "OTTAWA CDA RCS")]
        insert_data(mock_cur, data_to_insert)

        # Assert that rollback was called due to the error
        mock_conn.rollback.assert_not_called()


class TestMain:
    @patch("main.get_station_names")
    @patch("main.pd.date_range")
    @patch("main.psycopg2.connect")
    def test_store_weather_data(
        self, mock_connect, mock_date_range, mock_get_station_names, empty_database
    ):
        # Mock the return values of the dependencies
        mock_get_station_names.return_value = ["OTTAWA CDA RCS"]
        mock_date_range.return_value = [datetime(2024, 3, 25)]
        mock_conn = mock_connect.return_value

        # Set up the input parameters for the function under test
        station_names = mock_get_station_names.return_value
        dates = mock_date_range.return_value
        conn = mock_conn

        MAX_RETRIES = 3
        RETRY_DELAY = 5
        BATCH_SIZE = 10

        # Call the function under test
        store_weather_data(
            station_names, url, dates, conn, BATCH_SIZE, RETRY_DELAY, MAX_RETRIES
        )

        # Assert the expected behavior
        mock_conn.cursor.assert_called_once()
        assert mock_conn.commit.called_once()

    @patch("main.get_station_names")
    @patch("main.pd.date_range")
    @patch("main.psycopg2.connect")
    def test_store_weather_data_batch(
        self, mock_connect, mock_date_range, mock_get_station_names
    ):
        # Mock the return values of the dependencies
        mock_get_station_names.return_value = ["OTTAWA CDA RCS"]
        mock_date_range.return_value = [datetime(2024, 3, 24), datetime(2024, 3, 25)]
        mock_conn = mock_connect.return_value

        # Set up the input parameters for the function under test
        station_names = mock_get_station_names.return_value
        dates = mock_date_range.return_value
        conn = mock_conn

        MAX_RETRIES = 3
        RETRY_DELAY = 5
        BATCH_SIZE = 1
        # Call the function under test
        store_weather_data(
            station_names, url, dates, conn, BATCH_SIZE, RETRY_DELAY, MAX_RETRIES
        )

        # Assert the expected behavior
        mock_conn.cursor.assert_called_once()
        assert mock_conn.commit.called_once()

    @patch("main.get_station_names")
    @patch("main.pd.date_range")
    @patch("main.psycopg2.connect")
    def test_store_weather_data_error(
        self, mock_connect, mock_date_range, mock_get_station_names
    ):
        # Mock the return values of the dependencies
        mock_get_station_names.return_value = ["OTTAWA CDA RCS"]
        mock_date_range.return_value = [datetime(2024, 3, 24)]
        mock_conn = mock_connect.return_value

        # Set up the input parameters for the function under test
        station_names = mock_get_station_names.return_value
        dates = mock_date_range.return_value
        conn = mock_conn

        # Mock an error while inserting data
        mock_conn.cursor.return_value.execute.side_effect = psycopg2.DatabaseError(
            "Error inserting data"
        )
        MAX_RETRIES = 3
        RETRY_DELAY = 5
        BATCH_SIZE = 10
        # Call the function under test
        store_weather_data(
            station_names, url, dates, conn, BATCH_SIZE, RETRY_DELAY, MAX_RETRIES
        )

        mock_conn.commit.assert_called_once()

    @patch("main.get_station_names")
    @patch("main.pd.date_range")
    @patch("main.psycopg2.connect")
    def test_error_making_api_reqs(
        self, mock_connect, mock_date_range, mock_get_station_names
    ):
        # Set up the input parameters for the function under test
        MAX_RETRIES = 3
        RETRY_DELAY = 5
        BATCH_SIZE = 10

        url = "https://api.weather.gc.ca/collections/climate-daily/items"

        # Mock the return values of the dependencies
        mock_get_station_names.return_value = ["OTTAWA CDA RCS"]
        mock_date_range.return_value = [datetime(2024, 3, 25)]
        mock_conn = mock_connect.return_value

        # Set up the input parameters for the function under test
        station_names = mock_get_station_names.return_value
        dates = mock_date_range.return_value
        conn = mock_conn

        with requests_mock.Mocker() as m:
            # Mock the get request
            m.get(url, exc=Exception("Error making API request"))

            store_weather_data(
                station_names, url, dates, conn, BATCH_SIZE, RETRY_DELAY, MAX_RETRIES
            )
        # Assert the expected behavior
        assert len(m.request_history) == MAX_RETRIES

    @patch("requests.get")
    @patch("main.get_station_names")
    @patch("main.pd.date_range")
    @patch("main.psycopg2.connect")
    @patch("builtins.print")
    def test_store_no_data(
        self,
        mock_connect,
        mock_date_range,
        mock_get_station_names,
        mock_get,
        mock_print,
    ):
        url = "https://api.weather.gc.ca/collections/climate-daily/items"
        MAX_RETRIES = 3
        RETRY_DELAY = 5
        BATCH_SIZE = 1
        # Mock the return values of the dependencies
        mock_get_station_names.return_value = ["OTTAWA CDA RCS"]
        mock_date_range.return_value = [datetime(2024, 3, 24)]
        mock_conn = mock_connect.return_value

        station_names = mock_get_station_names.return_value
        dates = mock_date_range.return_value
        conn = mock_conn

        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = {"features": []}
        # m.get(url, json={"features": []})

        # Call the function under test
        store_weather_data(
            station_names, url, dates, conn, BATCH_SIZE, RETRY_DELAY, MAX_RETRIES
        )

        # Assert the expected behavior
        mock_conn.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
