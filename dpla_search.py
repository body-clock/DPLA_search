import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DPLA_API_KEY")


def get_data_based_on_search_term(term):
    # request the data
    search_url = f'https://api.dp.la/v2/items?q={term}&api_key={api_key}'
    r = requests.get(search_url)

    if r.status_code == 200:
        # convert to json and extract "docs" list
        search_data = json.loads(r.text)
        total_data_list = search_data["docs"]
        return total_data_list
    else:
        print(f"Error:{r.status_code}")


# grab what we need from the total data
def extract_relevant_data(total_data_list):
    if len(total_data_list) > 0:
        extracted_data_list = []
        for result in total_data_list:
            # add extracted data to a new dict
            extracted_data_dict = {}
            extracted_data_dict["_ID_"] = result["id"]
            extracted_data_dict["_INGEST_DATE_"] = result["ingestDate"]
            extracted_data_dict["_DATA_PROVIDER_"] = result["dataProvider"]
            # append extracted data to total list
            extracted_data_list.append(extracted_data_dict)
        return extracted_data_list
    else:
        print("No results found.")


data = get_data_based_on_search_term("coffee")
if data:
    print(extract_relevant_data(data))
else:
    print("Try another search term.")
