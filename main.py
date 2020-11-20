import re
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def getURL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        "Upgrade-Insecure-Requests": "1", "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    req_url = requests.get(url=url, headers=headers)
    req_url.raise_for_status()
    return req_url


def getStringList(start_str, end_str, txt):
    listString = []
    for i in re.finditer(start_str, txt):
        idx_start = i.start()
        idx_end = txt.index(end_str, idx_start)
        listString.append(txt[idx_start:idx_end])
    return listString


def getHTMLtext(url):
    url = getURL(url)
    soup = BeautifulSoup(url.content, 'html.parser')
    return str(soup)


def addCart(browser, urllist, timeout=5, timesleep=1):
    # Config
    failedList = []

    if browser == 'Firefox':
        driver = webdriver.Firefox()
        xpath_button1 = '/html/body/div[2]/div[3]/div[1]/div[2]/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[4]/div/button'
        xpath_button2 = '/html/body/div[2]/div[3]/div[1]/div[3]/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[4]/div/button'
    elif browser == 'Chrome':
        driver = webdriver.Chrome()
        xpath_button1 = '//*[@id="de"]/div[2]/div[3]/div[1]/div[2]/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[4]/div/button'
        xpath_button2 = '//*[@id="de"]/div[2]/div[3]/div[1]/div[3]/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[4]/div/button'
    else:
        return 0

    for i in range(len(urllist)):
        print(str(i + 1) + '/' + str(len(urllist)))
        driver.get(urllist[i])
        text = getHTMLtext(urllist[i])

        if "<span>Kostenlos</span>" in text or "<span>Free</span>" in text:
            try:
                button = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath_button1)))
                # sleep(timesleep)
                button.click()
                print('Added to cart')
            except TimeoutException:
                try:
                    button = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath_button2)))
                    button.click()
                    print('Added to cart')
                except TimeoutException:
                    print("Adding to cart took too much time")
                    failedList.append(urllist[i])
                    print(urllist[i])
                    continue
            try:
                cart = WebDriverWait(driver, timeout+10).until(EC.presence_of_element_located((By.ID, 'cart-success-title')))
                sleep(timesleep)
            except TimeoutException:
                print('Loading took too much time')
                failedList.append(urllist[i])
                print(urllist[i])
        else:
            print('Not free anymore')


def main(url, browser='Firefox'):
    # Get url-list from mydealz page
    text = getHTMLtext(url)
    udemyURLlist = getStringList('https://www.udemy.com/course/', '"', text)

    # Add courses in cart
    addCart(browser, udemyURLlist)


if __name__ == "__main__":
    page = 'https://www.mydealz.de/deals/ubersicht-uber-40-kostenlose-udemy-kurse-web-development-cisco-firepower-pmi-pmp-atlassian-javascript-python-meditation-seo-etc-1691559'
    main(page)
