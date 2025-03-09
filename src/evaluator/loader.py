import os
from echo.message import Message

import logging
logger = logging.getLogger(__name__)

class Loader:
    """
    Load input data
    """
    def __init__(self, input_folder=None):
        """ """
        self.input_folder = input_folder

    def load_messages(self, files=None):
        # Return a list of messages loaded from csv files with role, content columns
        messages = []
        for file in files:
            lines = [] # parse csv file from self.input_folder/grader/{file} into list of dict using column names
            messages.extend(lines)
        return messages
    
    def load_formatted_messages(self, folder="prompts", files=[]):
        # Return a list of messages loaded from the csv files with role, from, to, text columns
        messages = []
        for file in files:
            lines = [] # parse csv file from self.input_folder/{folder}/{file} into list of dicts with column names
            for line in lines:
                messages.append(Message(
                    role=line["role"], 
                    user=line["from"], 
                    dialog=line["to"], 
                    text=line["text"]
                ).as_llm_message())
        return messages
    
    def load_formatted_conversations(self, folder="conversations", files=None):
        conversations = {}
        for file in files:
            conversations[file] = self.load_formatted_messages(folder=folder, files=[file])
        return conversations
    
