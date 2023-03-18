import os
import time
from random import randint

import requests

cookies = {}

headers = {
    'authority': 'ticketsale.wimbledon.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'referer': 'https://ticketsale.wimbledon.com/content',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'x-api-key': '',
    'x-csrf-token': '',
    'x-secutix-host': 'ticketsale.wimbledon.com',
}

params = {
    'maxPerformances': '50',
    'maxTimeslots': '50',
    'maxPerformanceDays': '3',
    'maxTimeslotDays': '3',
    'includeMetadata': 'true',
}

week_end = ("2022-07-02T13:30:00.000Z", "2022-07-03T13:30:00.000Z")

while True:
    response = requests.get('https://ticketsale.wimbledon.com/tnwr/v1/catalog', params=params, cookies=cookies, headers=headers)
    days = response.json()["sections"][0]["clusters"][0]["items"]
    for day in days:
        product = day["product"]

        # Only keep week end days
        if product["firstDate"] not in week_end:
            continue

        # If tickets are available, make noise
        if "SoldOut" not in product["jsonLdMetadata"]["offers"]["availability"]:
            os.system('afplay /System/Library/Sounds/Sosumi.aiff')
            print("{}: {}".format(product["performances"][0]["name"]['en'], product["jsonLdMetadata"]["offers"]["availability"].split('/')[-1]))
        else:
            print("{}: {}".format(product["performances"][0]["name"]['en'], product["jsonLdMetadata"]["offers"]["availability"].split('/')[-1]))

    time.sleep(randint(15, 30))
