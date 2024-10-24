import pytest
import psycopg2


@pytest.fixture(scope="function")
def empty_database():
    # Connect to the database
    conn = psycopg2.connect(
        database="postgres",
        user="admin",
        password="123",
        host="127.0.0.1",
        port="5432",
        connect_timeout=10,
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Delete all data from the tables
    cursor.execute("DELETE FROM weathertable")

    # Commit the changes
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    # Yield control back to the test function
    yield

    # Connect to the database again
    conn = psycopg2.connect(
        database="postgres",
        user="admin",
        password="123",
        host="127.0.0.1",
        port="5432",
        connect_timeout=10,
    )

    # Create a cursor object again
    cursor = conn.cursor()

    # Delete all data from the tables again
    cursor.execute("DELETE FROM weathertable")

    # Commit the changes again
    conn.commit()

    # Close the cursor and the connection again
    cursor.close()
    conn.close()
