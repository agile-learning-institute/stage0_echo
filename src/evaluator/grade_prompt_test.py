import unittest
from unittest.mock import patch, mock_open
from evaluator.evaluator import Evaluator
from evaluator.loader import Loader

import logging
logging.basicConfig(level="WARNING")
logger = logging.getLogger(__name__)

class TestGradePrompt(unittest.TestCase):
    # NOTE: Requires ollama, does not mock backing service

    def setUp(self):
        self.evaluator = Evaluator(
            name="TestEvaluator", 
            model="llama3.2:latest",
            grade_model="Gary:latest"
        )
        self.loader = Loader(input_folder="./test")

    def tearDown(self):
        pass
    
    def test_basic_grader(self):
        """Test grade_reply"""
        # Arrange
        self.evaluator.grade_prompt = self.loader.load_messages(["basic_grader.csv"])
        logger.warning("Starting")
        
        # Act
        grade = self.evaluator.grade_reply(expected="Good Answer", given="Great Answer!")
        logger.warning(f"Grade: {grade} - expect very high")    

        grade = self.evaluator.grade_reply(expected="I really think this is a great idea, I'm so glad you thought of it", given="Great Idea!")
        logger.warning(f"Grade: {grade} - expect high")    

        grade = self.evaluator.grade_reply(expected="Hi", given="Hello")
        logger.warning(f"Grade: {grade} - expect high")    

        self.assertTrue(True)
            
if __name__ == "__main__":
    unittest.main()