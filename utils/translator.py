from deep_translator import GoogleTranslator
from langdetect import detect


# Detect language
def detect_language(text):

    try:
        return detect(text)

    except:
        return "en"


# Translate user question to English
def translate_to_english(text):

    try:

        language = detect_language(text)

        if language == "en":
            return text

        translated = GoogleTranslator(
            source='auto',
            target='en'
        ).translate(text)

        return translated

    except Exception as e:

        print("Translation Error:", e)

        return text


# Translate answer back to original language
def translate_answer(answer, target_language):

    try:

        if target_language == "en":
            return answer

        translated = GoogleTranslator(
            source='en',
            target=target_language
        ).translate(answer)

        return translated

    except Exception as e:

        print("Answer Translation Error:", e)

        return answer