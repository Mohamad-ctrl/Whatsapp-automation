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
    utils.send_input_key(driver, "مرحبا", 30)
    utils.send_input_key(driver, "أود تغيير باقتي", 10)


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
        utils.send_input_key(driver, "مرحبا", 30)

        # Test 1: I want to change my plan  | أود تغيير باقتي
        test1 = utils.send_by_chat_and_comp(driver, "أود تغيير باقتي", expected_responses[0], "ar")
        save_test_result(test1, writer)

        # Test 2: Switch to du | الانتقال إلى du
        go_to_change_plan_list(driver)
        test2 = utils.choose_and_compare(driver, "الانتقال إلى du", expected_responses[1], "ar")
        save_test_result(test2, writer)

        # Test 3: Mobile | خدمات الهاتف
        go_to_change_plan_list(driver)
        test3 = utils.send_message_by_selecting(driver, "خدمات الهاتف", expected_responses[2], "ar")
        save_test_result(test3, writer)

        # Test 4: Mobile -> Change Prepaid plan | باقة الدفع المسبق
        test4 = utils.send_message_by_selecting(driver, "باقة الدفع المسبق", expected_responses[3], "ar")
        save_test_result(test4, writer)

        # Test 5: Mobile -> Change Postpaid plan | باقةالدفع الآجل
        go_to_change_plan_list(driver)
        utils.send_message_by_selecting(driver, "خدمات الهاتف", "حسناً ! بالطبع يمكنني مساعدتك. اختر من القائمة التالية للمتابعة:")
        test5 = utils.send_message_by_selecting(driver, "باقةالدفع الآجل", expected_responses[4], "ar")
        save_test_result(test5, writer)

        # Test 6: Mobile -> Prepaid ↔ Postpaid | التبديل بين الباقات
        go_to_change_plan_list(driver)
        utils.send_message_by_selecting(driver, "خدمات الهاتف", "حسناً ! بالطبع يمكنني مساعدتك. اختر من القائمة التالية للمتابعة:")
        test6 = utils.send_message_by_selecting(driver, "التبديل بين الباقات", expected_responses[5], "ar")
        save_test_result(test6, writer)

        # Test 7: Others | أخرى
        go_to_change_plan_list(driver)
        test7 = utils.send_message_by_selecting(driver, "أخرى", expected_responses[6], "ar")
        save_test_result(test7, writer)

        # Test 8: Others -> Change Fixed plan | تغير باقة منزلية
        test8 = utils.send_message_by_selecting(driver, "تغير باقة منزلية", expected_responses[7], "ar")
        save_test_result(test8, writer)

        # Test 9: Others -> Business to Personal | أعمال إلى افراد
        go_to_change_plan_list(driver)
        utils.send_message_by_selecting(driver, "أخرى", "حسناً ! بالطبع يمكنني مساعدتك. اختر من القائمة التالية للمتابعة:")
        test9 = utils.send_message_by_selecting(driver, "أعمال إلى افراد", expected_responses[8], "ar")
        save_test_result(test9, writer)