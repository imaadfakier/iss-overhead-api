import requests
from datetime import datetime
import smtplib
import time

MY_LAT = # type latitude here
MY_LONG = # type longitude here
SMTP_SERVER_ADDRESS = 'type server address here'
TEST_EMAIL = 'type sender email here'
TEST_EMAIL_PASSWORD = 'type password here'
RECEIVER_EMAIL = 'type receiver email here'

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


# Your position is within +5 or -5 degrees of the ISS position.
# def is_valid_position():
def is_iss_overhead():
    # return MY_LONG - 5 <= MY_LONG <= MY_LONG + 5  # other way, and you have to do
                                                    # both!
    return MY_LONG - 5 <= iss_longitude <= MY_LONG and MY_LAT - 5 <= iss_latitude <= MY_LAT + 5


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
current_time_hour = time_now.hour


def is_dark():
    # return current_time_hour >= sunset
    return current_time_hour <= sunrise or current_time_hour >= sunset


while True:
    time.sleep(60)
    # if is_valid_position():
    #     if is_dark():
    #         pass
    # if (not is_valid_position()) or (not is_dark()):
    #     continue
    if (not is_iss_overhead()) or (not is_dark()):
        continue
    # if (is_valid_position()) and (is_dark()):
    #     ...

    with smtplib.SMTP(host=SMTP_SERVER_ADDRESS) as connection:
        connection.starttls()
        connection.login(user=TEST_EMAIL, password=TEST_EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=TEST_EMAIL,
            to_addrs=RECEIVER_EMAIL,
            msg='Subject:ISS Up Above! 👆\n\n'
                'Look up because the ISS is close to your current location! 🌎'
        )
    break
