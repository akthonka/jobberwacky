import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import os

print("Current Working Directory:", os.getcwd())


def read_csv_data(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def fill_form(driver, form_data):
    for field in form_data:
        try:
            element = driver.find_element(
                By.XPATH, f"//*[contains(@name, '{field['Name']}')]"
            )
            element.clear()
            element.send_keys(field["Value"])
        except Exception as e:
            print(f"Could not find or fill the field: {field['Name']}. Error: {e}")


def wait_for_user_input():
    input("Press Enter in the console to start filling out the form...")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    url = "https://idtechex.bamboohr.com/careers/87?source=aWQ9MTU%3D"
    driver.get(url)  # Replace with the actual URL of the form

    # Start a thread to wait for user input
    user_input_thread = threading.Thread(target=wait_for_user_input)
    user_input_thread.start()

    # Wait for the user input thread to complete
    user_input_thread.join()

    form_data = read_csv_data("../data/input/input_fields.csv")
    fill_form(driver, form_data)

    input("Press Enter to exit and close the browser...")
    driver.quit()
