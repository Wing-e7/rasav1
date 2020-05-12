from typing import Text, List, Dict, Any
import datetime
from rasa_sdk.events import ReminderScheduled, ReminderCancelled

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa.core.events import SlotSet
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import pymysql
import mysql.connector
import pandas as pd
import json 



class ActionCustomSentiment(Action):

    def name(self) -> Text:
        return "action_customsentiment"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn=pymysql.connect(host='localhost',port=int(3306),user='root',passwd='IPmanValley',db='rasa')
        df=pd.read_sql_query("SELECT * FROM yip.events ",conn, index_col = 'id')
        l = len(df[df.intent_name == 'pitch'].index)
        m = ''
        for i in range(0,l):
            text = df[df['intent_name']== 'pitch']['data'].iloc[i]
            res = json.loads(text) 
            k = res['text']
            m = m +' '+ k

        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(m)

        if ss['neg'] >= 0.1:
            #tracker.trigger_followup_action(action_utter_getout)
            dispatcher.utter_message("getout")
        elif ss['pos'] >= 0.4:
            #tracker.trigger_followup_action(action_utter_ilike)
            dispatcher.utter_message("ilike")
        else:
            #tracker.trigger_followup_action(action_utter_allfine)
            dispatcher.utter_message("followup")
            
            
        return []
