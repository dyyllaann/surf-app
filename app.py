from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import schedule
import smtplib
import requests

# Declare text carriers
carriers = {
	'att':    '@txt.att.net',
	'tmobile': ' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com',
    'googlefi': '@msg.fi.google.com'
}

class Buoy:
    swellData = []
    windWaveData = []
    formatted = None

# Get latest data from NDBC using requests library
def getLatestDataFromRequests():
    url = 'https://www.ndbc.noaa.gov/data/latest_obs/46267.txt'
    r = requests.get(url)
    data = r.text
    return data

# Create message function
def send(message):
    # Send message to to_number from gmail address
    to_number = f"3603019197{carriers['googlefi']}"

    # Gmail account and password
    auth = ('straitsurf@gmail.com', 'ubxdboegmwesflzg')

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

	# Send text message through SMS gateway of destination number
    server.sendmail(auth[0], to_number, message)

def populateBuoy():
    data = getLatestDataFromRequests()
    Buoy.formatted = data.replace('°', ' deg')
    array = Buoy.formatted.split('\n')

    for i in range(13, 16):
        subArray = array[i].split(' ')
        Buoy.swellData.append(subArray)

    for i in range(16, 19):
        subArray = array[i].split(' ')
        Buoy.windWaveData.append(subArray)

def checkSwell():
    populateBuoy()
    if float(Buoy.swellData[0][1]) > 0.5:
        send("SURF ALERT\n" + Buoy.formatted)
        print("Surf alert sent")

checkSwell()

schedule.every(30).minutes.do(checkSwell)

while True:
    schedule.run_pending()
    time.sleep(1)
