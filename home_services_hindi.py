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
    utils.send_input_key(driver, "नमस्ते", 30)
    expected_response = "tt"
    # home services
    utils.send_message_by_selecting(driver, "होम सेवाएँ", expected_response)

def go_to_streaming_list(driver, moveOneMoreStep = None):
    go_home_services_list(driver)
    expected_response = "tt"
    # streaming services
    utils.send_message_by_selecting(driver, "स्ट्रीमिंग सेवाएँ", expected_response)
    if moveOneMoreStep != None:
        expected_response = "tt"
        # amazon prime
        utils.send_message_by_selecting(driver, "ऐमज़ान प्रधान", expected_response)


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
        utils.send_input_key(driver, "नमस्ते", 30)
        go_home_services_list(driver)

        # test 1: Home relocation | होम स्थानांतरण
        test1 = utils.send_message_by_selecting(driver, "होम स्थानांतरण", expected_responses[0])
        save_test_result(test1, writer)

        # test 2: Home Plans | होम प्लान
        go_home_services_list(driver)
        test2 = utils.send_message_by_selecting(driver, "होम प्लान", expected_responses[1])
        save_test_result(test2, writer)

        # test 3: Home Plans -> Wireless | होम प्लान -> होम वायरलेस
        test3 = utils.send_message_by_selecting(driver, "होम वायरलेस", expected_responses[2])
        save_test_result(test3, writer)

        # test 4: Home Plans -> Fiber | होम प्लान -> होम फाइबर
        go_home_services_list(driver)
        utils.send_message_by_selecting(driver, "होम प्लान", "tt")
        test4 = utils.send_message_by_selecting(driver, "होम फाइबर", expected_responses[3])
        save_test_result(test4, writer)

        # test 5: Manage Home TV packages | होम टीवी पैकेज प्रबंधित करें
        go_home_services_list(driver)
        test5 = utils.send_message_by_selecting(driver, "होम टीवी पैकेज प्रबंधित करें", expected_responses[4])
        save_test_result(test5, writer)

        # test 6: Manage Home TV packages -> Clicking No | होम टीवी पैकेज प्रबंधित करें -> नहीं
        test6 = utils.choose_and_compare(driver, "नहीं", expected_responses[5])
        save_test_result(test6, writer)

        # test 7: Streaming services | स्ट्रीमिंग सेवाएँ
        go_home_services_list(driver)
        test7 = utils.send_message_by_selecting(driver, "स्ट्रीमिंग सेवाएँ", expected_responses[6])
        save_test_result(test7, writer)

        # test 8: OSN | ओएसएन
        test8 = utils.send_message_by_selecting(driver, "ओएसएन", expected_responses[7])
        save_test_result(test8, writer)

        # test 9: Disney Plus | डिज़्नी प्लस
        go_to_streaming_list(driver)
        test9 = utils.send_message_by_selecting(driver, "डिज़्नी प्लस", expected_responses[7])
        save_test_result(test9, writer)

        # test 10: Amazon Prime | ऐमज़ान प्रधान
        go_to_streaming_list(driver)
        test10 = utils.send_message_by_selecting(driver, "ऐमज़ान प्रधान", expected_responses[7])
        save_test_result(test10, writer)

        # test 11: How to activate | कैसे सक्रिय करें
        test11 = utils.send_message_by_selecting(driver, "कैसे सक्रिय करें", expected_responses[8])
        save_test_result(test11, writer)

        # test 12: How to deactivate | निष्क्रिय कैसे करें
        go_to_streaming_list(driver, "move one step")
        test12 = utils.send_message_by_selecting(driver, "निष्क्रिय कैसे करें", expected_responses[8])
        save_test_result(test12, writer)

        # test 13: Facing an issue | एक समस्या है
        go_to_streaming_list(driver, "move one step")
        test13 = utils.send_message_by_selecting(driver, "एक समस्या है", expected_responses[8])
        save_test_result(test13, writer)

        # test 14: Clicking No | नहीं
        test14 = utils.choose_and_compare(driver, "नहीं", expected_responses[5])
        save_test_result(test14, writer)