from deep_translator import GoogleTranslator
from langdetect import detect


# Detect language
def detect_language(text):

    try:
        language = detect(text)

        return language

    except:

        return "en"


# Translate to English
def translate_to_english(text):

    try:

        translated = GoogleTranslator(
            source='auto',
            target='en'
        ).translate(text)

        return translated

    except:

        return text


# Translate back to original language
def translate_answer(text, target_language):

    try:

        if target_language == "en":
            return text

        translated = GoogleTranslator(
            source='en',
            target=target_language
        ).translate(text)

        return translated

    except:

        return text