from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import schedule
import smtplib

# Declare text carriers
carriers = {
	'att':    '@txt.att.net',
	'tmobile': ' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com',
    'googlefi': '@msg.fi.google.com'
}

# Create Buoy object
class Buoy:
    id = 46088
    checkTime = time.localtime(time.time())

    # Wave attributes
    WVHT = None
    APD = None
    MWD = None
    GST = None

    def tos():
        return (str(Buoy.WVHT) + "\n" +
        str(Buoy.APD) + "\n" +
        str(Buoy.MWD)
        )

# Create message function
def send(message):
    # Send message to to_number from gmail address
    to_number = '3603019197{}'.format(carriers['googlefi'])

    # Gmail account and password
    auth = ('straitsurf@gmail.com', 'LibTech1')

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

	# Send text message through SMS gateway of destination number
    server.sendmail(auth[0], to_number, message)

# Text formatting for terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# fetch data
url = "https://www.ndbc.noaa.gov/station_page.php?station=46088"
page = urlopen(url)

# declare soup
soup = BeautifulSoup(page, 'html.parser')

# locate "data" id
data = soup.find("div", {"id": "data"})

# find first table in data
table = data.find("table")
rows = table.findAll("tr")

# iterate through relevent children and print results
print("")
rowIndex = 1
while rowIndex < len(rows):
    item = rows[rowIndex].findAll("td")
    keywords = ['WVHT', 'APD', 'MWD']
    
    # If length is greater than 2, it contains a key-value pair
    if len(item) > 2:
        key = item[1].string
        value = item[2].string

        print(key, value)

        # # Almost works...
        # while i < len(keywords):
        #     if keywords[i] in key:
        #         setattr(Buoy, keywords[i], (key + value))
        #         print(bcolors.OKGREEN + key, value + bcolors.ENDC)
        #     else:
        #         print(key, value)
    rowIndex += 1

# def action():
#      alert = "SURF ALERT\nBuoy 46088 (Port Angeles)\n" + Buoy.tos()
#      send(alert)
 
# schedule.every(10).minutes.do(action)
 
# while True:
#     schedule.run_pending()