import time
import requests
import smtplib
from bs4 import BeautifulSoup
from datetime import datetime


def getStockInfo(url):
    soup = BeautifulSoup(url.content, 'html.parser')
    if '"availability": "http://schema.org/OutOfStock"' in str(soup):
        inStock = False
    else:
        inStock = True

    return inStock


def getURL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        "Upgrade-Insecure-Requests": "1", "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    req_url = requests.get(url=url, headers=headers)
    req_url.raise_for_status()

    return req_url


def stock_check_listener(req_url, address, password, timer, run_hours, run_interval_min):
    listen = True
    start = datetime.now()
    while(listen):
        if getStockInfo(req_url):
            now = datetime.now()
            message = str(now) + ": NOW IN STOCK!"
            print(message)
            send_email(address, password)
            listen = False
            break
        else:
            now = datetime.now()
            print(str(now) + ": Not in Stock, yet...")

        duration = (now - start)
        seconds = duration.total_seconds()
        hours = int(seconds/3600)
        if timer:
            if hours >= run_hours:
                print("Finished")
                listen = False

        time.sleep(run_interval_min * 60)

    return


def send_email(address, password):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(address, password)
    message = """Subject: Phuongs Handtasche ist online!
    \n\nDie Handtasche gibt es hier:\nhttps://de.louisvuitton.com/deu-de/produkte/multi-pochette-accessoires-monogram-nvprod1770359v#M44813
    """
    server.sendmail(address, "v1et4nh@googlemail.com", message)
    return
