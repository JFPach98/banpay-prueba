import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import random
import requests
import json
import numpy as np
import urllib
import urllib.request
import random
import io

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

class Airport:
    def __init__(self):
        pass
    
    def generate_df(self):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open('datasample_airports')
        sheet_instance = sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_records()
        records_df = pd.DataFrame.from_dict(records_data)
        records_df = records_df.drop(['id'], axis=1)
        country_list = records_df['Country'].unique()
        country_list = country_list.tolist()
        def quick_sort(list_name):
            empty = False
            if "" in list_name:
                list_name.remove("")
                empty = True
            else:
                pass
            if len(list_name) <= 1:
                return list_name
            else:
                start = 0  
                end = len(list_name) - 1
                mid_value = random.randint(start, end)
                mid_element = list_name[mid_value]
                list_name.remove(mid_element)
                upper_half = []
                lower_half = []
                for element in list_name:
                    if element < mid_element:
                        upper_half.append(element)
                    else:
                        lower_half.append(element)
  
            if empty == True:
                return quick_sort(upper_half) + [mid_element] + quick_sort(lower_half) + [""]
            else:
                return quick_sort(upper_half) + [mid_element] + quick_sort(lower_half)
        
        ordered_list = quick_sort(country_list)
        list_of_data = []
        for country in ordered_list:
            cols = records_df.columns 
            sub_df = records_df[records_df['Country'].isin([country])]
            list_of_data.append(sub_df)

        self.__data = pd.concat(list_of_data)
        return self.__data

    def get_data(self, data):
        self.__uniques = data['Country'].unique()
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

        self.__list_out = []
        for key,value in self.__nativename.items():
            self.__sub_df = self.__data.loc[(self.__data['Country'] == key)]
            self.__sub_df['Native Name'] = value
            self.__list_out.append(self.__sub_df)
        
        self.__output = pd.concat(self.__list_out)
        return self.__output

    def create_excel(self):
        self.__list_out = []
        for key,value in self.__nativename.items():
            self.__sub_df = self.__data.loc[(self.__data['Country'] == key)]
            self.__sub_df['Native Name'] = value
            self.__list_out.append(self.__sub_df)
    
        self.__output = pd.concat(self.__list_out)  
        self.__output.to_excel("output.xlsx", index = False)
    
    def generate_html(self, data):
        self.dat = data
        self.html = self.dat.to_html()
        with io.open("./templates/home.html", "w", encoding="utf-8") as f:
            f.write(self.html)
            f.close()
    
    def generate_html1(self, data):
        self.dat = data
        self.html = self.dat.to_html()
        with io.open("./templates/asia.html", "w", encoding="utf-8") as f:
            f.write(self.html)
            f.close()
    

def home(request):
    dat = Airport()
    df = dat.generate_df()
    dat.generate_html(df)
    return render(request, "home.html", {})

def asia(request):
    dat = Airport()
    df = dat.generate_df()
    df1 = dat.get_data(df)
    dat.generate_html1(df1)
    return render(request, "asia.html", {})