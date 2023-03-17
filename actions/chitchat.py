# This code was developed for the Evita Virtual Coach project https://www.e-vita.coach/ at AIRC AIST
# Version 4.9; Date 2023-01-20;
# Programmer: Tatsuya Kudo, PI (AIRC): Kristiina Jokinen, unless otherwise indicated.
# We thank all the Evita project partners for discussions and contributions.
# License: Apache License 2.0;
# Contact: K. Jokinen <kristiina.jokinen@aist.go.jp>

import re
from typing import Text, Callable, Dict, List, Any, Optional
# from unicodedata import name
from rasa_sdk import Tracker, utils, Action
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from datetime import datetime
# import datetime as dt
# from random import choices
import sqlite3
import pytz
import json
from rasa_sdk.events import (
    EventType, SlotSet, UserUtteranceReverted
)

USER_INTENT_OUT_OF_SCOPE = "out_of_scope"
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:

        # Fallback caused by TwoStageFallbackPolicy
        last_intent = tracker.latest_message["intent"]["name"]
        # print(last_intent)
        if last_intent in ["nlu_fallback", USER_INTENT_OUT_OF_SCOPE]:
            return [SlotSet("feedback_value", "negative")]

        # Fallback caused by Core
        else:
            dispatcher.utter_message(template="utter_default")
            return [UserUtteranceReverted()]

class clear_slot(Action):
    def name(self) -> Text:
        return "action_clear_slot"
    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        if intent=='reset_slot':
            dispatcher.utter_message('リセットしました！')
        return [AllSlotsReset()]

class check_slot(Action):
    def name(self) -> Text:
        return "action_check_slot"
    def run(self, dispatcher, tracker, domain):
        print(tracker.current_slot_values())
        return []

class ActionGreeting1(Action):
    def name(self):
        return "action_greeting1"
    def run(self, dispatcher, tracker, domain):
        # Change way to get JST (Goran's advice)
        JST = pytz.timezone('Asia/Tokyo')
        now = datetime.now(JST).hour
        # now = int(dt.datetime.now().strftime('%H'))
        # now = now + 9
        if 4 <= now < 11:
            greeting = 'おはようございます。'
        elif 11 <= now < 17:
            greeting = 'こんにちは。'
        else:
            greeting = 'こんばんは。'

        conn = sqlite3.connect('rasa.db')
        cur = conn.cursor()
        cur.execute("SELECT data FROM events WHERE action_name = 'user_name'")
        results = cur.fetchall()
        if results:
            # print(results)
            row = results[len(results)-1][0]
            row = json.loads(row)
            user_name = row['value']
            # user_name = tracker.get_slot('user_name')
            # print(user_name)

            if user_name:
                ask_name = ''
                max_temperature = int(tracker.get_slot('temp_max'))
                if max_temperature >= 30:
                    msg2 = '今日は暑いですね。'
                elif max_temperature <= 10:
                    msg2 = '今日は寒いですね。'
                elif 10 <= max_temperature < 20:
                    msg2 = '今日は少し寒いですね。'
                elif 20 <= max_temperature < 25:
                    msg2 = '今日は過ごしやすいですね。'
                elif 25 <= max_temperature < 30:
                    msg2 = '今日は少し暑いですね。'

                msg3 = '何か予定はありますか？'

                msg = greeting + user_name + 'さん。' + msg2 + msg3
                
            else:
                ask_name = 'あなたの名前を教えてください。'
                msg = greeting + ask_name

            dispatcher.utter_message(msg)
        else:
            ask_name = 'あなたの名前を教えてください。'
            msg = greeting + ask_name
            dispatcher.utter_message(msg)

class ActionGreeting2(Action): 
    def name(self):
        return "action_greeting2"
    def run(self, dispatcher, tracker, domain):
        max_temperature = int(tracker.get_slot('temp_max'))
        if max_temperature >= 30:
            temp_level = '暑い'
        elif max_temperature <= 10:
            temp_level = '寒い'
        elif 10 <= max_temperature < 20:
            temp_level = '少し寒い'
        elif 20 <= max_temperature < 25:
            temp_level = '過ごしやすい'
        elif 25 <= max_temperature < 30:
            temp_level = '少し暑い'
        
        dispatcher.utter_message(response='utter_tell_about_temp', temp_level=temp_level, max_temperature=max_temperature)

class GetUserName(Action): 
    def name(self):
        return "get_user_name"
    def run(self, dispatcher, tracker, domain):
        user_name = tracker.latest_message['text']
        if 'です' in user_name:
            user_name = user_name.split('です')[0]
        elif 'と申します' in user_name:
            user_name = user_name.split('と申します')[0]
        elif 'といいます' in user_name:
            user_name = user_name.split('といいます')[0]
        elif 'っていいます' in user_name:
            user_name = user_name.split('っていいます')[0]
        elif 'だよ' in user_name:
            user_name = user_name.split('だよ')[0]

        dispatcher.utter_message(response='utter_learnt_user_name', user_name=user_name)
        return [SlotSet('user_name', user_name)]

# class ActionOmikuji(Action):
#     def name(self) -> Text:
#         return "action_omikuji"
#     def run(self, dispatcher, tracker, domain):
#         kuji = ['大吉', '中吉', '小吉', '末吉', '凶', '大凶']
#         unsei = choices(kuji, weights=[1, 5, 10, 10, 5, 1])[0]
#         if unsei=='大吉':
#             first_msg = 'おめでとうございます！'
#         elif unsei == '大凶':
#             first_msg = '残念！'
#         else:
#             first_msg = ''
#         dispatcher.utter_message(first_msg + '今日のあなたの運勢は' + unsei + 'です')

class RepeatUserInput(Action):
    def name(self) -> Text:
        return "repeat_back"
    def run(self, dispatcher, tracker, domain):
        free_talk = tracker.latest_message.get('text')
        if '行くよ' in free_talk:
            free_talk = re.findall('(.+?)行くよ', free_talk)[0] + '行く'
        elif '行きます' in free_talk:
            free_talk = re.findall('(.+?)行きます', free_talk)[0] + '行く'
        elif 'するよ' in free_talk:
            free_talk = re.findall('(.+?)するよ', free_talk)[0] + 'する'
        elif 'します' in free_talk:
            free_talk = re.findall('(.+?)します', free_talk)[0] + 'する'
        elif 'やります' in free_talk:
            free_talk = re.findall('(.+?)やります', free_talk)[0] + 'やる'
        elif 'やろうかな' in free_talk:
            free_talk = re.findall('(.+?)やろうかな', free_talk)[0] + 'やる'
        elif 'してます' in free_talk:
            free_talk = re.findall('(.+?)してます', free_talk)[0] + 'する'
        elif 'してきます' in free_talk:
            free_talk = re.findall('(.+?)してきます', free_talk)[0] + 'してくる'
        elif 'ってきます' in free_talk:
            free_talk = re.findall('(.+?)ってきます', free_talk)[0] + 'ってくる'
        elif '買おうかな' in free_talk:
            free_talk = re.findall('(.+?)買おうかな', free_talk)[0] + '買う'
        elif '見ます' in free_talk:
            free_talk = re.findall('(.+?)見ます', free_talk)[0] + '見る'
        else:
            free_talk = free_talk + 'する'

        dispatcher.utter_message('いいですね！' + free_talk + 'のですね！')
        return []
