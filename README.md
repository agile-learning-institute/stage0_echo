# stage0_echo
The Stage0 Echo Bot framework and LLM Training and Evaluation tools and data

This repo hosts the stage0_echo pip module, as well as the Evaluate pipeline. The CI publishes both to Github Packages

# Evaluate Runbook
Runbook reads configuration.yaml file in the input folder, and csv message files from /prompts, and testing conversations from /conversations 
and then grades the performance of the configured models and prompts using the test conversations. 

# Grades

# Running Evaluations
```bash
docker run --rm /
    -v ~/config:/opt/config
    -v ~/input:/opt/input
    -v ~/output:/opt/output
    ghcr.io/agile-learning-institute/stage0-echo-evaluate:latest
```
Use the `-v` option to mount your local data directories:

# Table of Contents
- [Grades]() 
- [configuration.yaml]()
- [Grading Prompt]()

```yaml
- name:
  model:
  prompts: []
  conversations: []
- name:
```

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

### Clear out the [~/tmp/testRepo](~/tmp.testRepo) folder
```bash
pipenv run clean
```

### Copy [test/repo](./test/repo/) to [~/tmp/testRepo](~/tmp.testRepo)
```bash
pipenv run setup
```
Note: This does clean, then copy

### Run code locally.
```bash
pipenv run local
```
Note: This does clean, copy, then runs the code locally

### Compare output with expected
```bash
pipenv run test
```
Note: This is a ``df`` and will only report errors, no output is good output

### Build the container
```bash
pipenv run build
```

### Run the container
```bash
pipenv run container
```
Note: Will use the utility [test.sh](./.stage0_template/test.sh) script.

