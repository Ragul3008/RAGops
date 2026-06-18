import re

class TextCleaner:
    def clean(self, text: str) -> str:
        if not text:
            return ""
        # Strip leading/trailing whitespaces and normalize multiple spaces/newlines
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text
