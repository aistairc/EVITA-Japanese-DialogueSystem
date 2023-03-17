# This code was developed for the Evita Virtual Coach project https://www.e-vita.coach/ at AIRC AIST
# Version 4.9; Date 2023-01-20;
# Programmer: Tatsuya Kudo, PI (AIRC): Kristiina Jokinen, unless otherwise indicated.
# We thank all the Evita project partners for discussions and contributions.
# License: Apache License 2.0;
# Contact: K. Jokinen <kristiina.jokinen@aist.go.jp>

from typing import Text, Callable, Dict, List, Any, Optional
from rasa_sdk import Tracker, utils, Action
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
import json
import urllib
from urllib.request import urlopen
from rasa_sdk.types import DomainDict
from rasa_sdk.events import (
    EventType, UserUtteranceReverted
)

weather_appid = '63630566634b8afa26f629dd64f2aa41'
class weather_user_request(Action):
    def name(self) -> Text:
        return "action_weather_user_request"
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        # intent = tracker.latest_message["intent"].get("name")
        # Case chitchat(greet)
        # if intent == 'greet':
        #     geographic_location = '仙台'
        #     weather_data = get_weather_info(str(geographic_location))
        #     temp_max_val = round(weather_data[1], 1)
        #     return [SlotSet('temp_max', temp_max_val)]
        # Case ask weather
        # else:
        requested_geographic_location = str(tracker.latest_message.get('text'))
        geographic_location = requested_geographic_location
        if '今日の' in requested_geographic_location and 'の天気' in requested_geographic_location:
            geographic_location_tmp = requested_geographic_location.split('今日の')[1]
            geographic_location = geographic_location_tmp.split('の天気')[0]
            # print(geographic_location)
        elif 'の天気' in requested_geographic_location:
            geographic_location = requested_geographic_location.split('の天気')[0]
        weather_data = get_weather_info(str(geographic_location))
        temp_max_val = round(weather_data[1], 1)
        temp_min_val = round(weather_data[2], 1)
        humidity_val = weather_data[3]
        wind_val = weather_data[4]
        rain_val = weather_data[5]
        snow_val = weather_data[6]
        weather_general = weather_data[7]
        # if not intent == 'greet':
        if rain_val == 0 and snow_val == 0:
            dispatcher.utter_message(response="utter_weather_details_norain_nosnow", geographic_location=geographic_location, temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, weather_description=weather_general)
        elif rain_val == 0 and snow_val != 0:
            dispatcher.utter_message(response="utter_weather_details_norain", geographic_location=geographic_location, temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, snow=snow_val, weather_description=weather_general)
        elif rain_val != 0 and snow_val == 0:
            dispatcher.utter_message(response="utter_weather_details_nosnow", geographic_location=geographic_location, temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, rain=rain_val, weather_description=weather_general)
        else:
            dispatcher.utter_message(response="utter_weather_details", geographic_location=geographic_location, temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, rain=rain_val, snow=snow_val, weather_description=weather_general)
        return [AllSlotsReset()]

class GetWeather(Action):
    def name(self) -> Text:
        return "get_weather"
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        geographic_location = '仙台'
        weather_data = get_weather_info(str(geographic_location))
        temp_max_val = round(weather_data[1], 1)
        # temp_min_val = round(weather_data[2], 1)
        # humidity_val = weather_data[3]
        # wind_val = weather_data[4]
        # rain_val = weather_data[5]
        # snow_val = weather_data[6]
        # weather_general = weather_data[7]
        return [SlotSet('temp_max', temp_max_val)]

class weather_tomorrow_user_request(Action):
    def name(self) -> Text:
        return "action_weather_tomorrow_user_request"
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        # requested_geographic_location = tracker.get_slot("geographic_location")
        requested_geographic_location = tracker.latest_message.get('text')
        if '明日の' in requested_geographic_location and 'の天気' in requested_geographic_location:
            geographic_location_tmp = requested_geographic_location.split('明日の')[1]
            geographic_location = geographic_location_tmp.split('の天気')[0]
        else:
            geographic_location = requested_geographic_location
        # print(geographic_location)
        weather_data = get_weather_forecast(str(geographic_location))

        temp_max_val = round(weather_data[1], 1)
        temp_min_val = round(weather_data[2], 1)
        humidity_val = weather_data[3]
        wind_val = weather_data[4]
        rain_val = weather_data[5]
        snow_val = weather_data[6]
        weather_general = weather_data[7]
        temp_val = round(weather_data[0], 1)

        if rain_val == 0 and snow_val == 0:
            dispatcher.utter_message(response="utter_weather_tomorrow_details_norain_nosnow", geographic_location=geographic_location, temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, weather_description=weather_general)
        elif rain_val == 0 and snow_val != 0:
            dispatcher.utter_message(response="utter_weather_tomorrow_details_norain", geographic_location=geographic_location, temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, snow=snow_val, weather_description=weather_general)
        elif rain_val != 0 and snow_val == 0:
            dispatcher.utter_message(response="utter_weather_tomorrow_details_nosnow", geographic_location=geographic_location, temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, rain=rain_val, weather_description=weather_general)
        else:
            dispatcher.utter_message(response="utter_weather_tomorrow_details", geographic_location=geographic_location, temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, rain=rain_val, snow=snow_val, weather_description=weather_general)
        # dispatcher.utter_message(response="utter_weather_tomorrow_detail", geographic_location=geographic_location, temperature_forecast=temp_val,
        #                          weather_description=weather_general)
        return [SlotSet("geographic_location", geographic_location)]

class weather_tomorrow_detail_user_request(Action):
    def name(self) -> Text:
        return "action_weather_tomorrow_detail_user_request"
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        # check weather
        # requested_geographic_location = tracker.get_slot("geographic_location")
        requested_geographic_location = tracker.latest_message.get('text')
        weather_data = get_weather_forecast_detail(str(requested_geographic_location))
        weather_general = weather_data[1]
        temp_max_val = round(weather_data[1], 1)
        temp_min_val = round(weather_data[2], 1)
        humidity_val = weather_data[3]
        wind_val = weather_data[4]
        rain_val = weather_data[5]
        snow_val = weather_data[6]
        weather_general = weather_data[7]
        
        if rain_val == 0 and snow_val == 0:
            dispatcher.utter_message(response="utter_weather_tomorrow_details_norain_nosnow", temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, weather_description=weather_general,
                                    geographic_location=requested_geographic_location)
        elif rain_val == 0 and snow_val != 0:
            dispatcher.utter_message(response="utter_weather_tomorrow_details_norain", temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, snow=snow_val, weather_description=weather_general,
                                    geographic_location=requested_geographic_location)
        elif rain_val != 0 and snow_val == 0:
            dispatcher.utter_message(response="utter_weather_tomorrow_details_nosnow", temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, rain=rain_val, weather_description=weather_general,
                                    geographic_location=requested_geographic_location)
        else:
            dispatcher.utter_message(response="utter_weather_tomorrow_details", temp_max=temp_max_val, temp_min=temp_min_val,
                                    humidity=humidity_val, wind=wind_val, rain=rain_val, snow=snow_val, weather_description=weather_general,
                                    geographic_location=requested_geographic_location)
        return []

def get_weather_info(geographic_location):
    # Weather api to predict weather
    if '県' in geographic_location:
        geographic_location = geographic_location.split('県')[1]
    if '大阪府' in geographic_location:
        geographic_location = geographic_location.split('大阪府')[1]
    if '京都府' in geographic_location:
        geographic_location = geographic_location.split('京都府')[1]
    if '東京都' in geographic_location:
        geographic_location = geographic_location.split('東京都')[1]
    if '北海道' in geographic_location:
        geographic_location = geographic_location.split('北海道')[1]

    BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
    url = BASE_URL + 'q=' + urllib.parse.quote(geographic_location) + '&appid=' + weather_appid + '&lang=ja&units=metric'
    try:
        response = urlopen(url)
    except urllib.error.HTTPError as e:
        geographic_location = geographic_location + '市'
        url = BASE_URL + 'q=' + urllib.parse.quote(geographic_location) + '&appid=' + weather_appid + '&lang=ja&units=metric'
        try:
            response = urlopen(url)
        except:
            geographic_location = geographic_location.split('市')[0] + '村'
            url = BASE_URL + 'q=' + urllib.parse.quote(geographic_location) + '&appid=' + weather_appid + '&lang=ja&units=metric'
            try:
                response = urlopen(url)
            except:
                geographic_location = geographic_location.split('村')[0] + '町'
                url = BASE_URL + 'q=' + urllib.parse.quote(geographic_location) + '&appid=' + weather_appid + '&lang=ja&units=metric'
                try:
                    response = urlopen(url)
                except:
                    geographic_location = ''
    print('geographic_location: ' + geographic_location)
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    # print(json_obj)
    rain = 0
    snow = 0
    temp = json_obj['main']['temp']
    temp_max = json_obj['main']['temp_max']
    temp_min = json_obj['main']['temp_min']
    humidity = json_obj['main']['humidity']
    wind = json_obj['wind']['speed']
    if 'rain' in json_obj:
        rain = json_obj['rain']['1h']
    if 'snow' in json_obj:
        snow = json_obj['snow']['1h']
    weather = json_obj['weather'][0]['description']

    return temp, temp_max, temp_min, humidity, wind, rain, snow, weather

def get_weather_forecast(geographic_location):
    import urllib
    BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast?'
    if '明日の' in geographic_location:
        geographic_location = geographic_location.split('明日の')[1]
    if 'の天気' in geographic_location:
        geographic_location = geographic_location.split('の天気')[0]
    if '県' in geographic_location:
        geographic_location = geographic_location.split('県')[1]
    if '大阪府' in geographic_location:
        geographic_location = geographic_location.split('大阪府')[1]
    if '京都府' in geographic_location:
        geographic_location = geographic_location.split('京都府')[1]
    if '東京都' in geographic_location:
        geographic_location = geographic_location.split('東京都')[1]
    if '北海道' in geographic_location:
        geographic_location = geographic_location.split('北海道')[1]
    url = BASE_URL + 'q=' + urllib.parse.quote(geographic_location) + '&appid=' + weather_appid + '&lang=ja&units=metric'
    try:
        response = urlopen(url)
    except urllib.error.HTTPError as e:
        geographic_location = geographic_location + '市'
        url = BASE_URL + 'q=' + urllib.parse.quote(geographic_location) + '&appid=' + weather_appid + '&lang=ja&units=metric'
        try:
            response = urlopen(url)
        except:
            geographic_location = geographic_location.split('市')[0] + '村'
            url = BASE_URL + 'q=' + urllib.parse.quote(geographic_location) + '&appid=' + weather_appid + '&lang=ja&units=metric'
            try:
                response = urlopen(url)
            except:
                geographic_location = geographic_location.split('村')[0] + '町'
                url = BASE_URL + 'q=' + urllib.parse.quote(geographic_location) + '&appid=' + weather_appid + '&lang=ja&units=metric'
                try:
                    response = urlopen(url)
                except:
                    geographic_location = ''
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    rain = 0
    snow = 0
    temp = json_obj['list'][0]['main']['temp']
    temp_max = json_obj['list'][0]['main']['temp_max']
    temp_min = json_obj['list'][0]['main']['temp_min']
    humidity = json_obj['list'][0]['main']['humidity']
    wind = json_obj['list'][0]['wind']['speed']
    if 'rain' in json_obj:
        rain = json_obj['list'][0]['rain']['1h']
    if 'snow' in json_obj:
        snow = json_obj['list'][0]['snow']['1h']
    weather = json_obj['list'][0]['weather'][0]['description']

    return temp, temp_max, temp_min, humidity, wind, rain, snow, weather

def get_weather_forecast_detail(geographic_location):
    import urllib
    BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast?'
    url = BASE_URL + 'q=' + urllib.parse.quote(geographic_location) + '&cnt=1&appid=' + weather_appid + '&lang=ja&units=metric'
    try:
        response = urlopen(url)
    except urllib.error.HTTPError as e:
        geographic_location = geographic_location + '市'
        url = BASE_URL + 'q=' + urllib.parse.quote(geographic_location) + '&cnt=1&appid=' + weather_appid + '&lang=ja&units=metric'
        response = urlopen(url)
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    rain = 0
    snow = 0
    temp = json_obj['list'][0]['main']['temp']
    temp_max = json_obj['list'][0]['main']['temp_max']
    temp_min = json_obj['list'][0]['main']['temp_min']
    humidity = json_obj['list'][0]['main']['humidity']
    wind = json_obj['list'][0]['wind']['speed']
    if 'rain' in json_obj:
        rain = json_obj['list'][0]['rain']['1h']
    if 'snow' in json_obj:
        snow = json_obj['list'][0]['snow']['1h']
    weather = json_obj['list'][0]['weather'][0]['description']

    return temp, temp_max, temp_min, humidity, wind, rain, snow, weather

class CheckWeatherTemp(Action):
    def name(self) -> Text:
        return "action_check_weather_temp"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # check weather
        requested_geographic_location = tracker.get_slot("geographic_location")
        # print(requested_geographic_location)
        weather_data = get_weather_info(str(requested_geographic_location))
        weather_general = weather_data[7]
        temp_val = weather_data[0]

        # set should_go_out flag
        intent = tracker.latest_message["intent"]["name"]
        if intent=='deny' or intent=='exercise_not_done' or intent=='not_done' or intent=='should_i_exercise':
            if "晴" in weather_general:
                dispatcher.utter_message(response='utter_suggest_exercise_outside')
            else:
                dispatcher.utter_message(response='utter_suggest_exercise_indoor')
        else:
            temp_int = int(temp_val)
            if temp_int >= 26:
                dispatcher.utter_message(response='utter_advise_clothing_1')
            elif 21 <= temp_int <= 25:
                dispatcher.utter_message(response='utter_advise_clothing_2')
            elif 16 <= temp_int <= 20:
                dispatcher.utter_message(response='utter_advise_clothing_3')
            elif 12 <= temp_int <= 15:
                dispatcher.utter_message(response='utter_advise_clothing_4')
            elif 7 <= temp_int <= 11:
                dispatcher.utter_message(response='utter_advise_clothing_5', temp_int=temp_int)
            elif 6 >= temp_int:
                dispatcher.utter_message(response='utter_advise_clothing_6', temp_int=temp_int)
