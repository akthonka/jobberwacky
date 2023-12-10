import PySimpleGUI as sg
from selenium import webdriver
from modules.form_filler import FormFiller
from selenium.common.exceptions import WebDriverException
import os
import csv


def read_csv_data(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return {row["Name"]: row["Value"] for row in reader}


def run_app():
    # Read data from CSV
    input_dir = os.path.join(os.getcwd(), "data", "input", "input_fields.csv")
    csv_data = read_csv_data(input_dir)

    # Define the window's contents (layout)
    layout = [
        [sg.Text("Enter the URL of the job application website:")],
        [sg.Input(key="-URL-", expand_x=True)],
        [sg.Button("Go"), sg.Button("Auto-Fill"), sg.Button("Cancel")],
        [
            sg.Text("First Name:", size=(15, 1)),
            sg.InputText(
                key="-firstName-",
                default_text=csv_data.get("firstName", ""),
                expand_x=True,
            ),
        ],
        [
            sg.Text("Last Name:", size=(15, 1)),
            sg.InputText(
                key="-lastName-",
                default_text=csv_data.get("lastName", ""),
                expand_x=True,
            ),
        ],
        [
            sg.Text("Email:", size=(15, 1)),
            sg.InputText(
                key="-email-",
                default_text=csv_data.get("email", ""),
                expand_x=True,
            ),
        ],
        # Add more fields as needed
    ]

    # Create the window
    window = sg.Window("Job Application Auto-Filler", layout, resizable=True)
    driver = None

    # Event loop
    while True:
        event, values = window.read()

        # End program if user closes window or clicks 'Cancel'
        if event == sg.WINDOW_CLOSED or event == "Cancel":
            break

        # When 'Go' is clicked
        if event == "Go":
            url = values["-URL-"]
            if url:
                try:
                    driver = webdriver.Chrome()
                    driver.get(url)
                except WebDriverException as e:
                    sg.popup_error(f"Failed to open browser: {e}")
            else:
                sg.popup_error("Please enter a URL")

        # When 'Auto-Fill' is clicked
        if event == "Auto-Fill" and driver:
            try:
                # Initialize FormFiller and call fill_form
                form_filler = FormFiller(driver)
                input_dir = os.path.join(
                    os.getcwd(), "data", "input", "input_fields.csv"
                )
                form_data = form_filler.read_csv_data(input_dir)
                form_filler.fill_form(driver, form_data)
            except Exception as e:
                sg.popup_error(f"Error filling form: {e}")

    # Close the window and the browser
    window.close()
    if driver:
        driver.quit()


if __name__ == "__main__":
    run_app()
