import smtplib

# Declare text carriers
carriers = {
	'att':    '@txt.att.net',
	'tmobile': ' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com',
    'googlefi': '@msg.fi.google.com'
}

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