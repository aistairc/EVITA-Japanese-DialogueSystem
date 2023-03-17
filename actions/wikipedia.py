# This code was developed for the Evita Virtual Coach project https://www.e-vita.coach/ at AIRC AIST
# Version 4.9; Date 2023-01-20;
# Programmer: Tatsuya Kudo, PI (AIRC): Kristiina Jokinen, unless otherwise indicated.
# We thank all the Evita project partners for discussions and contributions.
# License: Apache License 2.0;
# Contact: K. Jokinen <kristiina.jokinen@aist.go.jp>

import re
from typing import Text, Callable, Dict, List, Any, Optional
from unicodedata import name
from rasa_sdk import Tracker, utils, Action
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted
from rasa_sdk.executor import CollectingDispatcher
from duckduckgo_search import ddg
import wikipediaapi
from rasa_sdk.types import DomainDict
from rasa_sdk.events import (
    EventType, UserUtteranceReverted
)
frame_response=1
class ActionQueryWikipedia(Action):
    def name(self) -> Text:
        return "action_query_wikipedia"
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        response_segment_number = 0
        wiki_test = wikipediaapi.Wikipedia("ja")
        search_word = tracker.latest_message.get('text')
        if '調べて' in search_word:
            search_word_wiki = re.findall("ウィキペディアで(.+?)を調べて", search_word)
            if not search_word_wiki:
                search_word_wiki = re.findall("ウィキペディアで(.+?)について調べて", search_word)
            # print(type(search_word_wiki))
            # if isinstance(search_word_wiki, list):
            #     search_word_wiki = search_word_wiki[0]
        elif '教えて' in search_word:
            search_word_wiki = re.findall("ウィキペディアで(.+?)を教えて", search_word)
            if not search_word_wiki:
                search_word_wiki = re.findall("ウィキペディアで(.+?)について教えて", search_word)
            # if isinstance(search_word_wiki, list):
            #     search_word_wiki = search_word_wiki[0]
        else:
            search_word_wiki = search_word.replace('ウィキペディア、', '')
        if isinstance(search_word_wiki, list):
            search_word_wiki = search_word_wiki[0]
        response_search_engine = ''
        if search_word_wiki:
            results = wiki_test.page(search_word_wiki)
            response_search_engine = str(results.summary)

        if response_search_engine:
            list_tokens= response_search_engine.split('。')
            bot_answer= list_tokens[0]
            # print(list_tokens)
            if len(list_tokens) == 1:
                dispatcher.utter_message(bot_answer + '。')
            else:
                dispatcher.utter_message(bot_answer + '。' + 'もっと知りたいですか？')
        else:
            dispatcher.utter_message('すみません、ウィキペディアに'+search_word_wiki+'の項目はありませんでした。別の単語を試してみてください。')

        return [SlotSet("response_search_engine", response_search_engine),SlotSet("response_segment_number", response_segment_number+frame_response)]

class ActionQueryDuckduckgo(Action):
    def name(self) -> Text:
        return "action_query_duckduckgo"
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        # client = Client()
        user_input = tracker.latest_message.get('text')
        search_word_duck = re.findall("ダックゴーで(.+?)を調べて", user_input)
        if not search_word_duck:
            search_word_duck = re.findall("ダックゴーで(.+?)について調べて", user_input)
            if not search_word_duck:
                # Change by Goran
                # search_word_duck = re.findall("ダックゴー、(.+?)", user_input)
                search_word_duck = re.findall("ダックゴー、(.+)", user_input)
        if isinstance(search_word_duck, list):
            search_word_duck = search_word_duck[0]
        # print(search_word_duck)
        results = ddg(search_word_duck, region='wt-wt', safesearch='Moderate', time='y', max_results=25)
        bot_return = results[0]['body']
        # results = ddg_answers(search_word_duck)
        # print(results)
        # if search_word_duck:
        #     results = client.search(search_word_duck)
        #     bot_return = results[0].description
        #     print(search_word_duck, results, bot_return)
        dispatcher.utter_message(bot_return)
        return [AllSlotsReset()]

class response_know_more(Action):
    def name(self) -> Text:
        return "action_response_know_more"
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        response_search_engine = str(tracker.get_slot("response_search_engine"))
        response_segment_number= int(tracker.get_slot("response_segment_number"))
        list_tokens = response_search_engine.split('。')
        if (response_segment_number + frame_response) >= len(list_tokens):
            bot_answer = "すみません、これ以上の情報はありませんでした。"
        else:
            bot_answer = "。".join(list_tokens[1:])

        dispatcher.utter_message(bot_answer)
        return [AllSlotsReset()]
