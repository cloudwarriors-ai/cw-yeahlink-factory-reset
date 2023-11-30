
import time
import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Create a file handler and set the log file to debug.txt
file_handler = logging.FileHandler('debug.txt')
file_handler.setLevel(logging.DEBUG)

# Create a stream handler to log to stdout
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument("--headless")  # Run Chrome in headless mode
browser = webdriver.Chrome(options=options)



def phone_reset(ip, username, password):
    logger.info(f"Resetting phone with IP: {ip}")
    try:
        
        url = f"https://{ip}/servlet?m=mod_listener&p=login&q=loginForm&jumpto=status"
        logger.info(f"URL: {url}")
        browser.get(url)
        logger.info(f"Logging in to {ip}")
        username_input = browser.find_element("id", "idUsername")
        username_input.send_keys(username)
        password_input = browser.find_element("id", "idPassword")
        password_input.send_keys(password)
        login_button = browser.find_element("id", "idConfirm")
        login_button.click()
        logger.info(f"Logged in to {ip}")

        cookies = browser.get_cookies()
        time.sleep(5)
        url = f"https://{ip}/servlet?m=mod_data&p=settings-upgrade&q=load"
        logger.debug(f"URL: {url}")
        browser.get(url)

        for cookie in cookies:
            browser.add_cookie(cookie)

        factory_reset_button = browser.find_element("id", "ResetFactory")
        factory_reset_button.click()

        alert = browser.switch_to.alert
        alert.accept()

    except Exception as e:
        logger.error(f"An error occurred while resetting phone with IP: {ip}")
        logger.error(str(e))
        return False
    return True

# Add csv intake for the IP address, username, and password of the Yealink phones
# Add a comfort message that says "Press Enter to continue"


result_filename = "result-" + str(int(time.time())) +".csv"
with open('phones.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    #logger.info(f"Number of phones to be reset: {len(list(csv_reader))}")
    input("Press Enter to reset phones, or Ctrl+C to exit...")

  

    for row in reader:
        print ("in for loop")
        ip, username, password = row
        logger.info(f"calling phone_reset: {ip}")
        phone_result = phone_reset(ip, username, password)

        if phone_result is not True:
            logger.error(f"Failed to reset phone with IP: {ip}")
            # Add to output csv
            with open(result_filename, 'a', newline='') as result_file:
                writer = csv.writer(result_file)
                writer.writerow([ip, "Failed"])
        else:
                    
            with open(result_filename, 'a', newline='') as result_file:
                writer = csv.writer(result_file)
                writer.writerow([ip, "Success"])

            # Close the browser
    browser.quit()
    

