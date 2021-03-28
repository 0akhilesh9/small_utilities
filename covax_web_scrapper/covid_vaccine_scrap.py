import time
import winsound
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup


"""
A program to continuously poll NY covid19 vaccine website for available appointments

-> Uses Phantomjs for opening url

-> Checks for specific table row (table is searched by element ID 
"""



url = "https://am-i-eligible.covid19vaccine.health.ny.gov/"


browser = webdriver.PhantomJS(executable_path = r"D:\workspace\time_pass\others\bed\prep\phantomjs-2.1.1-windows\bin\phantomjs.exe")
# browser.implicitly_wait(10)
# browser = webdriver.PhantomJS()

def make_sound():
    milliseconds = 10000
    duration = 1000 * milliseconds
    sound_freq = 440  # Hz
    winsound.Beep(sound_freq, duration)

def check_availability():
    browser.get(url)
    delay = 3 # seconds
    try:
        # myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'statePods_table')))
        myElem = WebDriverWait(browser, delay).until(EC.text_to_be_present_in_element((By.ID, 'statePods_table'), "Location Name"))
        # print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='statePods_table')

    for i in range(len(table.contents[1])):
        if table.contents[1].contents[i].contents[0].text.strip() == "SUNY Stony Brook":
            if table.contents[1].contents[i].contents[3].text == "Yes":
                return True
            else:
                return False

while check_availability() == False:
    time.sleep(5 * 60)

make_sound()