import os
import urllib.parse
import requests
from dotenv import load_dotenv

load_dotenv()

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = os.getenv("MAPQUEST_API_KEY") 

def print_header(title):
    print("\033[96m" + "=" * 50)
    print(title.center(50))
    print("=" * 50 + "\033[0m")

def print_success_message(message):
    print("\033[92m" + message + "\033[0m")

def print_error_message(message):
    print("\033[91m" + message + "\033[0m")

def print_info_message(message):
    print("\033[93m" + message + "\033[0m")

while True:
    print_header("MAPQUEST DIRECTIONS API")

    orig = input("\033[94mStarting Location (or type 'quit' to exit): \033[0m")
    if orig.lower() == "quit" or orig.lower() == "q":
        print_info_message("Exiting program. Goodbye!")
        break

    dest = input("\033[94mDestination (or type 'quit' to exit): \033[0m")
    if dest.lower() == "quit" or dest.lower() == "q":
        print_info_message("Exiting program. Goodbye!")
        break

    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})

    print_info_message(f"Request URL: {url}\n")

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print_success_message("API Status: Success - Route found!\n")

        print_header(f"Route Summary: {orig} to {dest}")
        print("\033[95mTrip Duration: \033[0m" + json_data["route"]["formattedTime"])
        print("\033[95mDistance: \033[0m" + str("{:.2f}".format(json_data["route"]["distance"] * 1.61)) + " km")

        if "fuelUsed" in json_data["route"]:
            print("\033[95mFuel Used (Ltr): \033[0m" + str("{:.2f}".format(json_data["route"]["fuelUsed"] * 3.78)))
        else:
            print_info_message("Fuel data is not available for this route.")

        print_header("Turn-by-Turn Directions")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print("\033[94m" + each["narrative"] + " (" + str("{:.2f}".format(each["distance"] * 1.61)) + " km)\033[0m")
            print("-" * 50)

    elif json_status == 402:
        print_error_message("Invalid input: Unable to calculate route. Check the locations entered.")

    elif json_status == 611:
        print_error_message("Error: Missing entry for one or both locations.")

    else:
        print_error_message(f"API Error - Status Code: {json_status}")
        print_info_message("Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes")
