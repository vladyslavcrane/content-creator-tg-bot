import logging

log = logging.getLogger(__name__)


class FilePromptLoader:

    @staticmethod
    def get_prompt(file_path):
        try:
            with open(file_path) as f:
                return f.read()
        except FileNotFoundError:
            log.error(
                f"Trying to get a prompt from file `{file_path}` failed."
            )
            return ""
