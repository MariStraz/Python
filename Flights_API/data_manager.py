import requests
import json

ENDPOINT = "https://api.sheety.co/"
header = {
    "Content-Type": "application/json",
    # "Authorization": os.environ["TOKEN"]
    # "Authorization": ""
}
row = {
    "price": {
        "prices": "test",
        "city": "test",
        "iATA code": "test",
        "lowest Price": "test",
    }
}


class DataManager:
    #This class is responsible for talking to the Google Sheet sheety.co.
    # Because of limited usage count, uses local file instead of google sheet

    # result = requests.post(url=endpoint_addrow, json=row, headers=header)
    # print(result.json())

    def __init__(self):
        self.data = None
        self.endpoint = ENDPOINT
        self.header = header

    def get_data_site(self):
        """loads data from sheety.co"""
        result = requests.get(url=self.endpoint, headers=self.header)
        result.raise_for_status()
        self.data = result.json()["prices"]
        with open("sheet.json", "w") as file:
            json.dump(self.data, file, indent=4)

    def get_data_file(self):
        """loads data from local file sheet.json"""
        with open("sheet.json", "r") as file:
            self.data = json.load(file)

    def put_row_site(self,column, row):
        """Writes data to google sheet with name 'price'
        row: dictionary , column: key from dict
        """
        body={
            "price": {
                column: row[column],
            }
        }
        address = f"{self.endpoint}/{row["id"]}"
        result = requests.put(url=address, json=body)
        # print(result.text)
        result.raise_for_status()

