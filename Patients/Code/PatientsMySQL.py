import os
import mysql.connector

cnx = mysql.connector.connect(user='root', password='eshansql',
                              host='localhost',
                              database='Patients')
cnx.close()

def analyze_file(file_path):
    patients = []
    try:
        # Try to open the file in read mode
        with open(file_path, 'r') as file:
            # Reads all lines into a list
            lines = file.readlines()

            # Calculate the number of lines in the file
            num_lines = len(lines)

            # Calculate the total file size in bytes
            file_size = os.path.getsize(file_path)

            # Count the number of lines that start with "MSH"
            msh_count = sum(1 for line in lines if line.startswith('MSH'))

            # Print the results
            print(f"Number of lines: {num_lines}")
            print(f"Total file size: {file_size} bytes")
            print(f"Number of lines starting with 'MSH': {msh_count}")

            # Initialize patient counter
            patient_counter = 1

            # Iterate through the lines to find and print patient names from PID segments
            for line in lines:
                if line.startswith('PID'):
                    segments = line.split('|')
                    if len(segments) > 5:
                        # Extract last name (field 5) and first name (field 5)
                        patient_info = segments[5].split('^')
                        if len(patient_info) >= 2:
                            last_name = patient_info[0].strip()
                            first_name = patient_info[1].strip()
                            patients.append((patient_counter, first_name, last_name))
                            patient_counter += 1
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
    
    return patients

def connect_to_database():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='eshansql',
            database='patients_db'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def setup_database(connection):
    cursor = connection.cursor()
    # Drop the table if it exists
    cursor.execute("DROP TABLE IF EXISTS Patient_Name")
    # Create the Patient_Name table
    cursor.execute("""
        CREATE TABLE Patient_Name (
            Patient_ID INT PRIMARY KEY,
            Patient_First_Name VARCHAR(255),
            Patient_Last_Name VARCHAR(255)
        )
    """)
    connection.commit()

def insert_patients(connection, patients):
    cursor = connection.cursor()
    # Insert patient records into the Patient_Name table
    insert_query = """
        INSERT INTO Patient_Name (Patient_ID, Patient_First_Name, Patient_Last_Name)
        VALUES (%s, %s, %s)
    """
    cursor.executemany(insert_query, patients)
    connection.commit()

def main():
    # Receive input for the file path from the user
    file_path = input("Enter the full path of the text file: ")

    # Analyze the file and get patient data
    patients = analyze_file(file_path)

    # Connect to the MySQL database
    connection = connect_to_database()
    if connection:
        # Setup the database (drop and create table)
        setup_database(connection)
        # Insert patient data into the table
        insert_patients(connection, patients)
        # Close the connection
        connection.close()
        print("Database operation completed successfully")

if __name__ == "__main__":
    main()


