import requests
from beautifulsoup4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.edge import EdgeChromiumDriverManager

import execjs

#Set up WebDriver for Edge
driver = webdriver.Edge(executable_path='C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')

#Load the webpage
driver.get("https://tixel.com/uk/music-tickets/2025/07/24/truck-festival-2025")

try:
    #Wait for the element to be present
    collapsible_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,'headlessui-disclosure-panel-v-3-0-0-5'))
    )
    collapsible_box.click()  # Click the collapsible box to expand it
    
    target_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#headlessui-disclosure-panel-v-3-0-0-5 > button:nth-child(1) > p'))
    )
    
    #Get page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #Find the target element within the expanded box and print it
    element = soup.select_one('#headlessui-disclosure-panel-v-3-0-0-5 > button:nth-child(1) > p')
    print(element.text)  # Print the text content of the element
finally:
    #Close the webdriver
    driver.quit()




'''
#Get the page content as a string
URL = "https://tixel.com/uk/music-tickets/2025/07/24/truck-festival-2025"
response = requests.get(URL)
if response.status_code != 200:
    raise Exception(f"Failed to load page with status code: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')






#Using some JavaScript to find the html element on the page
js_code = """
function find(html) {
    var parser = new DOMParser();
    var document = parser.parseFromString(html, 'text/html');
    return document.querySelector("#headlessui-disclosure-panel-v-3-0-0-5 > button:nth-child(1) > p")
    }
"""

#Combined HTML and JavaScript execution
combined_code = f"""
{js_code}
findElement('{html_content}')
"""

result = execjs.eval(combined_code)

print(result)  # Output the result of the JavaScript function
'''