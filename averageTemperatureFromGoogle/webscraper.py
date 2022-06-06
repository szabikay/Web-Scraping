import time
import os
from selenium import webdriver
import pandas as pd

df = pd.read_csv('list_of_cities.csv',header=None)
cities = df[0].unique()


URL = 'https://www.google.com/search?q=' + 'average temperature '
driverPath = os.getcwd() + '\\chrome\\chromedriver'
browser = webdriver.Chrome(driverPath) #chromedrive can be downloaded from https://chromedriver.storage.googleapis.com/index.html


inputCity = []
locations = []
countries = []
months = []
highs = []
lows = []

browser.get(URL)

#we got the cookies by opening browser manually and consented all necessary cookies. Cookies were retrieved from running instance by using browser.get_cookies()
#anytime we initialise a new webdriver the following cookies will be automatically added
browser.add_cookie({'domain': 'www.google.com', 'expiry': 1652904381, 'httpOnly': False, 'name': 'DV', 'path': '/', 'secure': False, 'value': 'k4x7cE9EdrogIMGfk5A4RCEai-GLDdjoqshm1sxFHgIAAAA'})
browser.add_cookie({'domain': '.google.com', 'expiry': 1655495781, 'httpOnly': False, 'name': '1P_JAR', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '2022-05-18-19'})
browser.add_cookie({'domain': '.google.com', 'expiry': 1715975780, 'httpOnly': False, 'name': 'CONSENT', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'YES+srp.gws-20220509-0-RC1.en+FX+484'})
browser.add_cookie({'domain': '.google.com', 'expiry': 1668714981, 'httpOnly': True, 'name': 'NID', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '511=n5cNOzD-cMg4ira79KPQCVBxQc3BS7Cyl0kA-v-GGx81UI7F6MiXiWEtW5E80Lr788l-Xs4uUyaDqBVT8n9cdqAKz4at7IUABFuoE21K1r6CjwRIhz-jQJ2VCb0fviuAPjssAj3MPtiTVMlySdfGfklSf2XH-n49SlhiCeMKBx8'})
browser.add_cookie({'domain': '.google.com', 'expiry': 1668455767, 'httpOnly': True, 'name': 'AEC', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'AakniGN5BA2a8e4dsWqxPKa7lZ4CJ4aSpRM3nikPSNnXwFqTFMNFNk5nSA'})

browser.refresh()
browser.find_element_by_link_text('Change to English').click()

for city in cities:
    currentURL = URL + city
    browser.get(currentURL)

    try:
        location = browser.find_element_by_class_name('liveresults-climate__header-location').text
    except:
        inputCity.append(city)
        locations.append('could not be found')
        countries.append('could not be found')
        months.append('could not be found')
        highs.append(99)
        lows.append(99)
        continue

    browser.find_element_by_xpath("//div[@class='kUvfoc yG4QQe']").click() #expand to all months
    time.sleep(2) #expansion may take time let's wait for two seconds
    allSpans = browser.find_elements_by_xpath("//span[@jsname='zXitYb']") #the weather information is available in this span tag

    weatherData = allSpans[1].text

    for line in weatherData.splitlines():
        if line.find('day')>0:
            continue
        elif line.find('/')>0:
            line = line.replace(' ','')
            line = line.replace('°','')
            line = line.split('/')
            highs.append(line[0])
            lows.append(line[1])
        else:
            inputCity.append(city)
            locations.append(location.split(',')[0])
            countries.append(location.split(',')[1].strip())
            months.append(line)

dataToExport = pd.DataFrame(data={'input_city':inputCity,'city':locations,'country':countries,'month':months,'high':highs,'low':lows})
dataToExport.to_csv('averaged_temperature_export.csv',sep='|',index=False)