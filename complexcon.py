import requests
from time import sleep
from bs4 import BeautifulSoup as bs4
from slackclient import SlackClient
from time import gmtime, strftime
from datetime import datetime
import os
import json



print ("##############################################################")
print ("   Complexcon Monitor DEVELOPED BY @IAMKISHANN ©.             ")
print ("##############################################################")


def complexcon():
    headers = {
            'Host':'cms.complexcon.com',
            'X-App-Authorization':'xxx', #use ur app app auth key
            'Accept':'*/*',
            'User-Agent':'Complex/699 CFNetwork/974.2.1 Darwin/18.0.0',
            'Accept-Language':'en-us',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive'
            }
    s = requests.Session()
    s.headers.update(headers)

    requrl = "http://cms.complexcon.com/api/v1/marketplaces?limit=9223372036854775807&offset=0&include=marketplace_events,featured_products,marketplace_category?reservable=true"
    resp = s.get(requrl)
    sleep(1)
    #soup = bs4(resp.text, 'lxml')
    parsed_json = json.loads(resp.text)
    shops = []

    for i in range (0,len(parsed_json["data"])):
        shops.append(parsed_json["data"][i]["title"])

    return shops

def complexcon_refresh():
    main = True
    while (main == True):
        list1 = complexcon()
        sleep(3)
        list2 = complexcon()


        newshop = list(set(list2).difference(list1))

        if newshop != []:
            post_message = slackmessage("new shop found")
            post_message = slackmessage(newshop)
            print(datetime.now().strftime('%T') + " FOUND NEW PRODUCT on complexcon app. ")
            
        main = True
        print(datetime.now().strftime('%T') + " No new shops live on complexconapp. ")



def slackmessage(link):
    link = link
    sc = SlackClient("xxxx") #API TOKEN HERE 

    sc.api_call(
    "chat.postMessage",
    channel="#monitor", #CHANNEL NAME
    username="nikebot",
    icon_url="https://img.talkandroid.com/uploads/2016/02/SNKRS_App_Icon.png",
    text= link
    )

def main():
    complexcon_refresh()
    print(datetime.now().strftime('%T') + " started complexcon monitor ")


main()


