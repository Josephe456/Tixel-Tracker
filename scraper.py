import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service


#import execjs

#Set up WebDriver for Edge
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)

#Load the webpage
driver.get("https://tixel.com/uk/music-tickets/2025/07/24/truck-festival-2025")

try:
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Find all elements with IDs containing 'headlessui-disclosure-button'
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    button_candidates = [btn for btn in soup.find_all(id=True) if 'headlessui-disclosure-button' in btn['id']]
    print('Found disclosure button IDs:', [btn['id'] for btn in button_candidates])

    if button_candidates:
        button_id = button_candidates[0]['id']
        # Now use Selenium to click this button
        from selenium.common.exceptions import WebDriverException
        import time
        try:
            disclosure_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, button_id))
            )
            disclosure_button.click()
            time.sleep(1)  # Let the DOM settle

            # Re-fetch the panel candidates after click
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            panel_candidates = [el for el in soup.find_all(id=True) if 'headlessui-disclosure-panel' in el['id']]
            if panel_candidates:
                panel_id = panel_candidates[0]['id']
            else:
                panel_id = 'headlessui-disclosure-panel-v-3-0-0-5'  # fallback

            # Wait for the panel to become visible, retry if frame detaches
            for attempt in range(2):
                try:
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, panel_id))
                    )
                    break
                except WebDriverException as e:
                    print(f'WebDriverException: {e}. Retrying...')
                    time.sleep(1)
            # Get page source and parse it again
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            element = soup.select_one(f'#{panel_id} > button:nth-child(1) > p')
            if element:
                print(element.text)
            else:
                print('Target element not found!')
        except WebDriverException as e:
            print(f'WebDriverException occurred: {e}')
    else:
        print('No disclosure button found!')
finally:
    #Close the webdriver
    driver.quit()





# #Get the page content as a string
# URL = "https://tixel.com/uk/music-tickets/2025/07/24/truck-festival-2025"
# response = requests.get(URL)
# if response.status_code != 200:
#     raise Exception(f"Failed to load page with status code: {response.status_code}")

# soup = BeautifulSoup(response.text, 'html.parser')






# #Using some JavaScript to find the html element on the page
# js_code = """
# function find(html) {
#     var parser = new DOMParser();
#     var document = parser.parseFromString(html, 'text/html');
#     return document.querySelector("#headlessui-disclosure-panel-v-3-0-0-5 > button:nth-child(1) > p")
#     }
# """

# #Combined HTML and JavaScript execution
# combined_code = f"""
# {js_code}
# findElement('{html_content}')
# """

# result = execjs.eval(combined_code)

# print(result)  # Output the result of the JavaScript function
