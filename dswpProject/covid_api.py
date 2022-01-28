import requests
import db_context


def get_countries():
    res = requests.request("GET", "https://api.covid19api.com/countries")
    return res


# def get_days():
#     context = db_context.dbContext()
#     countries = context.get_countries()
#     result = []
#     for country in countries:
#         result.append(requests.request("GET", f"https://api.covid19api.com/country/{country[0]}"))
#     return result


def get_days(iso2):
    res = requests.request("GET", f"https://api.covid19api.com/country/{iso2}")
    return res
