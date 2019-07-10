from textblob import TextBlob
from textblob.exceptions import NotTranslated
from translate import Translator


def get_sentiment(text, lang):
    try:
        if lang == 'en':
            blob = TextBlob(text)
            sentiment, subjectivity = blob.sentiment
        else:
            translator = Translator(from_lang=lang, to_lang="en")
            translation = translator.translate(text)
            if translation[-10:] == 'NO CONTENT':
                return 0.0
            blob = TextBlob(translation)
            sentiment, subjectivity = blob.sentiment

        if subjectivity < 0.1:
            sentiment = 0.0

    except NotTranslated:
        sentiment = 0.0
    return sentiment
