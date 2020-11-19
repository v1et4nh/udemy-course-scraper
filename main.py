import re
from functions import *


if __name__ == "__main__":
    url_orig = 'https://www.mydealz.de/deals/ubersicht-uber-40-kostenlose-udemy-kurse-web-development-cisco-firepower-pmi-pmp-atlassian-javascript-python-meditation-seo-etc-1691559'
    url = getURL(url_orig)
    soup = BeautifulSoup(url.content, 'html.parser')
    text = str(soup)

    # Get list of udemy courses
    udemyURLlist = []
    for i in re.finditer('https://www.udemy.com/course/', text):
        idx_start = i.start()
        idx_end   = text.index('"', idx_start)
        udemyURLlist.append(text[idx_start:idx_end])
    print(udemyURLlist[0])
