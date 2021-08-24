import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import random
import requests
import json
import numpy as np
import urllib
import urllib.request

class Airport:
    def __init__(self, data, country, code1, code2, airport_name):
        self.__data = data
        self.__airport = airport_name
    def get_data(self):
        self.__country_list = self.__data['Country'].unique()
        self.__uniques = self.__data['Country'].unique()
        self.__uniques = self.__uniques.tolist()
        self.__nativename = {}
        for country in self.__uniques:
            if country == "":
                pass
            elif country == "North Korea":
                r = requests.get("https://restcountries.eu/rest/v2/name/People's Republic of Korea")
                json_data = json.loads(r.text)
                self.__nativename[country] = json_data[0]['nativeName']
            elif country == "South Korea":
                r = requests.get("https://restcountries.eu/rest/v2/name/Republic of Korea")
                json_data = json.loads(r.text)
                self.__nativename[country] = json_data[0]['nativeName']
            else:
                r = requests.get("https://restcountries.eu/rest/v2/name/" + country)
                json_data = json.loads(r.text)
                if 'message' in json_data:
                    pass
                else:
                    self.__region = json_data[0]['region']
                    if self.__region == 'Asia':
                        self.__nativename[country] = json_data[0]['nativeName']
                    else:
                        pass

        return self.__nativename

    def create_excel(self):
        self.__list_out = []
        for key,value in self.__nativename.items():
            self.__sub_df = self.__data.loc[(self.__data['Country'] == key)]
            self.__sub_df['Native Name'] = value
            self.__list_out.append(self.__sub_df)
    
        self.__output = pd.concat(self.__list_out)  
        self.__output.to_excel("output.xlsx", index = False)