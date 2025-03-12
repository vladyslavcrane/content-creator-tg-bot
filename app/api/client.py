from abc import ABC, abstractmethod
import logging
import openai

log = logging.getLogger(__name__)

openai_client = openai.Client()


class ContentClient(ABC):
    @abstractmethod
    def get_content(self, prompt):
        pass


class OpenAIContentClient(ContentClient):
    chat_model = "gpt-4o-mini"

    def __init__(self):
        self.api_client = openai_client

    def get_content(self, prompt):
        completion = self.api_client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {
                    "role": "developer",
                    "content": "Answer must be a JSON object",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        content = completion.choices[0].message.content
        log.info(f"ChatGPT answered:\n{content}")
        return content
