from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import pandas as pd
import os
from datetime import datetime
import explore_our_product_flow
import home_services
import explore_our_product_flow_ar

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to read expected responses from a CSV file
def read_expected_responses(csv_file_path):
    df = pd.read_csv(csv_file_path)
    expected_responses = df['expected_responses'].tolist()
    return expected_responses

# Initialize WebDriver
service = Service('C:/Users/Mohammad/.wdm/drivers/chromedriver/win64/127.0.6533.72/chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.maximize_window()

# Load WhatsApp Web
whatsapp_link = "https://web.whatsapp.com/"
driver.get(whatsapp_link)


# Home services flow
# Path to the CSV file containing expected responses
csv_file_path = 'C:\\Users\\Mohammad\\Desktop\\whatsapp\\explore_our_produect_expected_responses_ar.csv'  # Update with the actual path to your CSV file

# Read expected responses from the CSV file
home_services_expected_responses = read_expected_responses(csv_file_path)

explore_our_product_flow_ar.run_flow(driver, home_services_expected_responses)


driver.close()