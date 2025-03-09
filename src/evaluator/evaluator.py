import os
# from ollama import ollama
from echo.message import Message

import logging
logger = logging.getLogger(__name__)

class Evaluator:
    """
    Evaluate a Replies to a set of conversations
    
    parameters
    name: Configuration name
    model: LLM Model Name
    grade_prompt: Array of {role:, content:} messages used as the prompt for grading a reply
    prompts: Array of {role:, content:} messages used at the beginning of a conversation
    conversations: A dictionary of filename.csv entries, with Array of {role:, content:} messages to be evaluated
    """
    def __init__(self, name=None, model=None, grade_prompt=None, prompts=None, conversations=None):
        """ """
        self.input_folder = input
        self.name = name
        self.model = model
        self.grade_prompt = grade_prompt    # Grading Prompt [message]
        self.prompts = prompts              # Conversation engineered prompt [message]
        self.conversations = conversations  # Conversations for testing, dict of filename: [message]
        logger.info(f"Evaluator Initialized {self.name}")

    def evaluate(self):
        """Evaluate the conversations and report the grades"""
        grades = {
            "model": self.model,
            "prompts": self.prompt_files,
            "grader": self.grader_prompts
        }
        for name, conversation in self.conversations:
            grades[name] = self.grade_conversation(conversation)
            logger.info(f"Graded {name} as {grades[name]}")
        return grades

    def grade_conversation(self, conversation=[]):
        messages = self.prompts
        grades = []
        for message in conversation:
            messages.append(message)
            if message["role"] == "user":
                reply, latency = self.chat(messages=messages)
            elif message["role"] == "assistant":
                given=reply["content"]
                expected=message["content"]
                grades.append([latency, self.grade_reply(given, expected)])
        return grades
        
    def grade_reply(self, expected=None, given=None):
        # Use LLM model with grading prompts to grade message
        messages = self.grade_prompt[:]
        messages.append({"role":"user", "content": f"Grade the given value\n{given}\nAgainst the expected value\n{expected}"})
        grade, latency = self.chat(messages)["content"]
        # If grade not a good grade then log a error and return None
        return grade
    
    def chat(self, messages=None):
        # Get chat response to messages
        # return ollama.chat(model=self.model, messages=messages)
        # reply = ollama.chat(model=self.model, messages=messages)
        reply = {}
        latency = reply["latency"]
        response = reply["content"]
        return response, latency
        