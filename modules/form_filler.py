import os
import argparse
import csv
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


class FormFiller:
    def __init__(self, driver):
        # Default Chrome driver
        self.driver = driver
        # List of possible values to select
        self.values_to_select = []

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

    def try_select_option(self, value):
        try:
            option = driver.find_element(By.XPATH, f"//div[text()='{value}']")
            option.click()
            print(f"found a match for {value}")
            return True
        except:
            print(f"no match found for {value}")
            return False

    def select_dropdowns(self, driver):
        # Update list of dropdown info
        input_dir = os.path.join(os.getcwd(), "data", "input", "dropdown_fields.csv")
        with open(input_dir, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.values_to_select.append(row["Value"])
        print(self.values_to_select)

        # Find all dropdown elements on the page
        dropdown_toggles = driver.find_elements(By.CSS_SELECTOR, ".fab-SelectToggle")
        print("number of toggles = ", len(dropdown_toggles))

        # Iterate over each toggle and try to select each value from the list
        for toggle in dropdown_toggles:
            print(toggle)
            toggle.click()
            time.sleep(1)  # Wait for dropdown options to appear
            for value in form_filler.values_to_select:
                print(f"processing {value}...")
                if form_filler.try_select_option(value):
                    print(f"!!! Selected {value} !!!")
                    break  # Move to the next dropdown if a value is successfully selected
            time.sleep(0.5)  # Optional: Brief pause before moving to the next dropdown

        dropdown_toggles = driver.find_elements(By.CSS_SELECTOR, ".fab-SelectToggle")
        print("number of toggles = ", len(dropdown_toggles))


if __name__ == "__main__":

    def wait_for_user_input():
        input("Press Enter in the console to start filling out the form...")

    # Dynamic URL
    # print("Current Working Directory:", os.getcwd())
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

    # Process dropdowns
    input("Press Enter to attempt to fillout dropdown lists")
    form_filler.select_dropdowns(driver)

    input("Press Enter to exit and close the browser...")
    driver.quit()
