import google.generativeai as genai
from .client import configure
from .prompts import MEETING_SUMMARY_PROMPT, STAR_SUMMARY_PROMPT

MODEL = "gemini-1.5-flash"


def summarize_meeting_note(content: str) -> str:
    configure()
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(MEETING_SUMMARY_PROMPT.format(content=content))
    return response.text


def generate_star_summary(situation: str, task: str, action: str, result: str) -> str:
    configure()
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(STAR_SUMMARY_PROMPT.format(
        situation=situation,
        task=task,
        action=action,
        result=result,
    ))
    return response.text
