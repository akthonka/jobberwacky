from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import csv
import argparse


def wait_for_user_input():
    input("Press Enter in the console to scrape fields...")


def scrape_fields(driver):
    # Scrape all input fields using Selenium
    inputs = driver.find_elements(By.TAG_NAME, "input")
    fields = []
    for input_field in inputs:
        field_info = {
            "Type": input_field.get_attribute("type"),
            "Name": input_field.get_attribute("name"),
            "ID": input_field.get_attribute("id"),
            "Class": input_field.get_attribute("class"),
            "Value": input_field.get_attribute("value"),
            "Placeholder": input_field.get_attribute("placeholder"),
            "Data-Automation-ID": input_field.get_attribute("data-automation-id"),
        }
        fields.append(field_info)
    return fields


def save_to_csv(fields, filename):
    if not fields:
        print("No fields found to save to CSV.")
        return

    # Saving the scraped data to a CSV file
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields[0].keys())
        writer.writeheader()
        for field in fields:
            writer.writerow(field)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Webpage fields scraper.")
    parser.add_argument("url", help="URL of the webpage to scrape")
    args = parser.parse_args()
    url = args.url  # URL from command-line argument

    driver = webdriver.Chrome()
    # url = "https://idtechex.bamboohr.com/careers/87?source=aWQ9MTU%3D"

    # Open a webpage
    driver.get(url)  # replace with your target URL

    # Start a thread to wait for user input
    user_input_thread = threading.Thread(target=wait_for_user_input)
    user_input_thread.start()

    # Wait for up to 60 seconds for the user to press Enter
    user_input_thread.join(timeout=60)

    # Check if the thread is still alive (user hasn't pressed Enter yet)
    if user_input_thread.is_alive():
        print("Timed out waiting for user input. Scraping fields automatically.")
        user_input_thread.join()  # Clean up the thread

    # Scrape fields from the webpage
    fields = scrape_fields(driver)

    # Save scraped fields to CSV
    if fields:
        # Extract the first 7 characters of the URL
        url_prefix = url[8:15].replace("://", "_").replace("/", "_")
        filename = f"{url_prefix}_fields.csv"

        save_to_csv(fields, filename)
        print(f"Fields saved to {filename}")
    else:
        print("No fields were scraped from the webpage.")

    # Close the browser
    driver.quit()
