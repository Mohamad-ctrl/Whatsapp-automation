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


def go_to_change_plan_list(driver):
    utils.send_input_key(driver, "नमस्ते", 30)
    # Test 1: I want to change my plan | Needs transelating... 
    utils.send_input_key(driver, "I want to change my plan", 10)


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

        # Test 1: I want to change my plan | Needs transelating... 
        test1 = utils.send_by_chat_and_comp(driver, "I want to change my plan", expected_responses[0])
        save_test_result(test1, writer)

        # Test 2: Switch to du | 
        go_to_change_plan_list(driver)
        test2 = utils.choose_and_compare(driver, "डु पर स्विच करें", expected_responses[1])
        save_test_result(test2, writer)

        # Test 3: Mobile | मोबाइल
        go_to_change_plan_list(driver)
        test3 = utils.send_message_by_selecting(driver, "मोबाइल", expected_responses[2])
        save_test_result(test3, writer)

        # Test 4: Mobile -> Change Prepaid plan | मोबाइल -> प्रीपेड प्लान बदलें
        test4 = utils.send_message_by_selecting(driver, "प्रीपेड प्लान बदलें", expected_responses[3])
        save_test_result(test4, writer)

        # Test 5: Mobile -> Change Postpaid plan | पोस्टपेड प्लान बदलें
        go_to_change_plan_list(driver)
        utils.send_message_by_selecting(driver, "मोबाइल", "tt")
        test5 = utils.send_message_by_selecting(driver, "पोस्टपेड प्लान बदलें", expected_responses[4])
        save_test_result(test5, writer)

        # Test 6: Mobile -> Prepaid ↔ Postpaid | मोबाइल -> प्रीपेड ↔ पोस्टपेड
        go_to_change_plan_list(driver)
        utils.send_message_by_selecting(driver, "मोबाइल", "tt")
        test6 = utils.send_message_by_selecting(driver, "प्रीपेड ↔ पोस्टपेड", expected_responses[5])
        save_test_result(test6, writer)

        # Test 7: Others | अन्य
        go_to_change_plan_list(driver)
        test7 = utils.send_message_by_selecting(driver, "अन्य", expected_responses[6])
        save_test_result(test7, writer)

        # Test 8: Others -> Change Fixed plan 
        test8 = utils.send_message_by_selecting(driver, "फिक्स्ड प्लान बदलें", expected_responses[7])
        save_test_result(test8, writer)

        # Test 9: Others -> Business to Personal | अन्य -> व्यवसाय से व्यक्तिगत
        go_to_change_plan_list(driver)
        utils.send_message_by_selecting(driver, "अन्य", "tt")
        test9 = utils.send_message_by_selecting(driver, "व्यवसाय से व्यक्तिगत", expected_responses[8])
        save_test_result(test9, writer)