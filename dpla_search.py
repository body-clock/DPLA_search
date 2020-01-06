from dotenv import load_dotenv
import PySimpleGUI as sg
from pathlib import Path
import pandas as pd
import webbrowser
import requests
import json
import os

load_dotenv()
api_key = os.getenv("DPLA_API_KEY")

# GUI
sg.theme("DarkRed1")

search_layout = [[sg.Text('What would you like to search?'), sg.InputText(key='Term', size=(20,50))],
                 [sg.Button('Search')]]

main_layout = [[sg.Frame('Input', search_layout)]]
enter_data_window = sg.Window('DPLA Search', main_layout)


def get_data_based_on_search_term(term):
    # request the data
    search_url = f'https://api.dp.la/v2/items?q={term}&api_key={api_key}'
    r = requests.get(search_url)

    if r.status_code == 200 and term != '':
        # convert to json and extract "docs" list
        search_data = json.loads(r.text)
        total_data_list = search_data["docs"]
        return total_data_list
    elif r.status_code != 200:
        print(f"Error:{r.status_code}")
    else:
        print("Invalid search term.")


# grab what we need from the total data
def extract_relevant_data(total_data_list):
    if len(total_data_list) > 0:
        extracted_data_list = []
        for result in total_data_list:
            # add extracted data to a new dict
            extracted_data_dict = {"ID": result["id"], "Ingest Date": result["ingestDate"]}
            # account for lack of provider
            if result["dataProvider"]:
                extracted_data_dict["Data Provider"] = result["dataProvider"]
            else:
                extracted_data_dict["Data Provider"] = "N/A"
            # append extracted data to total list
            extracted_data_list.append(extracted_data_dict)
        return extracted_data_list
    else:
        print("No results found.")


def create_dataframe_and_convert_to_html_table(data_dict, term):
    df = pd.DataFrame(data_dict)

    # table style
    penn_red = "#990000"
    penn_blue = "#011F5B"
    html = {
        df.style
            .set_caption(f"Search results for: {term}")
            .set_properties(**{'background-color': penn_blue,
                               'color': 'white',
                               'text-align': 'left'})
            .set_table_attributes(f'border="5" bordercolor={penn_red}')
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
        search_term = values["Term"]
        data = get_data_based_on_search_term(values["Term"])
        if data:
            relevant_data = extract_relevant_data(data)
            create_dataframe_and_convert_to_html_table(relevant_data, search_term)

            webbrowser.open(f"file://{os.path.realpath('search_results.html')}", new=2)
        else:
            print("Try another search term.")
