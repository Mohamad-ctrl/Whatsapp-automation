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
import unicodedata
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')# Function to compare responses


def send_input_key(driver, textToSend, sleepTime = 15):
    # Locate the contenteditable div
    wait = WebDriverWait(driver, 1000)  # Adjust the timeout value as needed
    contenteditable_div = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][aria-label="Type a message"]'))
    )
    # Clear the input field 
    # contenteditable_div.clear()

    # Send the text to the input field
    contenteditable_div.send_keys(textToSend)

    # send an ENTER key to submit the message
    contenteditable_div.send_keys(Keys.ENTER)
    time.sleep(sleepTime)


def remove_newlines(text):
    return re.sub(r'\s+', '', text)

def get_latest_message(driver):
    try:
        # Find all elements with the class 'focusable-list-item'
        messages = driver.find_elements(By.CLASS_NAME, 'focusable-list-item')

        # Check if there are any messages
        if not messages:
            return None

        # Get the last message
        latest_message = messages[-1]

        # Find the text content within the latest message
        message_text_element = latest_message.find_element(By.CLASS_NAME, 'selectable-text')

        # Return the text content
        return message_text_element.text if message_text_element else None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None 

def click_last_button_by_text(driver, button_text):
    try:
        # Construct the XPath to locate all buttons by their text
        xpath = f"//button[contains(., '{button_text}')]"
        
        # Wait until at least one button is present
        buttons = WebDriverWait(driver, 1000).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        time.sleep(5)
        # Click the last button in the list
        if buttons:
            buttons[-1].click()
            logging.info(f"Successfully clicked the last button with text '{button_text}'")
        else:
            logging.warning(f"No buttons found with text '{button_text}'")

    except Exception as e:
        logging.error(f"An error occurred while clicking the last button with text '{button_text}': {e}")
        driver.save_screenshot(f'click_last_button_by_text_error_{button_text}.png')
        raise


def select_option_and_click_send(driver, option_name):
    try:
        # Construct the XPath to locate the button by its aria-label attribute
        xpath_option = f"//button[@role='radio' and @aria-label='{option_name}']"
        
        # Wait until the option button is present and clickable
        option_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_option))
        )
        
        # Click the option button
        option_button.click()
        logging.info(f"Successfully selected the option with name '{option_name}'")
        time.sleep(5)
        
        # Construct the XPath to locate the "send" button
        xpath_send_button = "//div[@role='button' and @tabindex='0' and @class='x78zum5 x6s0dn4 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1f6kntn xk50ysn x7o08j2 xtvhhri x1rluvsa x14yjl9h xudhj91 x18nykt9 xww2gxu xu306ak x12s1jxh xkdsq27 xwwtwea x1gfkgh9 x1247r65 xng8ra']/span[@data-icon='send']"
        
        # Wait until the send button is present and clickable
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_send_button))
        )
        
        # Click the send button
        send_button.click()
        logging.info("Successfully clicked the send button")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot.png')
        raise

def send_message_by_selecting(driver, optionName, expectedResponse, lang = None):
    if lang != None:
        click_last_button_by_text(driver, "يرجى الاختيار")
    else:
        click_last_button_by_text(driver, "Please select")
    time.sleep(5)
    select_option_and_click_send(driver, optionName)
    time.sleep(10)
    last_msg = get_latest_message(driver)
    print(str(last_msg))
    res = remove_newlines(str(last_msg)) == remove_newlines(expectedResponse)
    print("Passed" if res else "Failed")
    return {"Question": optionName, "Response From Bot": last_msg, "Expected Response": expectedResponse, "Test Results": "Passed" if res else "Failed"}


def go_to_explore_products_list(driver, sleepTime = 10):
    send_input_key(driver, "hi")
    time.sleep(sleepTime)
    expected_response = "Awesome ! We have a variety of plans and devices available.\nYou can choose from the list below"
    send_message_by_selecting(driver, "Explore our new products", expected_response)

def choose_and_compare(driver, option_name, expectedRes):
    try:
        # Construct the XPath to locate the option by its text
        xpath_option = f"//div[@role='button' and .//span[text()='{option_name}']]"
        
        # Wait until the option button is present and clickable
        option_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_option))
        )
        
        # Click the option button
        option_button.click()
        logging.info(f"Successfully clicked the option with name '{option_name}'")
        time.sleep(10)
        last_msg = get_latest_message(driver)
        print(str(last_msg))
        res = remove_newlines(str(last_msg)) == remove_newlines(expectedRes)
        return {"Question": option_name, "Response From Bot": last_msg, "Expected Response": expectedRes, "Test Results": "Passed" if res else "Failed"}
    except Exception as e:
        logging.error(f"An error occurred while clicking the option with name '{option_name}': {e}")
        driver.save_screenshot(f'click_option_by_name_error_{option_name}.png')
        raise

def send_by_chat_and_comp(driver, messageToSend, expected_response, sleepTime = None):
    try:
        if sleepTime == None:
            send_input_key(driver, messageToSend)
        else:
            send_input_key(driver, messageToSend, sleepTime)
        last_msg = get_latest_message(driver)
        print(str(last_msg))
        res = remove_newlines(str(last_msg)) == remove_newlines(expected_response)
        return {"Question": messageToSend, "Response From Bot": last_msg, "Expected Response": expected_response, "Test Results": "Passed" if res else "Failed"}
    except Exception as e:
        logging.error(f"An error occurred while sending this message >: '{messageToSend}': {e}")
        raise
