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

def go_trubleshoot_list(driver):
    utils.send_input_key(driver, "नमस्ते", 30)
    expected_response = "tt"
    utils.send_message_by_selecting(driver, "कोई समस्या है?", expected_response)

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
        
        # saying hi to reset the bot conversation
        utils.send_input_key(driver, "नमस्ते", 30)

        # test 1: Have a problem? | कोई समस्या है?
        test1 = utils.send_message_by_selecting(driver, "कोई समस्या है?", expected_responses[0])
        save_test_result(test1, writer) 

        # test 2: Billing Issue | बिलिंग समस्या
        test2 = utils.send_message_by_selecting(driver, "बिलिंग समस्या", expected_responses[1])
        save_test_result(test2, writer)

        # test 3: Payment / Recharge Issue | भुगतान/रिचार्ज समस्या
        test3 = utils.send_message_by_selecting(driver, "भुगतान/रिचार्ज समस्या", expected_responses[2])
        save_test_result(test3, writer)

        # test 4: Mobile Network issue | मोबाइल नेटवर्क समस्या
        go_trubleshoot_list(driver)
        test4 = utils.send_message_by_selecting(driver, "मोबाइल नेटवर्क समस्या", expected_responses[3])
        save_test_result(test4, writer)

        # test 5: Voice bundles Issue | वॉयस बंडल समस्या
        go_trubleshoot_list(driver)
        test5 = utils.send_message_by_selecting(driver, "वॉयस बंडल समस्या", expected_responses[4])
        save_test_result(test5, writer)

        # test 6: Roaming service Issue | रोमिंग सेवा समस्या
        go_trubleshoot_list(driver)
        test6 = utils.send_message_by_selecting(driver, "रोमिंग सेवा समस्या", expected_responses[5])
        save_test_result(test6, writer)
