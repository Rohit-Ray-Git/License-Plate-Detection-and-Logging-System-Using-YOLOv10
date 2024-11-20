import mysql.connector

# Connect to MySQL server
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='licensePlatedb'  # Ensure you specify the database
)

if conn.is_connected():
    print('connected')

# Create a cursor
mycursor = conn.cursor()

# Ensure the database exists before using it
mycursor.execute("CREATE DATABASE IF NOT EXISTS licensePlatedb")
mycursor.execute("USE licensePlatedb")

# Create the table
mycursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS LicensePlates(
        id INT AUTO_INCREMENT PRIMARY KEY,
        start_time TEXT,
        end_time TEXT,
        license_plate TEXT
    )
    '''
)

print("Table created successfully.")

# Close the connection
conn.close()
