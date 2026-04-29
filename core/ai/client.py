import google.generativeai as genai
from django.conf import settings

_configured = False


def configure():
    global _configured
    if not _configured:
        genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
        _configured = True
