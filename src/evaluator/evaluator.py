import os
import re

import ollama
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
    def __init__(self, name=None, model=None, grade_model=None, grade_prompt_files=None, grade_prompt=None, prompt_files=None, prompt=None, conversations=None):
        """ """
        self.input_folder = input
        self.name = name
        self.model = model
        self.grade_model = grade_model
        self.grade_prompt_files = grade_prompt_files
        self.grade_prompt = grade_prompt    
        self.prompt_files = prompt_files
        self.prompt = prompt
        self.conversations = conversations  
        logger.info(f"Evaluator {self.name} Initialized as {self}")

    def evaluate(self):
        """Evaluate the conversations and report the grades"""
        grades = {
            "model": self.model,
            "prompts": self.prompt_files,
            "grader": self.grade_prompt_files
        }
        for name, conversation in self.conversations.items():
            grades[name] = self.grade_conversation(conversation)
            logger.info(f"Graded {name} as {grades[name]}")
        return grades

    def grade_conversation(self, conversation=[]):
        messages = self.prompt[:]
        grades = []
        for message in conversation:
            messages.append(message)
            if message["role"] == "user":
                reply, latency = self.chat(messages=messages)
            elif message["role"] == "assistant":
                expected=message["content"]
                given=reply["content"]
                grade = self.grade_reply(expected=expected, given=given)
                grades.append({
                    "expected":expected, 
                    "given":given, 
                    "latency":latency, 
                    "grade":grade
                })
        return grades
        
    def grade_reply(self, expected=None, given=None):
        # Use LLM model with grading prompts to grade message
        messages = self.grade_prompt[:]
        messages.append({"role":"user", "content": f"Given:\n{given}\nExpected:\n{expected}"})
        reply, latency = self.chat(model=self.grade_model, messages=messages)
        content = reply["content"]
        grade = None
        try:
            match = re.search(r"the grade is (\d+(\.\d+)?)", content, re.IGNORECASE)
            if match:
                grade = float(match.group(1)) 
        except Exception:
            logger.warning(f"Grader didn't return a valid float: {content}")
            grade = None
        return grade
    
    def chat(self, model=None, messages=None):
        # Get chat response to messages
        # return ollama.chat(model=self.model, messages=messages)
        # reply = ollama.chat(model=self.model, messages=messages)
        model = model or self.model
        reply = ollama.chat(model=self.model, messages=messages)
        logger.debug(f"Chat reply {reply.message.content}")
        latency = reply.total_duration
        response = {
            "role":reply.message.role, 
            "content":reply.message.content
        }
        return response, latency
        