from dotenv import load_dotenv
import PySimpleGUI as sg
import pandas as pd
import webbrowser
import requests
import json
import os

load_dotenv()
api_key = os.getenv("DPLA_API_KEY")

# GUI
search_layout = [[sg.Text('What would you like to search?'), sg.InputText(key='_TERM_')],
                 [sg.Button('Search')]]

main_layout = [[sg.Frame('Input', search_layout)]]
enter_data_window = sg.Window('DPLA Search', main_layout)


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
            # TODO account for missing keys
            extracted_data_dict = {}
            extracted_data_dict["_ID_"] = result["id"]
            extracted_data_dict["_INGEST_DATE_"] = result["ingestDate"]
            extracted_data_dict["_DATA_PROVIDER_"] = result["dataProvider"]
            # append extracted data to total list
            extracted_data_list.append(extracted_data_dict)
        return extracted_data_list
    else:
        print("No results found.")


def create_dataframe_and_convert_to_html_table(data_dict, term):
    df = pd.DataFrame(data_dict)

    # TODO continue styling
    # table style
    html = {
        df.style
        .set_caption(f"Search results for: {term}")
        .render()
    }
    html_list = list(html)
    print(html)
    # write to file
    with open("search_results.html", "w") as f:
        f.write(html_list[0])


# main Loop
program_running = True
if program_running:
    event, values = enter_data_window.Read()
    if event == 'Search':
        search_term = values["_TERM_"]
        data = get_data_based_on_search_term(values["_TERM_"])
        if data:
            relevant_data = extract_relevant_data(data)
            create_dataframe_and_convert_to_html_table(relevant_data, search_term)

            file_location = "/Users/patrick/Git/DPLA_search/search_results.html"
            webbrowser.open(f"file://{file_location}", new=2)
        else:
            print("Try another search term.")
