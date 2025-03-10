import os
import csv
from echo.message import Message

import logging
logger = logging.getLogger(__name__)

class Loader:
    """
    Load methods that read csv files and return a list of message dictionaries with role and content properties. 
    """
    def __init__(self, input_folder=None):
        """Initialize Loader
        
        Args: input_folder were data files will be located
        """
        self.input_folder = input_folder

    def load_messages(self, files=None):
        """"Get messages from a list of simple {role, content} csv files from the input_folder/grader folder"""
        messages = []
        for file in files:
            file_path = os.path.join(self.input_folder, "grader", file)
            logger.debug(f"Loading Messages from {file_path}")
            with open(file_path, mode="r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f, quotechar='"', skipinitialspace=True)
                messages.extend(reader)                
        return messages
    
    def load_formatted_messages(self, folder="prompts", files=None):
        """"Construct messages from a list of {role, from, to, text} csv files found in the specified folder"""
        messages = []
        for file in files:
            file_path = os.path.join(self.input_folder, folder, file)
            logger.debug(f"Loading Formatted Messages from {file_path}")
            with open(file_path, mode="r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f, quotechar='"', skipinitialspace=True)
                lines = list(reader) 

            messages.extend(Message(
                role=line["role"],
                user=line["from"],
                dialog=line["to"],
                text=line["text"]
            ).as_llm_message() for line in lines)
        return messages
    
    def load_formatted_conversations(self, folder="conversations", files=None):
        """"Construct a dictionary of filename: [messages] from a list of formatted csv file names found in the conversations"""
        return {file: self.load_formatted_messages(folder=folder, files=[file]) for file in files or []}
