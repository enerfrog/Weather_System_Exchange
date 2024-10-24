# import unittest
# from unittest.mock import patch
# from daily_run import process_stations_daily
# from datetime import datetime
# import psycopg2

# url = "https://api.weather.gc.ca/collections/climate-daily/items?properties=COOLING_DEGREE_DAYS,HEATING_DEGREE_DAYS,MEAN_TEMPERATURE"


# class TestDaily(unittest.TestCase):
#     @patch("daily_run.get_station_names")
#     @patch("daily_run.pd.date_range")
#     @patch("daily_run.psycopg2.connect")
#     def test_process_stations_daily(
#         self, mock_connect, mock_date_range, mock_get_station_names
#     ):
#         # Mock the return values of the dependencies
#         mock_get_station_names.return_value = ["OTTAWA CDA RCS"]
#         mock_date_range.return_value = [
#             datetime(2024, 3, 20),
#             datetime(2024, 3, 21),
#             datetime(2024, 3, 22),
#             datetime(2024, 3, 23),
#             datetime(2024, 3, 24),
#             datetime(2024, 3, 25),
#             datetime(2024, 3, 26),
#         ]
#         mock_conn = mock_connect.return_value

#         # Set up the input parameters for the function under test
#         station_names = mock_get_station_names.return_value
#         dates = mock_date_range.return_value
#         conn = mock_conn

#         # Call the function under test
#         process_stations_daily(station_names, url, dates, conn)

#         # Assert the expected behavior
#         mock_conn.cursor.assert_called_once()
#         assert mock_conn.commit.call_count <= len(dates)

#     @patch("daily_run.get_station_names")
#     @patch("daily_run.pd.date_range")
#     @patch("daily_run.psycopg2.connect")
#     def test_process_stations_daily_error(
#         self, mock_connect, mock_date_range, mock_get_station_names
#     ):
#         # Mock the return values of the dependencies
#         mock_get_station_names.return_value = ["OTTAWA CDA RCS"]
#         mock_date_range.return_value = [datetime(2024, 3, 24), datetime(2024, 3, 25)]
#         mock_conn = mock_connect.return_value

#         # Set up the input parameters for the function under test
#         station_names = mock_get_station_names.return_value
#         dates = mock_date_range.return_value
#         conn = mock_conn

#         # Mock an error while inserting data
#         mock_conn.cursor.return_value.execute.side_effect = psycopg2.DatabaseError(
#             "Error inserting data"
#         )
#         # Call the function under test
#         process_stations_daily(station_names, url, dates, conn)

#         # Assert the expected behavior
#         mock_conn.cursor.assert_called_once()
#         assert mock_conn.rollback.call_count == len(
#             dates
#         )  # expect rollback to be called once


# if __name__ == "__main__":
#     unittest.main()
