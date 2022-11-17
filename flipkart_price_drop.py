# I want to know when Amazon Firestick and Echo dot price drops
# Can also tweak it to see when an item is available in stock
# Automate calling this script and send email to xyz to alert.
# Can log it in a csv file

link_targets_file = "flipkart.csv"

import requests
from bs4 import BeautifulSoup
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

                    # choose a random user agent from the list of user agents. This is to prevent
                    # Flipkart from denying our website requests understanding that a script is 
                    # requesting the webpage
                    user_agent = choice(user_agent_list)
                    
                    # feed the chosen user agent into session headers
                    session.headers['user-agent'] = user_agent

                    # get result of website link
                    res = session.get(link)

                    # convert the result to a BeautifulSoup object. html parser should work. 
                    # Else explore other options. Refer docs.
                    soup_data = BeautifulSoup(res.text, 'html.parser')

                    # get the tag that has the price
                    tag = soup_data.find(class_="_30jeq3 _16Jk6d")

                    # price string may have commas. Eg: "$2,599". Remove that.
                    # first character is the currency symbol. Remove that.
                    price = float(tag.string.replace(",","")[1:])
                    currency = tag.string[0]
                    display_price = tag.string
                    
                    return price, currency, display_price

            except AttributeError :
                # Amazon detected the script and did not deliver the webpage
                sleep(0.1)      # sleep before retrying in while loop        
        else :
            print("Request timed out.")
            exit()


def price_alert(price,target) :
    if price <= target :
        return True
    return False


def main() :

    # if the file with links and target prices does not exist in cwd, exit 
    if not os.path.exists(link_targets_file) :
        print(f"Error. {link_targets_file} does not exist.")
        exit()

    # open the file, load the csv
    with open(link_targets_file) as file :
        csvreader = csv.reader(file)

        # save entries as "title" (in quotes),"link" (in quotes),target (float type) 
        # IMPORTANT : do not put spaces in the beginning and end of the quotes 
        for row in csvreader :
            title = row[0]
            link = row[1]
            target = float(row[2])

            price,currency,display_price = check_price(link)
            buy = price_alert(price,target=target)
            if buy :
                print(f"{title} : {display_price} < {currency}{target} .")
            else :
                print(f"{title} : {display_price} > {currency}{target} .")


if __name__ == "__main__" :
    main()