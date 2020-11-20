import re
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
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


if __name__ == "__main__":
    url_orig = 'https://www.mydealz.de/deals/ubersicht-uber-40-kostenlose-udemy-kurse-web-development-cisco-firepower-pmi-pmp-atlassian-javascript-python-meditation-seo-etc-1691559'
    url = getURL(url_orig)
    soup = BeautifulSoup(url.content, 'html.parser')
    text = str(soup)

    # Get list of udemy courses
    udemyURLlist = getStringList('https://www.udemy.com/course/', '"', text)
    print(udemyURLlist[0])

    # --- New ---
    driver = webdriver.Chrome()
    driver.get(udemyURLlist[0])
    login_link = ''
    while not login_link:
        try:
            print('Login')
            login_link = driver.find_elements_by_link_text('Anmelden')
            login_link.click()
        except:
            continue

    emailID = ''
    while not emailID:
        try:
            emailID = driver.find_element_by_id("email--1")
            emailID.send_keys('v1et4nh@googlemail.com')
            emailID.send_keys(Keys.TAB)
            emailID.send_keys('NamAnh751968')
            emailID.send_keys(Keys.ENTER)
        except:
            continue
    # button = ''
    # while not button:
    #     try:
    #         button = driver.find_elements_by_xpath('//*[@id="de"]/div[2]/div[3]/div[1]/div[2]/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[5]/div/button')
    #         button[0].click()
    #     except:
    #         continue
    # driver.close()
