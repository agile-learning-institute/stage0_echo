import unittest
from unittest.mock import patch, mock_open
from evaluator.evaluator import Evaluator

class TestEvaluator(unittest.TestCase):

    def setUp(self):
        self.evaluator = Evaluator(
            name="TestEvaluator", 
            model="",
            grade_prompt=[
                {"role":"user", "content":"a message"},
                {"role":"user", "content":"a message"},
                {"role":"user", "content":"a message"}
            ], 
            prompts=[
                {"role":"user", "content":"a message"},
                {"role":"user", "content":"a message"},
                {"role":"user", "content":"a message"},
                {"role":"user", "content":"a message"},
                {"role":"user", "content":"a message"}
            ], 
            conversations={
                "filename.csv": [
                    {"role":"user", "content":"a message"},
                    {"role":"user", "content":"a message"},
                    {"role":"user", "content":"a message"},
                    {"role":"user", "content":"a message"},
                    {"role":"user", "content":"a message"}
                ],
                "filename.csv": [
                    {"role":"user", "content":"a message"},
                    {"role":"user", "content":"a message"},
                    {"role":"user", "content":"a message"},
                    {"role":"user", "content":"a message"},
                    {"role":"user", "content":"a message"}
                ]
            }
        )

    def tearDown(self):
        pass
    
    def test_chat(self):
        # NOTE: Requires ollama, does not mock backing service
        # Arrange
        
        # Act
        
        # Assert
        self.assertFalse(True)

if __name__ == "__main__":
    unittest.main()