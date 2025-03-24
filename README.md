# Patients MySQL Database Manager 🏥  

A Python script that analyzes patient data from a text file and stores it in a **MySQL database**.  
It extracts patient information from **HL7-formatted files**, processes it, and saves it into a structured database.  

---

## 🚀 Features  

✅ **Parses HL7 patient records** from a text file  
✅ **Extracts patient names** from PID segments  
✅ **Counts MSH header occurrences**  
✅ **Calculates file statistics** (size, number of lines, etc.)  
✅ **Connects to a MySQL database**  
✅ **Creates a `Patient_Name` table** (if not exists)  
✅ **Inserts extracted patient data** into MySQL  
✅ **Error handling for missing files and database issues**  

---

## 🛠 Installation  

### **1️⃣ Install Python (if not installed)**  
Download and install Python from [python.org](https://www.python.org/downloads/).  

### **2️⃣ Install Required Libraries**  
Run the following command to install dependencies:  

pip install mysql-connector-python

3️⃣ Install & Configure MySQL
Install MySQL from MySQL Community Downloads.

Create a database named patients_db (or modify the script for a different name).

Ensure MySQL is running, and update the connection details in PatientsMySQL.py if necessary.

📌 Usage
1️⃣ Run the script using: python PatientsMySQL.py

2️⃣ Enter the path of the HL7-formatted text file when prompted.

3️⃣ The script will:

Parse the HL7 file

Extract patient first and last names

Store the data in a MySQL table

4️⃣ If successful, you’ll see: Database operation completed successfully

🛠 Troubleshooting
1️⃣ Can't connect to MySQL?

Make sure MySQL is installed and running.

Check that your username, password, and database name are correct.

2️⃣ Script says "file not found"?

Double-check the file path and try again.

3️⃣ No patients are being inserted?

Ensure the input file contains PID segments in HL7 format.

Happy Coding! 🏥💻
