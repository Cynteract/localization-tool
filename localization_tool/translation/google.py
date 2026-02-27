from googletrans import Translator as GoogleTranslator
from .translator import BaseTranslator

class GoogleTranslate(BaseTranslator):
    def __init__(self):
        self.translator = GoogleTranslator()

    def translate(self, text, target_language):
        result = self.translator.translate(text, src='en', dest=target_language)
        # print(result, text, target_language, " google.py")
        translated_text = result.text

        confidence = None
        if hasattr(result, 'extra_data') and result.extra_data:
            confidence = result.extra_data.get('confidence')
        
        return translated_text, confidence