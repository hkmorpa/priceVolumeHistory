import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('priceVolume.db')
cursor = conn.cursor()

Stocks = ["SBI", "HDFCBANK", "ICICIBANK"]

#Create all the tables to be monitored
for stock in Stocks:
    query = f"CREATE TABLE if not exists {stock} (date DATE, stock TEXT, price INTEGER, volume INTEGER)"
    cursor.execute(query)
    conn.commit()

query = f'INSERT INTO {stock} VALUES ("2023-04-14", "SBI", 100, 200)'
cursor.execute(query)
conn.commit()

# Retrieve data
#cursor.execute('SELECT table_name from dba_tables')
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close connection
conn.close()
exit()

rows = cursor.fetchall()
for row in rows:
        print(row)
        conn.close()


# Specify the URL of the website
url = 'https://www.cdslindia.com/Authentication/OTP.aspx?id=P'

# Make a GET request to the URL and get the response
response = requests.get(url)

# Check the response status code to ensure the request was successful
if response.status_code != 200:
    print(f'GET request failed with status code {response.status_code}.')
    exit()

print(response.headers)
exit()

soup = BeautifulSoup(response.content, 'html.parser')
# Find all the text elements
form = soup.find('form')

pan_input = soup.find('input', {'id': 'txtpan'})
pan_input['value'] = 'BFQPG0822L' # Replace this with your actual PAN

eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
# Define the data to be submitted with the form
data = {
    '__EVENTVALIDATION': eventvalidation,
    'txtPanNo$txtInput': 'BFQPG0822L',
    'txtPanNo$txtInput2': ''
}

# Submit the form using a POST request
response = requests.post(url, data=data)
if response.status_code != 200:
    print(f'POST request failed with status code {response.status_code}.')
    exit()

print(response.text)
exit()
# Create a new BeautifulSoup object from the response text
soup = BeautifulSoup(response.text, 'html.parser')


print(response.text)

exit()
all_elements = soup.find_all('input', {'type': 'text'})
# Print the text elements
for element in all_elements:
    print(element)

# Extract the form data from the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
view_state = soup.find('input', {'id': '__VIEWSTATE'})['value']
view_state_generator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
event_validation = soup.find('input', {'id': '__EVENTVALIDATION'})['value']

# Set up the POST request data with the PAN number and form data
pan = 'AAVPJ5406E'  # Replace with your PAN number
data = {
    '__VIEWSTATE': view_state,
    '__VIEWSTATEGENERATOR': view_state_generator,
    '__EVENTVALIDATION': event_validation,
    'ctl00$ContentPlaceHolder1$txtPAN': pan,
    'ctl00$ContentPlaceHolder1$btnSubmit': 'Submit'
}

# Make the POST request with the data
response = requests.post(url, data=data)

# Find all the checkboxes and set their values to 'on' (checked)
for checkbox in soup.find_all('input', {'type': 'checkbox'}):
    checkbox['checked'] = 'on'

submit_button = soup.find('input', {'name': 'ctl00$ContentPlaceHolder$btnGenerateOTP'})
form_data = {
    'ctl00$ContentPlaceHolder$txtPAN': pan_input['value'],
    'ctl00$ContentPlaceHolder$btnGenerateOTP': submit_button.get('value'),
    '__EVENTTARGET': submit_button.get('name'),
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': soup.find('input', {'name': '__VIEWSTATE'})['value'],
    '__VIEWSTATEGENERATOR': soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'],
    '__EVENTVALIDATION': soup.find('input', {'name': '__EVENTVALIDATION'})['value'],
    'ctl00$ContentPlaceHolder$cbAgree': 'on',
    'ctl00$ContentPlaceHolder$cbAgree1': 'on',
    'ctl00$ContentPlaceHolder$cbAgree2': 'on'
}

# Send a POST request with the form data to generate OTP
response = requests.post(response.url, data=form_data, cookies=response.cookies)

# Check the response status code to ensure the request was successful
if response.status_code != 200:
    print(f'POST request failed with status code {response.status_code}.')
    exit()

# Do whatever you need to do with the response
print(response.text)

