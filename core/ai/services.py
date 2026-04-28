from .client import get_client
from .prompts import MEETING_SUMMARY_PROMPT, STAR_SUMMARY_PROMPT

MODEL = "claude-sonnet-4-6"


def summarize_meeting_note(content: str) -> str:
    client = get_client()
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": MEETING_SUMMARY_PROMPT.format(content=content)}],
    )
    return message.content[0].text


def generate_star_summary(situation: str, task: str, action: str, result: str) -> str:
    client = get_client()
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": STAR_SUMMARY_PROMPT.format(
                situation=situation,
                task=task,
                action=action,
                result=result,
            ),
        }],
    )
    return message.content[0].text
