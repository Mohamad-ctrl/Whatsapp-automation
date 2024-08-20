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
    expectedRes = "لحصولك على المعلومات بشكل أفضل ، اختر نوع الجهاز الذي تستعلم عنه ؟ يمكنك الاختيار من  القائمة أدناه"
    utils.send_message_by_selecting(driver, "أجهزة", expectedRes, "ar")

def go_to_explore_products_list(driver, sleepTime = 10):
    utils.send_input_key(driver, "مرحبا")
    time.sleep(sleepTime)
    expected_response = "رائع ! لدينا مجموعة متنوعة من الباقات والأجهزة المتاحة. يمكنك الاختيار من القائمة ادناه"
    utils.send_message_by_selecting(driver, "ﻣﻨﺘﺠﺎت ﺟﺪﯾﺪة", expected_response, "ar")

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
        utils.send_input_key(driver, "مرحبا")
        time.sleep(15)

        # Test 1: Explore our new products | منتجات جديدة
        test1 = utils.send_message_by_selecting(driver, "ﻣﻨﺘﺠﺎت ﺟﺪﯾﺪة", expected_responses[0], "ar")
        save_test_result(test1, writer)

        # Test 2: Enterprise Mobile | باقات الجوال للشركات
        test2 = utils.send_message_by_selecting(driver, "باقات الجوال للشركات", expected_responses[1], "ar")
        save_test_result(test2, writer)

        # Test 3: Enterprise Fixed | الباقات الثابتة للشركات
        go_to_explore_products_list(driver)
        test3 = utils.send_message_by_selecting(driver, "الباقات الثابتة للشركات", expected_responses[2], "ar")
        save_test_result(test3, writer)

        # Test 4: Check my order status | تتبع حالة طلبي
        go_to_explore_products_list(driver)
        test4 = utils.send_message_by_selecting(driver, "تتبع حالة طلبي", expected_responses[3], "ar")
        save_test_result(test4, writer)

        # Test 5: Prepaid Plans | باقات الدفع المسبق
        go_to_explore_products_list(driver)
        test5 = utils.send_message_by_selecting(driver, "باقات الدفع المسبق", expected_responses[4], "ar")
        save_test_result(test5, writer)

        # Test 6: Postpaid plans | باقات الدفع الآجل
        go_to_explore_products_list(driver)
        test6 = utils.send_message_by_selecting(driver, "باقات الدفع الآجل", expected_responses[5], "ar")
        save_test_result(test6, writer)

        # Test 7: Home plans | باقات المنزل
        go_to_explore_products_list(driver)
        test7 = utils.send_message_by_selecting(driver, "باقات المنزل", expected_responses[6], "ar")
        save_test_result(test7, writer)

        # Test 8: Home Wireless | الباقات الالسلكية
        test8 = utils.choose_and_compare(driver, "الباقات الالسلكية", expected_responses[7], "ar")
        save_test_result(test8, writer)

        # Test 9: Home Fiber | الباقات السلكية
        go_to_explore_products_list(driver)
        utils.send_message_by_selecting(driver, "باقات المنزل", expected_responses[6], "ar")
        test9 = utils.choose_and_compare(driver, "الباقات السلكية", expected_responses[8], "ar")
        save_test_result(test9, writer)

        # Test 10: Devices | أجهزة
        go_to_explore_products_list(driver)
        test10 = utils.send_message_by_selecting(driver, "أجهزة", expected_responses[9], "ar")
        save_test_result(test10, writer)

        # Test 11: Tablets | الأجهزة اللوحية
        go_to_devices(driver)
        test11 = utils.send_message_by_selecting(driver, "الأجهزة اللوحية", expected_responses[10], "ar")
        save_test_result(test11, writer)

        # Test 12: Phones | الهواتف
        go_to_devices(driver)
        test12 = utils.send_message_by_selecting(driver, "الهواتف", expected_responses[11], "ar")
        save_test_result(test12, writer)

        # Test 13: Apple | آبل
        test13 = utils.choose_and_compare(driver, "آبل", expected_responses[12], "ar")
        save_test_result(test13, writer)
