import pyodbc
import os

# Class to handle analyzing patient files
class PatientFileAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.patients = []

    def analyze_file(self):
        """
        Analyze the text file to extract patient information.
        """
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                # Get total number of lines and file size
                num_lines = len(lines)
                file_size = os.path.getsize(self.file_path)
                msh_count = sum(1 for line in lines if line.startswith('MSH'))

                # Print some stats about the file
                print(f"Number of lines: {num_lines}")
                print(f"Total file size: {file_size} bytes")
                print(f"Number of lines starting with 'MSH': {msh_count}")

                # Variable to keep track of patient count
                patient_counter = 1
                for line in lines:
                    if line.startswith('PID'):
                        segments = line.split('|')
                        if len(segments) > 5:
                            # Extract patient details from the line
                            patient_id = segments[3].split('^')[0].strip()
                            patient_info = segments[5].split('^')
                            if len(patient_info) >= 2:
                                last_name = patient_info[0].strip()
                                first_name = patient_info[1].strip()
                                gender = segments[8].strip()
                                # Save patient info to the list
                                self.patients.append((patient_id, first_name, last_name, gender))
                                print(f"PATIENT {patient_counter}: ID: {patient_id}, First Name: {first_name}, Last Name: {last_name}, Gender: {gender}") 
                                patient_counter += 1
        except FileNotFoundError:
            print(f"Error: The file at {self.file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Class to manage database operations
class DatabaseManager:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.connection = None

    def connect(self):
        """
        Connect to the SQL Server database using Windows Authentication.
        """
        try:
            self.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                'Trusted_Connection=yes;'
                'Encrypt=yes;'
                'TrustServerCertificate=yes;'
            )
            print("Connected to SQL Server database")
        except pyodbc.InterfaceError as ie:
            print("Interface Error: Unable to connect to the database. Please check your connection details.")
            print(ie)
        except pyodbc.DatabaseError as de:
            print("Database Error: Unable to connect to the database. Please check your database settings.")
            print(de)
        except pyodbc.Error as e:
            print("General Error: An error occurred while connecting to the database.")
            print(e)

    def setup_database(self):
        """
        Set up the database by dropping the existing Patient_Info table and creating a new one.
        """
        cursor = self.connection.cursor()
        # Drop the table if it exists
        cursor.execute("IF OBJECT_ID('Patient_Info', 'U') IS NOT NULL DROP TABLE Patient_Info;")
        # Create a new Patient_Info table
        cursor.execute("""
            CREATE TABLE Patient_Info (
                Patient_ID VARCHAR(255) PRIMARY KEY,
                First_Name VARCHAR(255),
                Last_Name VARCHAR(255),
                Gender VARCHAR(1)
            )
        """)
        self.connection.commit()

    def insert_patients(self, patients):
        """
        Insert patient records into the Patient_Info table.
        """
        cursor = self.connection.cursor()
        insert_query = """
            INSERT INTO Patient_Info (Patient_ID, First_Name, Last_Name, Gender)
            VALUES (?, ?, ?, ?)
        """
        cursor.executemany(insert_query, patients)
        self.connection.commit()

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()
            print("Database connection closed")

# Class to coordinate file analysis and database operations
class PatientDataProcessor:
    def __init__(self, file_path, server, database):
        self.analyzer = PatientFileAnalyzer(file_path)
        self.db_manager = DatabaseManager(server, database)

    def process(self):
        """
        Process the patient data file and insert the data into the database.
        """
        self.analyzer.analyze_file()
        self.db_manager.connect()
        if self.db_manager.connection:
            self.db_manager.setup_database()
            self.db_manager.insert_patients(self.analyzer.patients)
            self.db_manager.close_connection()
            print("Database operation completed successfully")

def main():
    file_path = input("Enter the full path of the text file: ")
    server = 'ESHAN'  # replace with your SQL Server name
    database = 'Clinic'  # replace with your database name
    processor = PatientDataProcessor(file_path, server, database)
    processor.process()

if __name__ == "__main__":
    main()
