import unittest
from unittest.mock import patch, mock_open
from evaluator.loader import Loader

class TestEvaluator(unittest.TestCase):

    def setUp(self):
        self.loader = Loader(input_folder="./test")

    def tearDown(self):
        pass
    
    def test_load_messages(self):
        # NOTE: Requires ollama, does not mock backing service
        # Arrange
        
        # Act
        
        # Assert
        self.assertFalse(True)

    def test_load_formatted_messages(self):
        # NOTE: Requires ollama, does not mock backing service
        # Arrange
        
        # Act
        
        # Assert
        self.assertFalse(True)

    def test_load_formatted_conversations(self):
        # NOTE: Requires ollama, does not mock backing service
        # Arrange
        
        # Act
        
        # Assert
        self.assertFalse(True)
        
if __name__ == "__main__":
    unittest.main()