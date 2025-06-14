# from openrouter import OpenRouter
import os
import time
import requests
import json
from requests.exceptions import RequestException, HTTPError
from loguru import logger


API_KEY = os.getenv("OPENROUTER_API_KEY")

test = "openai/gpt-3.5-turbo"
model = "openai/gpt-4o"


def enrich_with_llm(
    prompt: str,
    model: str = "openai/gpt-4o",
    max_retries: int = 2,
    backoff_base: float = 1.0,
) -> str:

    for attempt in range(max_retries):
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}",},
                data=json.dumps(
                    {"model": model, "messages": [{"role": "user", "content": prompt}]}
                ),
            )

            # Check for 4xx/5xx errors
            response.raise_for_status()

            data = json.loads(response.content)
            llm_text = data["choices"][0]["message"]["content"]

            return llm_text

        except (RequestException, HTTPError) as e:
            if attempt == max_retries:
                raise

            sleep_time = backoff_base * (2 ** (attempt - 1))
            time.sleep(sleep_time)

    raise RuntimeError("Failed to get a response.")


if __name__ == "__main__":
    test_prompt = "What is the meaning of life?"
    print(enrich_with_llm(test_prompt, model="openai/gpt-3.5-turbo"))