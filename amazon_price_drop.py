# I want to know when Amazon Firestick and Echo dot price drops
# Can also tweak it to see when an item is available in stock
# Automate calling this script and send email to xyz to alert.
# Can log it in a csv file

FIRESTICK_LINK = "https://www.amazon.in/Fire-TV-Stick-Alexa-Voice-Remote-3rd-Gen/dp/B08R6QR863/ref=sr_1_1_sspa?crid=3AP2BSJGP0P8E&keywords=fire+stick&qid=1667356023&qu=eyJxc2MiOiIzLjAxIiwicXNhIjoiMi40NiIsInFzcCI6IjIuMzMifQ%3D%3D&sprefix=firestick%2Caps%2C275&sr=8-1-spons&psc=1"
FIRESTICK_LITE_LINK = "https://www.amazon.in/Fire-TV-Stick-Lite-with-all-new-Alexa-Voice-Remote-Lite/dp/B09BY17DLV/ref=sr_1_2_sspa?crid=3AP2BSJGP0P8E&keywords=fire+stick&qid=1667356023&qu=eyJxc2MiOiIzLjAxIiwicXNhIjoiMi40NiIsInFzcCI6IjIuMzMifQ%3D%3D&sprefix=firestick%2Caps%2C275&sr=8-2-spons&psc=1"
ECHO_DOT_LINK = "https://www.amazon.in/Echo-Dot-4th-Gen-Blue/dp/B084KSRFXJ/ref=sr_1_3?crid=2Y6RFEKPFIRVM&keywords=echo+dot&qid=1667356120&qu=eyJxc2MiOiI0LjMyIiwicXNhIjoiNC4wNCIsInFzcCI6IjMuNzYifQ%3D%3D&sprefix=echo+do%2Caps%2C213&sr=8-3"
HDMI_LINK = "https://www.amazon.in/LAPSTER-Switch-Splitter-Bi-Directional-Supports/dp/B08W579B4F/?_encoding=UTF8&pd_rd_w=YwDrI&content-id=amzn1.sym.1f592895-6b7a-4b03-9d72-1a40ea8fbeca&pf_rd_p=1f592895-6b7a-4b03-9d72-1a40ea8fbeca&pf_rd_r=WVBVM5FYWQ0KP55T7RJ6&pd_rd_wg=wcYPP&pd_rd_r=fcf3daf2-8a78-4747-a2da-329e08d38fea&ref_=pd_gw_ci_mcx_mr_hp_atf_m"
HDMI_CABLE_LINK = "https://www.amazon.in/AmazonBasics-High-Speed-HDMI-Cable-Feet/dp/B014I8SIJY/ref=sr_1_4?crid=1TCQ42WFB4ZJE&keywords=hdmi+cable&qid=1667622294&qu=eyJxc2MiOiI1LjExIiwicXNhIjoiNC41NiIsInFzcCI6IjQuMzQifQ%3D%3D&s=computers&sprefix=hdmi+cabl%2Ccomputers%2C239&sr=1-4"

import requests
from bs4 import BeautifulSoup
import json
from time import sleep
from random import choice
import time
# import sys


user_agent_list = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36' ,
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' ,
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Avant Browser; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727)' ,

]


def check_price(link) :

    timeout = time.time() + 60
    
    while (time.time() < timeout) :
        try :
        
            with requests.session() as session :

                usr_agent = choice(user_agent_list)
                # print(usr_agent)
                session.headers['user-agent'] = usr_agent
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

        except AttributeError :
            # print("Connection unsuccessful. Retrying")
            sleep(0.1)


def price_alert(price,target) :
    if price <= target :
        return True
    return False


def main() :

    price,currency,display_price = check_price(ECHO_DOT_LINK)
    buy = price_alert(price,target=20)
    if buy :
        print(f"Price is {display_price}. Buy now.")
    else :
        print(f"Price is {display_price}. Look for a better deal.")


if __name__ == "__main__" :
    main()