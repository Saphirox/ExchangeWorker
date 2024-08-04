from time import sleep

import requests
import json

with open('client_secrets.json') as client_secrets:
    secrets = json.load(client_secrets)

MEASUREMENT_ID = secrets["MEASUREMENT_ID"]
API_SECRET = secrets["API_SECRET"]


def send_event(rate):
    url = f'https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}'
    client_id = secrets["client_id"]
    payload = {
        "client_id": client_id,
        "events": {
            "name": "exchange_rate",
            "params": {
                "rate": rate,
            }
        }
    }
    requests.post(url, json=payload)


while True:
    nbu_rates = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json").json()
    exchange_rate = list(filter(lambda x: x["cc"] == "USD", nbu_rates))[0]["rate"]
    send_event(exchange_rate)
    sleep(10)