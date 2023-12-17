import os, re
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

    def match_field_name(self, web_label, alt_field_map):
        # Normalize the label by removing non-alphanumeric characters and converting to lowercase
        normalized_label = re.sub(r"[^a-z0-9]", "", web_label.lower())

        # Exact match check
        if normalized_label in alt_field_map:
            foo = alt_field_map[normalized_label]
            print(f"Matched standard: {foo}")
            return foo

        # Attempt to find a match using regex with word boundaries for more complete matches
        # TODO: Might need reworking...
        print(f"Attempting regex for {normalized_label}")
        for alternative, standard in alt_field_map.items():
            pattern = (
                r"\b" + re.escape(alternative) + r"\b"
            )  # Use word boundaries to match whole words
            if re.search(pattern, normalized_label):
                print(f"Found a regex match: {normalized_label} = {standard}")
                return standard

        # Attempt to find a match using regex without word boundaries for partial matches
        print(f"Attempting regex for {normalized_label}")
        for alternative, standard in alt_field_map.items():
            if re.search(alternative, normalized_label):
                print(f"Found a regex match: {normalized_label} = {standard}")
                return standard

        return None

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
        alt_map_dir = os.path.join(os.getcwd(), "config", "field_alternatives.csv")
        alt_field_map = commons.alt_field_map(alt_map_dir)
        # print(alt_field_map)
        for detail in input_details:
            label = detail["label"]
            matched_field = self.match_field_name(label, alt_field_map)
            if matched_field and matched_field in csv_data:
                value = csv_data[matched_field]
                element = detail["element"]
                element.clear()
                element.send_keys(value)
                print(f"Sent field input: {value}")
