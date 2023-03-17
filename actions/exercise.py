# This code was developed for the Evita Virtual Coach project https://www.e-vita.coach/ at AIRC AIST
# Version 4.9; Date 2023-01-20;
# Programmer: Tatsuya Kudo, PI (AIRC): Kristiina Jokinen, unless otherwise indicated.
# We thank all the Evita project partners for discussions and contributions.
# License: Apache License 2.0;
# Contact: K. Jokinen <kristiina.jokinen@aist.go.jp>

from typing import Text, Callable, Dict, List, Any, Optional
# from unicodedata import name
from rasa_sdk import Tracker, utils, Action
# from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted
from rasa_sdk.executor import CollectingDispatcher
# from datetime import datetime
# import datetime as dt
# from kanjize import int2kanji, kanji2number, Number
# from rasa_sdk.events import (
#     EventType, SlotSet, UserUtteranceReverted
# )

# class prevention_fall(Action):
#     def name(self) -> Text:
#         return "action_prevention_fall"
#     def run(self, dispatcher, tracker, domain):
#         intent = tracker.latest_message["intent"].get("name")
#         if intent == 'prevention_fall':
#             dispatcher.utter_message(response='utter_recommend_prevention_fall')
#             advice_prevention_of_fall = 1
#             advice_meal = 0
#             advice_footwear = 0

#         if intent == 'affirm':
#             advice_prevention_of_fall = tracker.get_slot('advice_prevention_of_fall')
#             advice_meal = tracker.get_slot('advice_meal')
#             advice_footwear = tracker.get_slot('advice_footwear')
#             if advice_prevention_of_fall == 1:
#                 dispatcher.utter_message(response='utter_advice_prevention_of_fall')
#                 advice_prevention_of_fall = 0
#                 advice_meal = 1
#                 advice_footwear = 0
#             elif advice_meal == 1:
#                 dispatcher.utter_message(response='utter_advice_meal')
#                 advice_meal = 0
#                 advice_footwear = 1
#             elif advice_footwear == 1:
#                 dispatcher.utter_message(response='utter_advice_footwear')
#                 advice_footwear = 0

#                 # print(advice_prevention_of_fall, advice_meal, advice_footwear)

#         return [SlotSet('advice_prevention_of_fall', advice_prevention_of_fall),
#                 SlotSet('advice_meal', advice_meal),
#                 SlotSet('advice_footwear', advice_footwear)]

class CompareStepsWithLastWeek(Action):
    def name(self) -> Text:
        return 'compare_steps_with_last_week'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        steps_last_week = tracker.get_slot('average_steps_last_week')
        steps_today = tracker.get_slot('steps_today')
        if steps_today < steps_last_week:
            dispatcher.utter_message(response='utter_steps_less_than_last_week')
        else:
            dispatcher.utter_message(response='utter_steps_more_than_last_week')

# minamiguchi for takano-sensei's senarios
# class CalcStrideLength(Action):
#     def name(self) -> Text:
#         return "action_calc_stride_length"
    
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         # pending calc block; to replace the previous block once relevant data become available
#         foot_steps = tracker.get_slot("pedometer_user")
#         distance_walked = tracker.get_slot("distance_walked") # (km)
#         if foot_steps:
#             try:
#                 foot_steps = int(foot_steps)
#             except:
#                 foot_steps = kanji2number(foot_steps)
#         if distance_walked:
#             try:
#                 distance_walked = float(distance_walked)
#             except:
#                 distance_walked = kanji2number(distance_walked)

#         stride_length = distance_walked / foot_steps
#         if stride_length < 0.0006: # threshold TBD
#             short_stride = True
#         else:
#             short_stride = False
        
#         return [SlotSet(key="short_stride", value=short_stride)]
