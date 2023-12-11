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


def create_input_row(field_name, default_value=""):
    return [
        sg.Text(f"{field_name}:", size=(15, 1)),
        sg.InputText(
            default_text=default_value, key=f"-{field_name.upper()}-", expand_x=True
        ),
    ]


def run_app():
    # Set theme
    sg.theme("LightBrown2")

    # Define the window's contents (layout)
    input_dir = os.path.join(os.getcwd(), "data", "input", "input_fields.csv")
    layout = [
        [sg.Text("Enter the URL of the job application website:")],
        [sg.Input(key="-URL-", expand_x=True)],
        [
            sg.Button("Go"),
            sg.Button("Auto-Fill"),
            sg.Button("Fill Dropdowns"),
            sg.Button("Cancel"),
        ],
    ]

    # Create text fields from csv rows
    with open(input_dir, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            layout.append(create_input_row(row["Name"], row["Value"]))

    # Add empty fields (i.e. for login data)
    custom_fields = [
        [
            sg.Text("Custom 1:", size=(15, 1)),
            sg.InputText(key="-custom1-", expand_x=True),
        ],
        [
            sg.Text("Custom 2:", size=(15, 1)),
            sg.InputText(key="-custom2-", expand_x=True),
        ],
    ]
    layout.append(custom_fields)

    # Create the window
    window = sg.Window("Job Application Auto-Filler", layout, resizable=True)
    driver = None
    form_filler = None

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
                    form_filler = FormFiller(driver)
                except WebDriverException as e:
                    sg.popup_error(f"Failed to open browser: {e}")
            else:
                sg.popup_error("Please enter a URL")

        # When 'Auto-Fill' is clicked
        if event == "Auto-Fill" and driver:
            try:
                # Initialize FormFiller and call fill_form
                # form_filler = FormFiller(driver)
                input_dir = os.path.join(
                    os.getcwd(), "data", "input", "input_fields.csv"
                )
                form_data = form_filler.read_csv_data(input_dir)
                form_filler.fill_form(driver, form_data)
            except Exception as e:
                sg.popup_error(f"Error filling form: {e}")

        # When 'Fill Dropdowns' is clicked
        if event == "Fill Dropdowns" and driver and form_filler:
            try:
                form_filler.select_dropdowns()
            except Exception as e:
                sg.popup_error(f"Whoops... {e}")

    # Close the window and the browser
    window.close()
    if driver:
        driver.quit()


if __name__ == "__main__":
    run_app()
