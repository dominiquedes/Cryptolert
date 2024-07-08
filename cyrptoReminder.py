import requests
import smtplib, ssl
from datetime import datetime
from email.mime.text import MIMEText
import gspread
from google.oauth2.service_account import Credentials

API_KEY = "Coin Gecko API KEY"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = r'path to credentials'
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_url("yourr spreadsheet url").sheet1

url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin&x_cg_demo_api_key={API_KEY}'
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    coin_data = response.json()
    all_data = coin_data[0]
    print("ID:", all_data['id'])
else:
    print(f"Error fetching data: {response.status_code}")

active_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


port = 587
password = "google password"

text = f'Coin: {all_data['name']}, Price: {all_data['current_price']}, Time Checked: {active_time}'
message = MIMEText(text, "plain")
message["Subject"] = "CRYPTO-UPDATE"
message["From"] = "email"
message["To"] = "recievers email"

with smtplib.SMTP("smtp.gmail.com", port) as server:
    server.starttls()  # Secure the connection
    server.login("email", password)
    server.sendmail("email", "recievers email", message.as_string())

def add_data_to_next_row():
    try:
        row_data = [active_time, all_data['name'], all_data['current_price']]
        sheet.append_row(row_data)
        print("Data added successfully.")
    except Exception as e:
        print(f"Error adding data: {e}")

add_data_to_next_row()
print('Sent')
