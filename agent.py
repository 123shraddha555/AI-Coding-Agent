from google import genai
from google.genai import errors
import json
import time

MODEL_NAME = "gemini-3.1-flash-lite"


def create_client(api_key):
    """Create and return a Gemini API client."""
    return genai.Client(api_key=api_key)




def generate_response(client, prompt):
    """Send prompt to Gemini with safe retry handling."""

    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            return response

        except errors.ServerError as error:

            if error.code == 503:

                if attempt < max_attempts - 1:
                    time.sleep(2 * (attempt + 1))
                    continue

                raise RuntimeError(
                    "Gemini is temporarily overloaded. "
                    "Please try again in a few seconds."
                )

            raise RuntimeError(
                f"Gemini server error ({error.code}): {error}"
            )

        except errors.ClientError as error:

            if error.code == 429:
                raise RuntimeError(
                    "Gemini quota/rate limit reached. "
                    "Please try again later."
                )

            if error.code == 403:
                raise RuntimeError(
                    "Gemini API access was denied. "
                    "Please check the API key."
                )

            if error.code == 404:
                raise RuntimeError(
                    "The configured Gemini model is unavailable."
                )

            raise RuntimeError(
                f"Gemini API error ({error.code}): {error}"
            )

        except OSError:
            raise RuntimeError(
                "Network error while connecting to Gemini."
            )


        
def analyze_task(client, task, codebase_context):
    """
    Analyze the developer task and identify relevant files.
    """

    prompt = f"""
You are an AI coding agent.

Developer Task:
{task}

Codebase:
{codebase_context}

Analyze the developer task.

Return exactly these sections:

1. Task Understanding
2. Relevant Files
3. Implementation Plan
4. Expected Changes

Be concise.

Only mention files that actually exist in the codebase.

Do not include API keys, passwords, or secrets.
"""

    response = generate_response(
        client,
        prompt
    )

    return response.text


def generate_changes(client, task, codebase_context):
    """
    Generate the code changes required to complete the task.
    """

    prompt = f"""
You are an AI coding agent.

Developer Task:
{task}

Codebase:
{codebase_context}

Create the minimum code changes required to complete the task.

Return ONLY valid JSON using this structure:

{{
    "changes": [
        {{
            "file": "sample_project/file.py",
            "updated_code": "complete updated file content"
        }}
    ],
    "explanation": "Short explanation of the changes."
}}

Rules:

- Modify only relevant existing files.
- Return complete content for every modified file.
- Do not modify unrelated files.
- Do not create new files unless required.
- Only use files that exist in the codebase.
- Do not include API keys, passwords, or secrets.
- Return valid JSON only.
"""

    response = generate_response(
        client,
        prompt
    )

    text = response.text.strip()

    # Remove Markdown code fences if Gemini adds them
    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError as error:

        raise RuntimeError(
            f"Gemini returned invalid JSON: {error}"
        )