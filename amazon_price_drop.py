# I want to know when Amazon Firestick and Echo dot price drops
# Can also tweak it to see when an item is available in stock
# Automate calling this script and send email to xyz to alert.
# Can log it in a csv file

FIRESTICK_LINK = "https://www.amazon.in/Fire-TV-Stick-Alexa-Voice-Remote-3rd-Gen/dp/B08R6QR863/ref=sr_1_1_sspa?crid=3AP2BSJGP0P8E&keywords=fire+stick&qid=1667356023&qu=eyJxc2MiOiIzLjAxIiwicXNhIjoiMi40NiIsInFzcCI6IjIuMzMifQ%3D%3D&sprefix=firestick%2Caps%2C275&sr=8-1-spons&psc=1"
FIRESTICK_LITE_LINK = "https://www.amazon.in/Fire-TV-Stick-Lite-with-all-new-Alexa-Voice-Remote-Lite/dp/B09BY17DLV/ref=sr_1_2_sspa?crid=3AP2BSJGP0P8E&keywords=fire+stick&qid=1667356023&qu=eyJxc2MiOiIzLjAxIiwicXNhIjoiMi40NiIsInFzcCI6IjIuMzMifQ%3D%3D&sprefix=firestick%2Caps%2C275&sr=8-2-spons&psc=1"
ECHO_DOT_LINK = "https://www.amazon.in/Echo-Dot-4th-Gen-Blue/dp/B084KSRFXJ/ref=sr_1_3?crid=2Y6RFEKPFIRVM&keywords=echo+dot&qid=1667356120&qu=eyJxc2MiOiI0LjMyIiwicXNhIjoiNC4wNCIsInFzcCI6IjMuNzYifQ%3D%3D&sprefix=echo+do%2Caps%2C213&sr=8-3"

import requests
import json
from bs4 import BeautifulSoup

# headers = {
#     'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
# }

def check_price(link) :

    with requests.session() as session :
        
        session.headers['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
        res = session.get(link)
        soup_data = BeautifulSoup(res.text, 'html.parser')

        # get the tag that has the price
        tag = soup_data.find(class_="a-section aok-hidden twister-plus-buying-options-price-data")
        
        # convert string to dictionary (json)
        details_dict = json.loads(tag.string[1:-1])      
        
        price = float(details_dict["priceAmount"])
        currency = details_dict["currencySymbol"]
        display_price = details_dict["displayPrice"]

        return price, currency, display_price


def price_alert(price,target) :
    if price <= target :
        return True
    return False


def main() :

    price,currency,display_price = check_price(FIRESTICK_LITE_LINK)
    buy = price_alert(price,target=4000)
    if buy :
        print(f"Price is {display_price}. Buy now.")


if __name__ == "__main__" :
    main()