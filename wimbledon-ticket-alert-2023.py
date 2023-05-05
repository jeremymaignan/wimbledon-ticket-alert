import os
import time
from random import randint
from termcolor import colored
import requests

cookies = {}

headers = {}

params = {
    'maxPerformances': '50',
    'maxTimeslots': '50',
    'maxPerformanceDays': '3',
    'maxTimeslotDays': '3',
    'includeMetadata': 'true',
}

# Days you want ticket for
dates_selection = ("2023-07-08", "2023-07-09")

# Courts you want. (comment the ones you don't want)
courts_selection = {
    "Centre Court": 0,
    "No.1 Court": 1,
    "No.2 Court": 2,
    "No.3 Court": 3
}

while True:
    response = requests.get('https://ticketsale.wimbledon.com/tnwr/v1/catalog', params=params, cookies=cookies, headers=headers).json()["sections"]
    for i, court in enumerate(response):

        # Ignore courts not in the courts selection
        if courts_selection and i not in courts_selection.values():
            continue

        days = court["clusters"][0]["items"]
        for day in days:
            product = day["product"]

            # Only keep week end days
            date = product["firstDate"].split('T')[0]
            if dates_selection and date not in dates_selection:
                continue

            # If tickets are available, make noise
            availability = product["jsonLdMetadata"]["offers"]["availability"].split('/')[-1]
            if "InStock" == availability:
                os.system('afplay /System/Library/Sounds/Sosumi.aiff')
                print(product["performances"][0]["name"]['en'], colored(product["jsonLdMetadata"]["offers"]["availability"].split('/')[-1], 'green'))
            else:
                print(product["performances"][0]["name"]['en'], colored(product["jsonLdMetadata"]["offers"]["availability"].split('/')[-1], 'red'))
    print("_")
    time.sleep(randint(10, 30))
