from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta

data_sheet = DataManager()
flight_search = FlightSearch()
data_sheet.get_data_file()
# print(data_sheet.data)

today = datetime.today()
future_date = today + timedelta(days=6 * 30)
current_date = today.strftime("%d/%m/%Y")
end_date = future_date.strftime("%d/%m/%Y")
print(current_date)
print(end_date)

for item in data_sheet.data:
    flight_search.get_flight(item["iataCode"], current_date, end_date)
    if flight_search.price is not None:
        print(
            f"{item["city"]}: {flight_search.price} tam z {flight_search.departure_begin_from} " +
            f"spat z {flight_search.departure_end_from}")
        if float(flight_search.price) < float(item["lowestPrice"]):
            print(f"{flight_search.departure_begin} ... 😀✈️")






# Fill IATA codes to sheet
# data_sheet.det_data_site()
# for item in data_sheet.data:
#     item["iataCode"] = flight_search.get_city_code(item["city"])
#     # print(item["iataCode"])
#     row = {
#         "id": item["id"],
#         "iataCode": item["iataCode"]
#     }
#     data_sheet.put_row_site("iataCode",row)

# print(data_sheet.data)
# row = {
#     "id":2,
#     "iataCode": "test"
# }
# data_sheet.put_row_site(row)
