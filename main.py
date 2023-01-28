import requests
from datetime import datetime
import smtplib
import time
MY_EMAIL = "Masoncu13@ymail.com"
MY_PASSWORD = "Abc123$"
MY_LAT = 30.266666
MY_LNG = -97.733330
FORMAT = 0
ISS_URL = "http://api.open-notify.org/iss-now.json"
SUN_URL = "https://api.sunrise-sunset.org/json"
EMAIL_MSG = "Subject: Look Up\n\nThe ISS is above you."
SMTP_EMAIL = "smtpd.yahoo.com"


# within_view() returns a bool based on if the ISS is within 5 degrees of my location
def within_view() -> bool:
    response = requests.get(url=ISS_URL)
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG-5 <= iss_longitude <= MY_LNG+5:
        return True
    else:
        return False


# is_night() compares the time in Austin to the time the sun is not out, and returns bool
def is_night() -> bool:
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": FORMAT
    }

    response = requests.get(url=SUN_URL, params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False


# iss() checks every hour if the ISS is within view at night. If True, sends an email letting me know.
def iss():
    while True:
        time.sleep(3600)
        if is_night() and within_view():
            connection = smtplib.SMTP(SMTP_EMAIL)
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=EMAIL_MSG)


if __name__ == "__main__":
    iss()
