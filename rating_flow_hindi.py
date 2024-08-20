from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import utils
import os
from datetime import datetime


def save_test_result(test_result, writer):
    df = pd.DataFrame([test_result])
    df.to_excel(writer, sheet_name='Messages Logs', index=False, header=False, startrow=writer.sheets['Messages Logs'].max_row)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')# Function to compare responses

def run_flow(driver, expected_responses):
    # Create the file name
    currentDate = datetime.now()
    formatted_date_time = currentDate.strftime("%d-%m_%I.%M%p").lower()
    file_name = f'whatsapp_messages_results_{formatted_date_time}.xlsx'
    print(file_name)

    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    result_file = os.path.join(script_directory, file_name)

    with pd.ExcelWriter(result_file, mode='w', engine='openpyxl') as writer:
        writer.book.create_sheet('Messages Logs')

        # Saying hi to reset the bot conversation
        utils.send_input_key(driver, "नमस्ते", 30)

        # Test 1: clicking No to enter the rating flow
        # Explore our new products
        utils.send_message_by_selecting(driver, "नए उत्पाद देखें", "tt")
        # Postpaid plans
        utils.send_message_by_selecting(driver, "पोस्टपेड योजनाएँ", "tt")
        # No
        test1 = utils.choose_and_compare(driver, "नहीं", expected_responses[0])
        save_test_result(test1, writer)

        # Test 2: rating form 1 to 10
        test2 = utils.send_message_by_selecting(driver, "1", expected_responses[1])
        save_test_result(test2, writer)
        
        # Test 3: clicking no for (did we resolve your issue ?)
        test3 = utils.choose_and_compare(driver, "नहीं", expected_responses[2])
        save_test_result(test3, writer)

        # Test 4: sending the feedback
        test4 = utils.send_by_chat_and_comp(driver, "automated test feedback for the hindi flow", expected_responses[3])
        save_test_result(test4, writer)
