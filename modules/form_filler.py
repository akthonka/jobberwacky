from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FormFiller:
    def __init__(self, driver_path, form_data):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.form_data = form_data

    def fill_text_field(self, field_name, value):
        """Fill a text field identified by its name."""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, field_name))
        )
        element.clear()
        element.send_keys(value)

    def fill_form(self, url):
        """Navigate to the form URL and fill in the form with provided data."""
        self.driver.get(url)

        # For each field in the form data, fill the field
        for field_name, value in self.form_data.items():
            self.fill_text_field(field_name, value)

        # Add logic for other types of fields like radio buttons, checkboxes, dropdowns, etc.

        # Uncomment the next line to submit the form
        # self.driver.find_element_by_id('submit-button-id').click()

    def close_browser(self):
        """Close the web browser."""
        self.driver.quit()


if __name__ == "__main__":
    # Example usage
    driver_path = "path/to/chromedriver"
    form_data = {
        "first_name": "John",
        "last_name": "Doe",
        # Add other form fields here
    }
    url = "https://example.com/job-application-form"

    filler = FormFiller(driver_path, form_data)
    filler.fill_form(url)
    # Uncomment the next line to close the browser after filling the form
    # filler.close_browser()
