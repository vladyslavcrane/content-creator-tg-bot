import logging
import os
import json
from typing import Union
import openai

from settings import BASE_DIR

log = logging.getLogger(__name__)

client = openai.Client()

def get_prompt_from_file(fp: Union[str, "os.PathLike[str]"]):
    try:
        with open(fp) as file:
            prompt = file.read()
    except FileNotFoundError:
        log.error(
            f"Trying to get a prompt from file `{fp}` failed. Returning empty string."
        )
        return ""
    return prompt


def get_completion(prompt: str = ""):

    if not prompt:
        prompt = get_prompt_from_file(BASE_DIR / "prompt.txt")

    if prompt and isinstance(prompt, str):
        log.info('Asking ChatGPT....')

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer",
                    "content": 'Answer must be a JSON object',
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        answer = completion.choices[0].message.content

        log.info(f'ChatGPT answered:\n{answer}')

        current_response = json.loads(answer)

        with open(BASE_DIR / 'openai_movie_responses.json', 'r+') as file:
            responses = json.load(file)
            responses['all'].append(current_response)

            file.seek(0)
            file.write(json.dumps(responses, indent=2))

        return current_response

    log.warning("Couldn't parse a prompt. OpenAI API hasn't called")

    return {}
