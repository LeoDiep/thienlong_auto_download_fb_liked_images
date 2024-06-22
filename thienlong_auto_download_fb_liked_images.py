from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import urllib.request
import random
import string
import re
import time

start_count_time = time.time()

chrome_options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values.notifications': 2}   #block notification popup
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("--headless")        #running on background or on Linux


driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(4)
action = ActionChains(driver)



driver.get('https://www.facebook.com/')
driver.add_cookie({"name": "wd", "value": "your_cookie"})
driver.add_cookie({"name": "presence", "value": "your_cookie"})
driver.add_cookie({"name": "xs", "value": "your_cookie"})
driver.add_cookie({"name": "c_user", "value": "your_cookie"})
driver.add_cookie({"name": "datr", "value": "your_cookie"})
driver.add_cookie({"name": "fr", "value": "your_cookie"})
driver.add_cookie({"name": "sb", "value": "your_cookie"})
driver.add_cookie({"name": "ps_n", "value": "your_cookie"})
driver.add_cookie({"name": "ps_l", "value": "your_cookie"})
sleep(7)
driver.refresh()


#Login by username password (not reccommended because of fb checkpoint)
# driver.get('https://www.facebook.com/login')
# driver.find_element(by=By.XPATH,value=f'//input[contains(@name,"email")]').send_keys('your_email')
# driver.find_element(by=By.XPATH,value=f'//input[contains(@name,"pass")]').send_keys('your_password')
# driver.find_element(by=By.XPATH,value=f'//button[contains(@name,"login")]').click()

sleep(5)
print('Done log in')
# Go to Activity log page, like and reactions section
driver.get('https://www.facebook.com/your_fb_id/allactivity?activity_history=false&category_key=LIKEDPOSTS&manage_mode=false&should_load_landing_page=false')
main_window = driver.current_window_handle

current_date_running = '22 Tháng 6, 2024'      # For setting language vietnamese, update manually for next time running
up_to_date_scroll = '25 Tháng 5, 2024'         # Have at least 1 image liked that day
keep_scroll = True
print('Start scrolling')
unique_date_select = []
while keep_scroll:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Get the furthest date of the scroll
    texts = [el.text for el in driver.find_elements(by=By.XPATH,value=f'//span[contains(@class,"x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1j85h84")]')]
    reg = re.compile(r'\d+ Tháng \d+, \d+')
    date_select = (list(filter(lambda x: reg.search(x), texts)))
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    scroll_origin = ScrollOrigin.from_viewport(10, 10)
    ActionChains(driver).scroll_from_origin(scroll_origin, 0, 1000).perform()
    sleep(1)
    # Print out where is has going to
    for new_date in date_select:
        if new_date not in unique_date_select:
            print(f'Scroll up to {new_date}')
            unique_date_select.append(new_date)
    # Stop scrolling when we get the target date
    if up_to_date_scroll in date_select:
        keep_scroll = False
print('Done scrolling\n')

# Start loading images
num1 = len(driver.find_elements(by=By.XPATH,value=f'//div[contains(@class,"xm6i5cn")]/div'))
print(f'There are {num1-2} days to get')
for i in range(4,num1+1):     #i start from 4, j start from  2
    num2 = len(driver.find_elements(by=By.XPATH, value=f'//div[contains(@class,"xm6i5cn")]/div[{i}]/div'))
    print(f'\nThere are {num2-1} images to get in i={i}')
    for j in range(2,num2+1):
        try:
            single_target = driver.find_element(by=By.XPATH,value=f'//div[contains(@class,"xm6i5cn")]/div[{i}]/div[{j}]//a[contains(@role,"link") and contains(@tabindex,"0")]')
            single_target.send_keys(Keys.CONTROL + Keys.RETURN)
            # switch to the image tab
            windows = driver.window_handles
            driver.switch_to.window(windows[1])
            sleep(2)
            # click to the main or first image if any
            try:
                # sometimes the element don't allow click() so added another way to fix it. Maybe there are other element
                # contain x10l6tqk x13vifvy and isn't clickable so it return error.
                driver.find_element(by=By.XPATH, value=f'//div[@class="x10l6tqk x13vifvy"]/img').click()
                # webdriver.ActionChains(driver).move_to_element(image_click).click(image_click).perform()
                sleep(2)
            except:
                pass
            # by pass if it's not image
            try:
                required_image=driver.find_element(by=By.XPATH, value=f'//img[contains(@data-visualcompletion,"media-vc-image")]').get_attribute('src')
                name = ''.join(random.choice(string.ascii_lowercase) for x in range(20))   #Set random name for images
                urllib.request.urlretrieve(required_image,f'E:\Dowloads\{str(name)}.jpg')
                sleep(1.5)
            except:
                pass
            driver.close()
            driver.switch_to.window(main_window)
            print(f'Done download i={i} j={j}')
            sleep(4)
        except:
            pass
driver.quit()

print('Done download all, job finished\n')
end_count_time = time.time()
total_time_taken = int(end_count_time - start_count_time)
print("Total time taken:", total_time_taken, "seconds")