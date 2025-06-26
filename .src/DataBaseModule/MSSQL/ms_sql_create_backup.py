import subprocess
import datetime
import os

def create_sql_server_backup():
    # SQL Server details
    SERVER_NAME = "DEV-03\SQLEXPRESS"  # Replace with your server name and instance if needed
    DATABASE_NAME = "site_modbus"  # Replace with the name of your database
    current_directory = os.getcwd()
    print(current_directory)
    BACKUP_DIR = f"{current_directory}\\DataBaseModule\\MSSQL\\backup\\"
    DATE_STR = datetime.date.today().strftime("%Y%m%d")
    BACKUP_FILE = os.path.join(BACKUP_DIR, f"{DATABASE_NAME}_full_backup_{DATE_STR}.bak")

    # Ensure backup directory exists
    os.makedirs(BACKUP_DIR, exist_ok=True)

    # Construct the sqlcmd command for a full backup
    command = [
        "sqlcmd",
        "-S", SERVER_NAME,
        "-E",  # Use Windows Authentication (change to -U and -P for SQL Server Authentication)
        "-Q", f"BACKUP DATABASE {DATABASE_NAME} TO DISK = '{BACKUP_FILE}' WITH INIT"
    ]

    print(f"Starting full backup of {DATABASE_NAME}...")
    try:
        subprocess.run(command, check=True)
        print(f"Full backup completed successfully: {BACKUP_FILE}")
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
    except FileNotFoundError:
        print("Error: The 'sqlcmd' utility was not found. Make sure SQL Server command-line tools are installed and in your system's PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

