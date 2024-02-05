import os
import PySimpleGUI as sg
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from modules.form_filler import FormFiller
from modules.commons import Commons

commons = Commons()


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
            # sg.Button("Fill Dropdowns"),
            sg.Button("Cancel"),
        ],
    ]

    # Create text fields from csv rows
    input_dir = os.path.join(os.getcwd(), "data", "input", "input_fields.csv")
    csv_data = commons.read_csv_data(input_dir)
    for key, value in csv_data.items():
        layout.append(create_input_row(key, value))

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
    window = sg.Window(
        "Job Application Auto-Filler", layout, size=(300, 320), resizable=True
    )
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
                print("running Autofill...")
                # Initialize FormFiller and call fill_form
                # form_filler = FormFiller(driver)
                input_dir = os.path.join(
                    os.getcwd(), "data", "input", "input_fields.csv"
                )
                form_filler.fill_fields(driver)
            except Exception as e:
                sg.popup_error(f"Error filling form: {e}")

        # When 'Fill Dropdowns' is clicked
        # if event == "Fill Dropdowns" and driver and form_filler:
        #     try:
        #         # form_filler.select_dropdowns()
        #         pass
        #     except Exception as e:
        #         sg.popup_error(f"Whoops... {e}")

    # Close the window and the browser
    window.close()
    if driver:
        driver.quit()


if __name__ == "__main__":
    run_app()
