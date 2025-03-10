# stage0_echo
The Stage0 Echo Bot framework and LLM Training and Evaluation tools

This repo hosts key resources that implement the Echo Bot framework
- The stage0_echo pip module used by stage0_EchoBot services (fran, sam, etc.)
- The stage0_echo evaluation pipeline runbook. Stage0 echo services can use this runbook to evaluate models and prompts for their application
- The stage0_echo grading grader runbook. This runbook attempts to grade the grader with a key of human provided grades

# Evaluation Pipeline Runbook
This runbook reads a configuration.yaml file, and referenced evaluation data files, and then it evaluates
the model's responses to each assistant reply in a test conversation. Grades are assigned by a separate grading prompt
that specializes in comparing given and expected values. 

## Using this in your project. 
Adjust this command to use appropriate values for the input and output volumes in your project. Your input folder should contain ``conversations``, ``grader``, and ``prompts`` folders with the csv files with your grader, prompts, and testing conversations. Your config folder should contain a ``configurations.yaml`` file. There is a [sample file](./test/configuration/configuration.yaml) in the test/configuration folder. A single output file called ``grades.json`` will be written to the output folder.
```bash
docker run --rm /
    -v ~/config:/opt/config
    -v ~/input:/opt/input
    -v ~/output:/opt/output
    ghcr.io/agile-learning-institute/stage0-echo-evaluate:latest
```

# Grader Pipeline Runbook
This runbook accepts as parameters the grading prompts, and key files to use in evaluating the grader. Key files consist of input Given and Expected values along with human assigned grade min/max values. The provided values are presented to the grading prompt, and their given grade is noted in the output.

# Stage0 Echo Module
This is still to be moved from stage0_fran. Will need additional packaging (__init.py__)

# Contributing

## Prerequisites

Ensure the following tools are installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

## Testing

## Install Dependencies
```bash
pipenv install
```

### Clear out the ./test/output folder
```bash
pipenv run clean
```

### Run code locally.
```bash
pipenv run local
```
Note: This does clean then runs the code locally

### Debug code locally.
```bash
pipenv run debug
```
Note: This does clean then runs the code locally with logging set to DEBUG

### Build the Evaluate Runbook container
```bash
pipenv run build
```

### Build, and run the Evaluate Runbook container
```bash
pipenv run container
```
Note: Will use ./test folders

