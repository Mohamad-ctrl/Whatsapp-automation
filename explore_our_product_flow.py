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


def go_to_devices(driver):
    utils.go_to_explore_products_list(driver)
    expectedRes = "To give you the best info, which device are you curious about ?  You can choose from the list below"
    utils.send_message_by_selecting(driver, "Devices", expectedRes)

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
        utils.send_input_key(driver, "hi")
        time.sleep(15)

        # Test 1: Explore our new products
        test1 = utils.send_message_by_selecting(driver, "Explore our new products", expected_responses[0])
        save_test_result(test1, writer)

        # Test 2: Enterprise Mobile
        test2 = utils.send_message_by_selecting(driver, "Enterprise Mobile", expected_responses[1])
        save_test_result(test2, writer)

        # Test 3: Enterprise Fixed
        utils.go_to_explore_products_list(driver)
        test3 = utils.send_message_by_selecting(driver, "Enterprise Fixed", expected_responses[2])
        save_test_result(test3, writer)

        # Test 4: Check my order status
        utils.go_to_explore_products_list(driver)
        test4 = utils.send_message_by_selecting(driver, "Check my order status", expected_responses[3])
        save_test_result(test4, writer)

        # Test 5: Prepaid Plans
        utils.go_to_explore_products_list(driver)
        test5 = utils.send_message_by_selecting(driver, "Prepaid Plans", expected_responses[4])
        save_test_result(test5, writer)

        # Test 6: Postpaid plans
        utils.go_to_explore_products_list(driver)
        test6 = utils.send_message_by_selecting(driver, "Postpaid plans", expected_responses[5])
        save_test_result(test6, writer)

        # Test 7: Home plans
        utils.go_to_explore_products_list(driver)
        test7 = utils.send_message_by_selecting(driver, "Home plans", expected_responses[6])
        save_test_result(test7, writer)

        # Test 8: Home Wireless
        test8 = utils.choose_and_compare(driver, "Home Wireless", expected_responses[7])
        save_test_result(test8, writer)

        # Test 9: Home Fiber
        utils.go_to_explore_products_list(driver)
        utils.send_message_by_selecting(driver, "Home plans", "Which home plan suits your needs?")
        test9 = utils.choose_and_compare(driver, "Home Fiber", expected_responses[8])
        save_test_result(test9, writer)

        # Test 10: Devices
        utils.go_to_explore_products_list(driver)
        test10 = utils.send_message_by_selecting(driver, "Devices", expected_responses[9])
        save_test_result(test10, writer)

        # Test 11: Tablets
        go_to_devices(driver)
        test11 = utils.send_message_by_selecting(driver, "Tablets", expected_responses[10])
        save_test_result(test11, writer)

        # Test 12: Phones
        go_to_devices(driver)
        test12 = utils.send_message_by_selecting(driver, "Phones", expected_responses[11])
        save_test_result(test12, writer)

        # Test 13: Apple
        test13 = utils.choose_and_compare(driver, "Apple", expected_responses[12])
        save_test_result(test13, writer)
