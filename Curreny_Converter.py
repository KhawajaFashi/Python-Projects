from requests import get
from pprint import PrettyPrinter

API_KEY = "fca_live_Vrveedr11jgoUJBikMigiOMjLaaHONSuiqSi0Zct"
BASE_URL = "https://api.freecurrencyapi.com/"

printer = PrettyPrinter()


def get_currency():
    endpoint = f"v1/latest?apikey={API_KEY}"

    url = BASE_URL + endpoint

    data = get(url).json()["data"]
    # printer.pprint(data)
    return data


def print_currencies(currencies):
    for currency, rate in currencies.items():
        print(f"Currency: {currency} - Rate: {rate}")


def exchange_rate(currencies, currency1, currency2):
    try:
        currency_to_convert = currencies[currency1]
    except Exception as e:
        print(f"Invalid currency {currency1}! Please the curreny correctly")
        return 0
    try:
        currency_convert_to = currencies[currency2]
    except Exception as e:
        print("Invalid currency {currency2}! Please the curreny correctly")
        return 0
    convert_usd = 1 / currency_to_convert
    converted_currency = convert_usd * currency_convert_to
    return converted_currency


def conversion(currencies, amount, currency1, currency2):
    rate = exchange_rate(currencies, currency1, currency2)
    if rate == 0:
        return 0
    print(f"The Exchange rate of {currency1} to {currency2} is {rate}")
    rate *= amount
    return rate


def convert_currency(data):
    while 1:
        command = input(
            '\nEnter "list" to print the currency list or Enter "convert" for currency conversion(q to quit): '
        )
        if command == "list":
            print_currencies(data)
            continue
        elif command == "convert":
            currency1 = input("\nEnter the currency you want to convert from: ").upper()
            currency2 = input("Enter the currency you want to convert to: ").upper()
            amount = float(
                input(f"Enter the amount of {currency1} you want to convert: ")
            )
            converted_amount = conversion(data, amount, currency1, currency2)
            if converted_amount != 0:
                print(f"The amount in {currency2} will be {converted_amount}")
        elif command == "q":
            return
        else:
            print("\nInvalid Input!")


data = get_currency()

convert_currency(data)
