import google.generativeai as genai
from django.conf import settings

_model = None


def get_model() -> genai.GenerativeModel:
    global _model
    if _model is None:
        genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
        _model = genai.GenerativeModel('gemini-1.5-flash')
    return _model
