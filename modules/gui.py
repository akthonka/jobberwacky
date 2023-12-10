import PySimpleGUI as sg
import tkinter
from selenium import webdriver

# Assuming the fill_form function is defined as before


def gui_app():
    # Define the window's contents (layout)
    layout = [
        [sg.Text("Enter the URL of the job application website:")],
        [sg.Input(key="-URL-")],
        [sg.Button("Auto-Fill"), sg.Button("Cancel")],
    ]

    # Create the window
    window = sg.Window("Job Application Auto-Filler", layout)

    # Event loop
    while True:
        event, values = window.read()

        # End program if user closes window or clicks 'Cancel'
        if event == sg.WINDOW_CLOSED or event == "Cancel":
            break

        # When 'Auto-Fill' is clicked
        if event == "Auto-Fill":
            url = values["-URL-"]
            if url:
                driver = webdriver.Chrome()
                driver.get(url)

                # Add the logic to read form data and auto-fill
                form_data = read_csv_data("path/to/form_data.csv")
                fill_form(driver, form_data)

                # Optionally, close the browser
                # driver.quit()

    # Close the window
    window.close()


if __name__ == "__main__":
    gui_app()
