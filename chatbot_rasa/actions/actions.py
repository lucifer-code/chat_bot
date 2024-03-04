from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionSelectChoice(Action):
    def name(self) -> Text:
        return "action_select_choice"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_choice = tracker.latest_message['intent']['name']
        dispatcher.utter_message(template="utter_selected_choice", user_choice=user_choice)
        return []

class ActionSelectDateTime(Action):
    def name(self) -> Text:
        return "action_select_date_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        dispatcher.utter_message(template="utter_selected_date_time", date=date, time=time)
        return []

class ActionGetAvailableHeroes(Action):
    def name(self) -> Text:
        return "action_get_available_heroes"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Implement logic to get available heroes based on date and time
        available_heroes = ["Hero1", "Hero2", "Hero3"]
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        dispatcher.utter_message(template="utter_available_heroes", date=date, time=time, available_heroes=", ".join(available_heroes))
        return []
