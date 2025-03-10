# stage0_echo
The Stage0 Echo Bot framework and LLM Training and Evaluation tools

This repo hosts key resources that implement the Echo Bot framework
- The stage0_echo pip module used by stage0_EchoBot services (fran, sam, etc.)
- The stage0_echo evaluation pipeline runbook. Stage0 echo services can use this runbook to evaluate models and prompts for their application
- The stage0_echo grading grader runbook. This runbook attempts to grade the grader with a key of human provided grades

# Some  LLM basics (it's not magic)
The first thing you need to know is that a Large Language Model (LLM) does not "remember" anything. While I'm skipping over a few things, the basics for interacting with a LLM is to call a ``chat(messages)`` function. Messages is a list of LLM formatted of chat messages. A LLM Chat message has the form ``{"role":"user", "content":"The chat message"}``. The valid roles are ``system``, ``user``, and ``assistant``. The back-and-forth of a conversation is reflected by alternating messages from the role ``user`` and ``assistant``. System messages are used for establishing a system prompt, and typically are at the beginning of the conversation, although the can occur anywhere. When you call the LLM ``chat(messages)`` function you provide a list of messages, and the LLM responds with the next message in the conversation. It is important to note that every call to ``chat()`` includes the entire conversation, from the ``system`` prompt messages and all of the back and forth up to the newest message. A significant portion of the echo code deals with a "conversation" that is just a ``list`` of ``Messages``. 

# It is about group chat, and an internal dialog
The Echo Bot framework is designed to participate in group conversations, and to use an "inner dialog" to interact with tools using a simple ``/agent/action/arguments`` syntax. In order for the AI to operate in this manner we need to provide some additional information in every message. Specifically a ``From`` value to identify a user name, and a ``To`` value to identify the dialog. The dialog will be ``group`` for the group chat with humans, and ``tools`` for the inner dialog with agents. Within the Echo code base, a [``Messages``](./src/echo/message.py) has the atomic values ``role``, ``user``, ``dialog``, and ``text``. This message can be rendered as a simple LLM Message with just ``role`` and ``content`` properties, with ``from``, ``to``, and ``text`` values combined in the ``content`` property.

# Evaluation Pipeline Runbook
This runbook reads a [configuration.yaml](./test/configuration/configuration.yaml) file, and loads the referenced evaluation data files, and then evaluates the model's responses to each assistant reply in a set of test conversations. Grades are assigned by a separate grading prompt that specializes in comparing given and expected values. 

## Using this in your project. 
Adjust this command to use appropriate values for your Echo Bot project. Your input folder should contain ``conversations``, ``grader``, and ``prompts`` folders with the csv files with your grader, prompts, and testing conversations. Your config folder should contain a ``configurations.yaml`` file. There is a [sample file](./test/configuration/configuration.yaml) in the test/configuration folder. A single output file called ``grades.json`` will be written to the output folder. Any existing ``grades.json`` file will be over-written.
```bash
docker run --rm /
    -v ./bot_name:/opt/input
    -v ./bot_name/config:/opt/config
    -v ./bot_name/output:/opt/output
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

# NOTE ==== FROM HERE DOWN IS ASPIRATIONAL =======
### Clear out the ./test/output folder
```bash
pipenv run clean
```

### Run Evaluate Runbook locally.
```bash
pipenv run local
```
Note: This does clean then runs the code locally

### Run Grader Runbook locally.
```bash
pipenv run grader
```

### Debug Evaluate Runbook locally
```bash
pipenv run debug
```
Runs locally with logging level set to DEBUG

### Build the Evaluate Runbook container
```bash
pipenv run build
```

### Build, and run the Evaluate Runbook container
```bash
pipenv run container
```
Note: Will use ./test folders

