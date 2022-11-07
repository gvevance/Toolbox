# I want to know when Amazon Firestick and Echo dot price drops
# Can also tweak it to see when an item is available in stock
# Automate calling this script and send email to xyz to alert.
# Can log it in a csv file

link_targets_file = "filename_2.csv"

import requests
from bs4 import BeautifulSoup
import json
from time import sleep
from random import choice
from time import time
import os
import csv
# import sys


user_agent_list = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36' ,
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' ,
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Avant Browser; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727)' ,

]


def check_price(link) :

    timeout = time() + 60       # try for 60 seconds and exit
    
    while (True) :

        if time() < timeout :
            try :
            
                with requests.session() as session :

                    usr_agent = choice(user_agent_list)
                    # print(usr_agent)
                    session.headers['user-agent'] = usr_agent
                    res = session.get(link)
                    soup_data = BeautifulSoup(res.text, 'html.parser')

                    # get the tag that has the price
                    tag = soup_data.find(class_="_30jeq3 _16Jk6d")

                    price = float(tag.string.replace(",","")[1:])
                    currency = tag.string[0]
                    display_price = tag.string
                    
                    # price,currency,display_price = 0,0,0
                    return price, currency, display_price

            except AttributeError :
                # print("Connection unsuccessful. Retrying")
                sleep(0.1)
        
        else :
            print("Request timed out.")
            exit()


def price_alert(price,target) :
    if price <= target :
        return True
    return False


def main() :

    if not os.path.exists(link_targets_file) :
        print(f"Error. {link_targets_file} does not exist.")
        exit()
    
    with open(link_targets_file) as file :
        csvreader = csv.reader(file)
        for row in csvreader :
            title = row[0]
            link = row[1]
            target = float(row[2])

            price,currency,display_price = check_price(link)
            buy = price_alert(price,target=target)
            if buy :
                print(f"Price of {title} is {display_price}. Buy now.")
            else :
                print(f"Price of {title} is {display_price}. Look for a better deal.")


if __name__ == "__main__" :
    main()