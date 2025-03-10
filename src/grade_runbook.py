import json
import os
import sys
from evaluator.evaluator import Evaluator
from evaluator.loader import Loader

import logging
logger = logging.getLogger(__name__)

class Runbook:
    """
    Processor class for testing a grading prompt using a grading key
    """
    def __init__(self, grade_prompts=None, grade_keys=None, input_folder="./input"):
        self.loader = Loader(input_folder=input_folder)
        self.evaluator = Evaluator(
            name="Grade Prompt Evaluator", 
            grade_model="Gary:latest",
            grade_prompt=self.loader.load_messages(files=grade_prompts)
        )
        self.grade_keys = self.loader.load_messages(files=grade_keys)
    
    def run(self):
        """Process Evaluation Configuration"""
        outcomes = []
        passing = 0
        for line in self.grade_keys:
            given = line["given"]
            expected = line["expected"]
            min_value = line["min_value"]
            max_value = line["max_value"]
            grade = self.evaluator.grade_reply(expected=expected, given=given)
            outcomes.append({
                "Given": given, 
                "Expected": expected, 
                "Grade": grade, 
                "Min Expected": min_value, 
                "Max Expected": max_value
            })
            if min_value <= grade <= max_value:
                passing += 1
            logger.info(f"Grade: {grade}, Pass: {min_value <= grade <= max_value}")
                
        print(outcomes)
        print(f"Grade: {passing / len(outcomes)}")
    
def main():
    input_folder = os.getenv("INPUT_FOLDER", "./test/configuration")
    logging_level = os.getenv("LOG_LEVEL", "INFO")

    # Get Grading Prompt Files and Key Files
    grade_prompts = json.loads(sys.argv[1]) or ["basic_grader.csv"] or sys.exit(1)
    grade_keys = json.loads(sys.argv[2]) or ["basic_grader_key.csv"] or sys.exit(1)
    
    logging.basicConfig(level=logging_level)
    logger.info(f"======================== Grader Evaluation Pipeline Starting ============================")
    logger.info(f"Initialized, Input: {input_folder}, Logging @{logging_level}")
    logger.info(f"Processing using grader prompts: {grade_prompts}")
    logger.info(f"Using grader keys: {grade_keys}")
    
    try:
        runner = Runbook(input_folder=input_folder, grade_prompts=grade_prompts, grade_keys=grade_keys)
        runner.run()
    except Exception as e:
        logger.error(f"Error Reported {str(e)}")
    logger.info(f"=================== Grader Evaluation Pipeline Completed Successfully =====================")

if __name__ == "__main__":
    main()