import requests
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Sheets configuration
SPREADSHEET_ID = '1RRfSP_ZSc_YPUlTgts5B4Ym4KVGJ1yTuPUE064XEx0M'
SHEET_RANGE = 'Sheet1!A:B'  # Column A for timestamp, Column B for IP address

# Authentication with Google Sheets API
creds = Credentials.from_service_account_file('jjm-data-c708ac6c3047.json')
service = build('sheets', 'v4', credentials=creds)

# Function to append data to Google Sheets
def append_to_sheet(data):
    body = {
        'values': [data]
    }
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

# Function to fetch IP address and timestamp
def fetch_ip_and_timestamp():
    try:
        # Fetch IP address from ipify API
        ip_response = requests.get("https://api.ipify.org?format=json")
        ip_data = ip_response.json()
        ip_address = ip_data.get("ip")

        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return timestamp, ip_address

    except Exception as e:
        print(f"An error occurred while fetching IP and timestamp: {e}")
        return None, None

def main():
    timestamp, ip_address = fetch_ip_and_timestamp()
    
    try:
        if timestamp and ip_address:
            print(f"Timestamp: {timestamp}, IP Address: {ip_address}")

            # Prepare data to append to the Google Sheet
            sheet_data = [timestamp, ip_address]
            append_to_sheet(sheet_data)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
