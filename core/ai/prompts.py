MEETING_SUMMARY_PROMPT = """다음 회의록을 분석하여 아래 형식으로 요약해주세요.

**주요 결정 사항**
- (결정된 내용을 간결하게 나열)

**액션 아이템**
- (담당자: 할 일)

**다음 회의 안건**
- (논의할 내용)

회의록:
{content}"""

STAR_SUMMARY_PROMPT = """다음 프로젝트 경험을 STAR 기법을 바탕으로 포트폴리오용 소개글로 작성해주세요.
자연스러운 한 문단으로 200자 내외로 작성하고, 수치나 성과가 있으면 반드시 포함하세요.

상황(Situation): {situation}
목표(Task): {task}
행동(Action): {action}
결과(Result): {result}"""
