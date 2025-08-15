import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

IP_GEOLOCATION_PROVIDER = "ip-api"

UNITS = os.getenv("UNITS", "imperial")
HOT_THRESHOLD = float(os.getenv("HOT_THRESHOLD", 85))
COLD_THRESHOLD = float(os.getenv("COLD_THRESHOLD", 50))

ENABLE_EMAIL = True
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_FROM = EMAIL_USERNAME
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587

# --- Scheduling / testing ---
RUN_IMMEDIATE_TEST_CHECK = os.getenv("RUN_IMMEDIATE_TEST_CHECK", "False").lower() in ["true", "1", "yes"]
