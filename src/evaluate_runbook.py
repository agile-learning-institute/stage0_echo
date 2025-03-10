import os
from evaluator.evaluator import Evaluator
from evaluator.loader import Loader

class Runbook:
    """
    Processor class for evaluating a Echo LLM Configuration (Models and Prompts)
    """
    def __init__(self, config_folder="./config", input_folder="./input", output_folder="./output"):
        self.config_folder = config_folder
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.configs = []            # load config_folder/configuration.yaml
    
    def run(self):
        """Process Evaluation Configuration"""
        output = {}
        for config in self.configs:
            # Setup Evaluator
            loader = Loader(input_folder=self.input_folder)
            evaluator = Evaluator(
                name=config["name"], 
                model=config["model"], 
                grade_model=config["grade_model"],
                grade_prompt_files=config["grade_prompt"],
                grade_prompt=loader.load_messages(files=config["grade_prompt"]), 
                prompt_files=config["prompts"],
                prompt=loader.load_formatted_messages(files=config["prompts"]), 
                conversations=loader.load_formatted_conversations(files=config["conversations"])
            )

            # Evaluate the configured conversations
            output[config["name"]] = config
            output[config["name"]]["grades"] = evaluator.evaluate()
            
        # Write output
        # fs.write(self.output_folder, filename, output)
        pass
    
def main():
    input_folder = os.getenv("INPUT_FOLDER", "./test")
    output_folder = os.getenv("OUTPUT_FOLDER", "./test/output")
    config_folder = os.getenv("CONFIG_FOLDER", "./test/configuration")
    logging_level = os.getenv("LOG_LEVEL", "INFO")

    import logging
    logging.basicConfig(level=logging_level)
    logger = logging.getLogger(__name__)
    logger.info(f"============================ Evaluation Pipeline Starting ==============================")
    logger.info(f"Initialized, Input: {input_folder}, Output: {output_folder}, Config: {config_folder} Logging Level {logging_level}")
    
    try:
        runner = Runbook(config_folder=config_folder, input_folder=input_folder, output_folder=output_folder)
        runner.run()
    except Exception as e:
        logger.error(f"Error Reported {str(e)}")
    logger.info(f"===================== Evaluation Pipeline Completed Successfully =======================")

if __name__ == "__main__":
    main()