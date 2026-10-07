# AI Coding Agent

An AI-powered coding agent that understands natural-language developer tasks, analyzes a codebase, identifies relevant files, proposes code changes, generates code diffs, and validates the proposed changes using automated tests.


## Overview
-This project demonstrates a lightweight AI coding-agent workflow using Google Gemini.

-The agent analyzes a developer task, reads the relevant files from the repository, generates an    implementation plan, proposes code changes, displays the differences, and validates the proposed changes  using automated tests.


## Key Features

- Natural-language developer task input
- Repository-aware code analysis
- Relevant file identification
- AI-generated implementation plan
- AI-generated code change proposals
- Before/after code diff
- Safe validation using a temporary project copy
- Automated pytest testing
- Gemini API error handling and retry mechanism


## Workflow

Developer Task
      ↓
Streamlit Interface
      ↓
Gemini Analysis
      ↓
Relevant Files
      ↓
Implementation Plan
      ↓
Proposed Code Changes
      ↓
Diff Preview
      ↓
Temporary Project Copy
      ↓
Pytest Validation
      ↓
Validation Result


## Example Task
-The developer can enter a natural-language coding task such as:
-Add email validation to the user registration API and write a test for invalid emails.


## Project Structure
AI-Coding-Agent/
│
├── app.py
├── agent.py
├── codebase.py
├── diff_generator.py
├── validator.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── sample_project/
    ├── app.py
    ├── config.py
    ├── models.py
    ├── routers.py
    ├── services.py
    ├── validators.py
    │
    └── tests/
        ├── test_routes.py
        ├── test_services.py
        └── test_validators.py


## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google GenAI SDK
- Pytest
- pathlib
- difflib
- Git and GitHub   


## How It Works

# 1. Task Understanding
- The developer enters a coding task through the Streamlit interface.
- Gemini analyzes the task and the available codebase.

### 2. Codebase Analysis
- The agent reads relevant source and test files and provides them as context to Gemini.
- Gemini identifies the files relevant to the requested task.

### 3. Implementation Plan
Gemini generates:

- Task understanding
- Relevant files
- Implementation steps
- Expected changes

### 4. Code Change Proposal
Gemini generates the minimum required code changes, including the file path, updated code, and explanation

The original project files are not directly modified.


### 5. Diff Generation
The application compares the original code with Gemini's proposed code and displays a unified before/after diff.

### 6. Validation
- The proposed changes are applied to a temporary copy of the project.
- The existing pytest test suite is executed against the temporary copy.
- This keeps the original project unchanged during validation.


## Validation Result
The proposed code changes were successfully validated using the project's automated test suite.

10 tests collected
10 tests passed
0 tests failed


## Setup

### 1. Clone the Repository

bash
git clone https://github.com/123shraddha555/AI-Coding-Agent.git

cd AI-Coding-Agent

### 2. Install Dependencies
pip install -r requirements.txt


###3. Run the Application
python -m streamlit run app.py


## Safety Measures

- Original project files are not modified during validation.
- Proposed changes are tested in a temporary copy.
- Only existing Python files can be modified during validation.
- Path traversal is rejected.
- API keys and secrets are excluded from the repository.
- The agent does not automatically commit or push generated changes.


## Assumptions and Limitations

- The current demonstration uses a small Python sample project.

- The agent is designed as a lightweight coding-agent prototype.

- Gemini API availability, quota, and model availability can affect responses.

- A valid Gemini API key is required.

- The current version does not automatically commit or push generated changes.

- The current validation workflow is focused on Python projects using pytest.


## Approach

The project follows a controlled AI coding-agent workflow:

**Task Understanding → File Selection → Implementation Plan → Code Changes → Diff Generation → Isolated Validation**

The goal is to demonstrate how an LLM can be integrated with repository inspection, code-change generation, and automated validation in a practical development workflow.


## GitHub Repository
https://github.com/123shraddha555/AI-Coding-Agent


## Author:
**Shraddha Ghaytadkar**
