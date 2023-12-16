import os, csv, time
from selenium.webdriver.common.by import By
from modules.commons import Commons


class FormFiller:
    def __init__(self, driver):
        self.driver = driver  # Default Chrome driver
        self.field_alternatives = {
            "firstName": ["firstName", "name"],
            "lastName": ["lastName", "surName"],
            "zipcode": ["zipcode", "zip", "postcode"],
            "phone": ["phone", "mobile"],
            "street": ["street", "address"],
            "state": ["state", "county"],
        }
        self.values_to_select = []  # List of possible values to select

    def fill_fields(self, driver):
        commons = Commons()
        csv_dir = os.path.join(os.getcwd(), "data", "input", "input_fields.csv")
        csv_data = commons.read_csv_data(csv_dir)
        # print(csv_data)

        input_dir = os.path.join(os.getcwd(), "scripts", "dank.js")
        js_code = commons.read_javascript(input_dir)
        input_details = driver.execute_script(js_code)
        # print(input_details)

        # Fill in the fields
        for detail in input_details:
            # Currently only matches "dumb" text
            label = detail["label"]
            if label in csv_data:
                value = csv_data[label]
                element = detail["element"]
                element.clear()  # Clear any pre-filled value
                element.send_keys(value)
