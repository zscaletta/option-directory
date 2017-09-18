import os
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

import pandas as pd

output_dir = r'C:\Users\Zach\Google Drive\resources'

def get_ppilot_faddress():

    url = "http://www.nasdaqtrader.com/MicroNews.aspx?id=OTA2017-52"

    conn = urlopen(url)

    html = conn.read()

    soup = BeautifulSoup(html)
    links = soup.find_all('li')

    for item in links:
        if 'Penny Pilot Issues' in str(item):
            link = item.find('a').attrs['href']
            
    if link:
        return link
    else:
        return 'Unable to find penny pilot link'
            
        
link = get_ppilot_faddress()
urllib.request.urlretrieve(link, 'pennies.xlsx')
df = pd.read_excel('pennies.xlsx', skiprows=6)
df[df.columns[0]].to_csv(os.path.join(output_dir,'pennies.csv'),index=False)
