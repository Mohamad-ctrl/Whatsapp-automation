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

def go_home_services_list(driver):
    utils.send_input_key(driver, "hi")
    expected_response = "I'm sorry to hear that, what is your issue related to? You can choose from the below"
    utils.send_message_by_selecting(driver, "Home services", expected_response)

def go_to_streaming_list(driver, moveOneMoreStep = None):
    go_home_services_list(driver)
    expected_response = "Awesome ! I can help you with this. Please choose an option of your choice"
    utils.send_message_by_selecting(driver, "Streaming services", expected_response)
    if moveOneMoreStep != None:
        expected_response = "Please select from the list below:"
        utils.send_message_by_selecting(driver, "Amazon Prime", expected_response)


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
        
        # saying hi to reset the bot conversation and going to the home services list
        utils.send_input_key(driver, "hi")
        go_home_services_list(driver)

        # test 1: Home relocation
        test1 = utils.send_message_by_selecting(driver, "Home relocation", expected_responses[0])
        save_test_result(test1, writer)

        # test 2: Home Plans
        go_home_services_list(driver)
        test2 = utils.send_message_by_selecting(driver, "Home plans", expected_responses[1])
        save_test_result(test2, writer)

        # test 3: Home Plans -> Wireless
        test3 = utils.send_message_by_selecting(driver, "Wireless", expected_responses[2])
        save_test_result(test3, writer)

        # test 4: Home Plans -> Fiber
        go_home_services_list(driver)
        utils.send_message_by_selecting(driver, "Home plans", "Which home plan suits your needs?")
        test4 = utils.send_message_by_selecting(driver, "Home Fiber", expected_responses[3])
        save_test_result(test4, writer)

        # test 5: Manage Home TV packages
        go_home_services_list(driver)
        test5 = utils.send_message_by_selecting(driver, "Manage Home TV packages", expected_responses[4])
        save_test_result(test5, writer)

        # test 6: Manage Home TV packages -> Clicking No 
        test6 = utils.choose_and_compare(driver, "No", expected_responses[5])
        save_test_result(test6, writer)

        # test 7: Streaming services
        go_home_services_list(driver)
        test7 = utils.send_message_by_selecting(driver, "Streaming services", expected_responses[6])
        save_test_result(test7, writer)

        # test 8: OSN
        test8 = utils.send_message_by_selecting(driver, "OSN", expected_responses[7])
        save_test_result(test8, writer)

        # test 9: Disney Plus
        go_to_streaming_list(driver)
        test9 = utils.send_message_by_selecting(driver, "Disney Plus", expected_responses[7])
        save_test_result(test9, writer)

        # test 10: Amazon Prime
        go_home_services_list(driver)
        test10 = utils.send_message_by_selecting(driver, "Amazon Prime", expected_responses[7])
        save_test_result(test10, writer)

        # test 11: How to activate
        test11 = utils.send_message_by_selecting(driver, "How to activate", expected_responses[8])
        save_test_result(test11, writer)

        # test 12: How to deactivate
        go_to_streaming_list(driver, "move one step")
        test12 = utils.send_message_by_selecting(driver, "How to deactivate", expected_responses[8])
        save_test_result(test12, writer)

        # test 13: Facing an issue
        go_to_streaming_list(driver, "move one step")
        test13 = utils.send_message_by_selecting(driver, "Facing an issue", expected_responses[8])
        save_test_result(test13, writer)

        # test 14: Clicking No
        test14 = utils.choose_and_compare(driver, "No", expected_responses[5])
        save_test_result(test14, writer)