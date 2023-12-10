import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import os
import argparse


class FormFiller:
    def __init__(self, driver):
        self.driver = driver

    def read_csv_data(self, file_path):
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def fill_form(self, driver, form_data):
        for field in form_data:
            try:
                element = driver.find_element(
                    By.XPATH, f"//*[contains(@name, '{field['Name']}')]"
                )
                element.clear()
                element.send_keys(field["Value"])
            except Exception as e:
                print(f"Could not find or fill the field: {field['Name']}. Error: {e}")


if __name__ == "__main__":

    def wait_for_user_input():
        input("Press Enter in the console to start filling out the form...")

    print("Current Working Directory:", os.getcwd())

    # Dynamic URL
    # parser = argparse.ArgumentParser(description="Webpage fields scraper.")
    # parser.add_argument("url", help="URL of the webpage to scrape")
    # args = parser.parse_args()
    # url = args.url  # URL from command-line argument

    # Static URL for testing purposes
    url = "https://idtechex.bamboohr.com/careers/87?source=aWQ9MTU%3D"
    driver = webdriver.Chrome()
    driver.get(url)

    # Start a thread to wait for user input
    user_input_thread = threading.Thread(target=wait_for_user_input)
    user_input_thread.start()

    # Wait for the user input thread to complete
    user_input_thread.join()
    form_filler = FormFiller(driver)
    input_dir = os.path.join(os.getcwd(), "data", "input", "input_fields.csv")
    form_data = form_filler.read_csv_data(input_dir)
    form_filler.fill_form(driver, form_data)

    input("Press Enter to exit and close the browser...")
    driver.quit()
