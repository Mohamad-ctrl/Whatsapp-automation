from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import pandas as pd
import os
from datetime import datetime
import explore_our_product_flow
import home_services

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to read expected responses from a CSV file
def read_expected_responses(csv_file_path):
    df = pd.read_csv(csv_file_path)
    expected_responses = df['expected_responses'].tolist()
    return expected_responses

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.maximize_window()

# Load WhatsApp Web
whatsapp_link = "https://web.whatsapp.com/"
driver.get(whatsapp_link)


# Home services flow
# Path to the CSV file containing expected responses
csv_file_path = 'C:\Users\Mohammad\Desktop\whatsapp'  # Update with the actual path to your CSV file

# Read expected responses from the CSV file
home_services_expected_responses = read_expected_responses(csv_file_path)

home_services.run_flow(driver, home_services_expected_responses)


driver.close()
