import PySimpleGUI as sg
from selenium import webdriver
from modules.form_filler import FormFiller
from selenium.common.exceptions import WebDriverException
import os


def run_app():
    # Define the window's contents (layout)
    layout = [
        [sg.Text("Enter the URL of the job application website:")],
        [sg.Input(key="-URL-")],
        [sg.Button("Go"), sg.Button("Auto-Fill"), sg.Button("Cancel")],
    ]

    # Create the window
    window = sg.Window("Job Application Auto-Filler", layout)
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
