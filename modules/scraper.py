# Import necessary libraries
from bs4 import BeautifulSoup
import requests


class JobApplicationScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def fetch_page(self):
        """Fetch the page HTML content and create a BeautifulSoup object."""
        try:
            response = requests.get(self.url)
            # Ensure the request was successful
            if response.status_code == 200:
                self.soup = BeautifulSoup(response.text, "html.parser")
            else:
                print(f"Failed to retrieve webpage: Status code {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def scrape_form_fields(self):
        """Scrape the form fields from the page."""
        if not self.soup:
            print("Soup object not initialized. Call fetch_page() first.")
            return

        # Find form elements (e.g., input, select)
        forms = self.soup.find_all("form")
        for form in forms:
            print(f"Form: {form.get('id') or form.get('name')}")
            inputs = form.find_all("input")
            for input in inputs:
                print(
                    f"Input Field - Name: {input.get('name')}, Type: {input.get('type')}"
                )

            selects = form.find_all("select")
            for select in selects:
                print(f"Select Field - Name: {select.get('name')}")
                # You can also iterate over options in select here

            # Add other form elements as needed (e.g., textarea, button)


if __name__ == "__main__":
    print("I'm actually running dw...")
    # Example usage
    url = "https://jobs.mckinsey.com/careers/ApplicationMethods?folderId=20159"
    scraper = JobApplicationScraper(url)
    scraper.fetch_page()
    scraper.scrape_form_fields()
