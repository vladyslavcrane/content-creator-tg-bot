from abc import ABC, abstractmethod
import json
import logging
from typing import Any, Dict, Optional, Union
from openai import Client as OpenaiClient

log = logging.getLogger(__name__)

openai_client = OpenaiClient()


class ContentClientException(Exception):
    pass


class ContentSerializationError(ContentClientException):
    pass


class ContentClient(ABC):
    @abstractmethod
    def get_content(self, prompt: str) -> Dict[Any, Any]:
        pass


class OpenAIContentClient(ContentClient):
    chat_model = "gpt-4o-mini"

    def __init__(self) -> None:
        self.api_client: OpenaiClient = openai_client
        self.content: Optional[Dict[Any, Any]] = None

    def get_content(self, prompt: str) -> Dict[Any, Any]:
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
        raw_content = completion.choices[0].message.content
        log.info(f"ChatGPT answered:\n{raw_content}")
        self.content = self.serialize_content(raw_content or "")

        return self.content

    def serialize_content(
        self, content: Union[str, bytes, bytearray]
    ) -> Dict[Any, Any]:
        try:
            serialized_content = json.loads(content)
            if not isinstance(serialized_content, dict):
                raise ContentSerializationError(f"Content is not a dictionary")
            return serialized_content
        except (TypeError, ValueError):
            raise ContentSerializationError(f"Content serialization failed")
