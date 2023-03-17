# This code was developed for the Evita Virtual Coach project https://www.e-vita.coach/ at AIRC AIST
# Version 4.9; Date 2023-01-20;
# Programmer: Tatsuya Kudo, PI (AIRC): Kristiina Jokinen, unless otherwise indicated.
# We thank all the Evita project partners for discussions and contributions.
# License: Apache License 2.0;
# Contact: K. Jokinen <kristiina.jokinen@aist.go.jp>

import re
from typing import Text, Callable, Dict, List, Any, Optional
from rasa_sdk import Tracker, utils, Action
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import (
    EventType, SlotSet, UserUtteranceReverted
)
from bs4 import BeautifulSoup
import requests

class yahooNews(Action):
    def name(self) -> Text:
        return "action_yahoo_news"
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        global count, before_intent, top_news, count_deny
        # retrieve top news
        class yahooNews:
            def getTopNews(self):
                url = "https://news.yahoo.co.jp/" # url of top news
                headlines = []
                html = requests.get(url) # html of the url
                soup = BeautifulSoup(html.text, "html.parser")
                data_list = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
                
                for headline in data_list:
                    # print(headline.text)
                    headlines.append(headline.text)

                return(headlines)

            # search news
            def searchNews(self, search_word):
                url = "https://news.yahoo.co.jp/search?p=" + str(search_word) + "&ei=utf-8"
                headlines = []
                html = requests.get(url)
                soup = BeautifulSoup(html.content, "html.parser")
                for headline in soup.find_all(class_ = "newsFeed_item_title"):
                    headlines.append(headline.text)

                return(headlines)

        yahooNews = yahooNews()
        intent = tracker.latest_message["intent"].get("name")

        if intent == 'ask_news':
            before_intent = intent
            top_news = yahooNews.getTopNews()
            dispatcher.utter_message('8つのニュースをお届けします。')
            dispatcher.utter_message('1、' + top_news[0])
            dispatcher.utter_message('次のニュースを読み上げましょうか？')
            count = 1
            count_deny = 0            
            return [SlotSet('before_intent', before_intent), SlotSet('top_news', top_news)]

        elif intent == 'ask_news_with_word':
            count_deny = 0 # Add 20230315 by Kudo
            before_intent = intent
            search_word_news = tracker.latest_message.get('text')
            search_word = search_word_news.split('のニュース')[0]

            result_with_search_word = yahooNews.searchNews(search_word)
            result_num = len(result_with_search_word)
            # dispatcher.utter_message(search_word)
            if result_num:
                if result_num > 8:
                    result_num = 8
                dispatcher.utter_message(search_word + "に関するニュースを8つお届けします。")
                dispatcher.utter_message('1、' + result_with_search_word[0])
                dispatcher.utter_message('次のニュースを読み上げましょうか？')
                count = 1

            # else:
            #     dispatcher.utter_message(search_word + 'に関するニュースはありませんでした。')
            return [SlotSet('before_intent', before_intent), SlotSet('search_word', search_word),
                    SlotSet('result_with_search_word', result_with_search_word)]

        elif intent=='affirm' or intent=='next':
            # if before_intent:
            if before_intent == 'ask_news':
                top_news = tracker.get_slot('top_news')
                if top_news:
                    dispatcher.utter_message(str(count+1) + '、' + top_news[count])
                    if count <= 6:
                        dispatcher.utter_message('次のニュースを読み上げましょうか？')
                        count += 1
                    else:
                        dispatcher.utter_message('以上、トップニュースをお伝えしました。')
                        count = 0
                        before_intent = ''
                        # return [AllSlotsReset()]
                        return [SlotSet('before_intent', None), SlotSet('search_word', None), SlotSet('top_news', None)]
                else:
                    dispatcher.utter_message(response='utter_tell_me_request')

            elif before_intent == 'ask_news_with_word':
                # dispatcher.utter_message('ask_news_with_word')
                result_with_search_word = tracker.get_slot('result_with_search_word')
                if result_with_search_word:
                    # print(result_with_search_word)
                    if len(result_with_search_word) >= count:
                        dispatcher.utter_message(str(count+1) + '、' + result_with_search_word[count])
                        if count <= 6:
                            dispatcher.utter_message('次のニュースを読み上げましょうか？')
                            count += 1
                        else:
                            search_word = tracker.get_slot('search_word')
                            dispatcher.utter_message('以上、' + search_word + 'に関するニュースをお伝えしました。')
                            count = 0
                            before_intent = ''
                            # return [AllSlotsReset()]
                            return [SlotSet('before_intent', None), SlotSet('search_word', None), SlotSet('result_with_search_word', None)]
                    else:
                        dispatcher.utter_message('これ以上ニュースはありませんでした。')
                        return [AllSlotsReset()]
                else:
                    dispatcher.utter_message(response='utter_tell_me_request')

        else:
            if count_deny == 0:
                dispatcher.utter_message(response='utter_thanks')
                count_deny += 1
            else:
                dispatcher.utter_message(response='utter_have_a_good_day')
                # print(before_intent)
            return [SlotSet('before_intent', None), SlotSet('search_word', None), SlotSet('result_with_search_word', None), SlotSet('top_news', None)]

        # from newsapi import NewsApiClient
        # # クライアントを初期化
        # api_key = '709ad4c2b2df40639f15a488d5cf113d'
        # newsapi = NewsApiClient(api_key=api_key)
        # # categoryをbusiness、国をjpに指定してニュースを取得
        # # headlines = newsapi.get_top_headlines(category='business', country='jp')
        # headlines = newsapi.get_top_headlines(sources='techcrunch', country='jp')
        # print(headlines)

        # if( headlines['totalResults'] > 0 ):
        #     print(headlines['articles'][0])
        # else:
        #     print("条件に合致したトップニュースはありません。")