# This code was developed for the Evita Virtual Coach project https://www.e-vita.coach/ at AIRC AIST
# Version 4.9; Date 2023-01-20;
# Programmer: Tatsuya Kudo, PI (AIRC): Kristiina Jokinen, unless otherwise indicated.
# We thank all the Evita project partners for discussions and contributions.
# License: Apache License 2.0;
# Contact: K. Jokinen <kristiina.jokinen@aist.go.jp>

from typing import Text, Callable, Dict, List, Any, Optional
from unicodedata import name
from rasa_sdk import Tracker, utils, Action
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    EventType, SlotSet, UserUtteranceReverted
)
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase

class ACtionQueryDiseaseDatabase(ActionQueryKnowledgeBase):
    def name(self) -> Text:
        return "action_query_disease_database"
    def __init__(self):
        knowledge_base = InMemoryKnowledgeBase("disease.json")
        super().__init__(knowledge_base)

    def utter_attribute_value(
        self,
        dispatcher: CollectingDispatcher,
        object_name: Text,
        attribute_name: Text,
        attribute_value: Text,
    ):
        if attribute_value:
            if attribute_name:
                text=f"{attribute_value}"
            dispatcher.utter_message(text=text)
            # dispatcher.utter_message(attribute_value)
            return[SlotSet('object_name', object_name)]

    async def utter_objects(self, dispatcher, object_type, objects):
        if objects:
            # print(objects)
            if len(objects) == 1:
                text = objects[0]['定義']
                dispatcher.utter_message(text=text)
            else:
                dispatcher.utter_message(
                    text=f"私が知っている" + object_type + "は次の" + str(len(objects)) + "個です"
                )

                repr_function = await utils.call_potential_coroutine(
                    self.knowledge_base.get_representation_function_of_object(object_type)
                )

                for i, obj in enumerate(objects, 1):
                    dispatcher.utter_message(text=f"{i}: {repr_function(obj)}")
        else:
            dispatcher.utter_message(
                text=f"'{object_type}'は見つけれらませんでした。"
            )

# class ACtionQueryFallDatabase(ActionQueryKnowledgeBase):
#     def name(self) -> Text:
#         return "action_query_fall_database"
#     def __init__(self):
#         knowledge_base = InMemoryKnowledgeBase("fall.json")
#         super().__init__(knowledge_base)

#     def utter_attribute_value(
#         self,
#         dispatcher: CollectingDispatcher,
#         object_name: Text,
#         attribute_name: Text,
#         attribute_value: Text,
#     ):
#         dispatcher.utter_message(object_name)
#         if attribute_value:
#             dispatcher.utter_message('aaaaaaaa')
#             if attribute_name:
#                 text=f"{attribute_value}"
#             dispatcher.utter_message(text=text)
#             return[SlotSet('object_name', object_name)]
#         else:
#             dispatcher.utter_message('ssssss')

#     async def utter_objects(self, dispatcher, object_type, objects):
#         if objects:
#             if len(objects) == 1:
#                 text = (objects[0]['定義'])
#                 dispatcher.utter_message(text=text)
#                 return[SlotSet('object_name', object_type)]
#         else:
#             dispatcher.utter_message(
#                 text=f"'{object_type}'に関する情報は見つけれらませんでした。"
#             )
