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

def findPrice():
    result = ""
    try:
        # ait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        #Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser') 
        #Find all elements with IDs containing 'headlessui-disclosure-button' which is the button needed to expand the panel
        button_candidates = [btn for btn in soup.find_all(id=True) if 'headlessui-disclosure-button' in btn['id']]

        #Now, if there are button candidates, click the first one
        if button_candidates:
            button_id = button_candidates[0]['id']
            #Use Selenium to click this button
            from selenium.common.exceptions import WebDriverException
            import time
            try:
                #Wait for the button to be clickable
                disclosure_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, button_id))
                )
                disclosure_button.click()
                time.sleep(1)  #Let the DOM settle

                #Re-fetch the panel candidates after click, to stop it breaking
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                panel_candidates = [el for el in soup.find_all(id=True) if 'headlessui-disclosure-panel' in el['id']]
                if panel_candidates:
                    panel_id = panel_candidates[0]['id']
                else:
                    panel_id = 'headlessui-disclosure-panel-v-3-0-0-5'  #fallback based on original code

                #Wait for the panel to become visible, retry if frame detaches
                for attempt in range(2):
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.ID, panel_id))
                        )
                        break
                    except WebDriverException as e:
                        print(f'WebDriverException: {e}. Retrying...')
                        time.sleep(1)

                #Get page source and parse it again, then print the text of the target element
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                element = soup.select_one(f'#{panel_id} > button:nth-child(1) > p') #This selector is based on the js code provided from inspect element
                if element:
                    result = element.text
                else:
                    result = 'Target element not found!'
            except WebDriverException as e:
                result = (f'WebDriverException occurred: {e}')
        else:
            result = 'No disclosure button found!'
    finally:
        #Close the webdriver
        driver.quit()
        return result


if __name__ == "__main__":
    result = findPrice()
    print(result)



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
