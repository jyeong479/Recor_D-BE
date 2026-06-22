# RecorD — 프로젝트 기록 관리 & 포트폴리오 자동 생성 서비스

> 회의록·할 일·일정을 프로젝트 단위로 기록하고, AI가 STAR 기법 기반의 포트폴리오 초안을 자동으로 생성해주는 서비스의 백엔드 레포지토리입니다.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.15-red?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-SimpleJWT-black?style=flat-square)
![CI](https://github.com/jyeong479/Recor_D-BE/actions/workflows/django.yml/badge.svg)

---

## 주요 기능

| 도메인 | 기능 |
|--------|------|
| **인증** | 카카오 소셜 로그인, JWT 발급 (Access 24h / Refresh 30d), 회원 탈퇴 |
| **프로젝트** | 프로젝트 CRUD, 멤버 초대 및 역할 관리 |
| **할 일** | 할 일 CRUD, 우선순위·마감일·완료 상태 관리 |
| **일정** | 일정 CRUD, 시작/종료 시간·색상·카테고리 설정 |
| **회의록** | 수동 작성 / 음성 파일 업로드 후 Whisper STT 자동 변환, Gemini AI 요약 |
| **포트폴리오** | STAR 기법 기반 초안 자동 생성, Gemini AI STAR 요약, 수동 편집 |

---

## 기술 스택

### Backend
- **Python 3.11** / **Django 4.2** / **Django REST Framework 3.15**
- **PostgreSQL** (Production) / **SQLite** (Local)
- **JWT 인증** — djangorestframework-simplejwt
- **API 문서** — drf-spectacular (Swagger UI)

### AI / 외부 API
- **Google Gemini** (`gemini-2.5-flash`) — 회의록 요약, STAR 포트폴리오 초안 생성
- **OpenAI Whisper** (`whisper-1`) — 음성 파일 STT 변환
- **카카오 OAuth 2.0** — 소셜 로그인

### DevOps
- **CloudType** — 서버 배포
- **GitHub Actions** — pytest 기반 CI (PR·main push 자동 실행)

---

## 핵심 구현 포인트

### 1. 음성 → 회의록 자동 생성 파이프라인
음성 파일(MP3, WAV 등 7종, 50MB 이하)을 업로드하면 OpenAI Whisper로 텍스트를 추출하고, Gemini에 회의록 요약 프롬프트를 던져 `key_points`·`action_items`를 구조화된 JSON으로 반환합니다.

```
POST /api/meetings/upload/
→ Whisper STT → Gemini 요약 → Meeting 초안 응답
```

### 2. 프로젝트 컨텍스트 기반 포트폴리오 자동 생성
유저가 프로젝트를 선택하면 해당 프로젝트에 연결된 완료된 할 일과 요약된 회의록 텍스트를 수집해 Gemini에 STAR 구조 초안 생성을 요청합니다. 응답은 `situation / task / action / result` 필드로 파싱해 DB에 저장합니다.

```
POST /api/portfolios/generate/
→ 완료 투두 + 회의록 요약 수집 → Gemini STAR 초안 생성 → Portfolio 저장
```

### 3. AI 응답 안전 파싱
Gemini 응답이 마크다운 코드블록에 감싸지거나 JSON 외 텍스트가 섞일 경우를 대비해 정규식 fallback 파싱 로직을 구현했습니다. LLM 응답 불안정성을 서비스 레이어에서 흡수합니다.

### 4. camelCase API 계약
프론트엔드와 응답 필드명을 camelCase로 통일했습니다. DRF SerializerMethodField + `source` 파라미터를 활용해 DB 모델의 snake_case와 API 응답의 camelCase를 명확히 분리했습니다.

---

## API 엔드포인트

| Method | URL | 설명 |
|--------|-----|------|
| POST | `/api/auth/kakao/login/` | 카카오 소셜 로그인 |
| POST | `/api/auth/token/refresh/` | Access Token 재발급 |
| DELETE | `/api/auth/withdraw/` | 회원 탈퇴 |
| GET/POST | `/api/projects/` | 프로젝트 목록 조회 / 생성 |
| GET/PATCH/DELETE | `/api/projects/{id}/` | 프로젝트 상세 / 수정 / 삭제 |
| GET/POST | `/api/todos/` | 할 일 목록 / 생성 |
| GET/PATCH/DELETE | `/api/todos/{id}/` | 할 일 상세 / 수정 / 삭제 |
| GET/POST | `/api/schedules/` | 일정 목록 / 생성 |
| GET/POST | `/api/meetings/` | 회의록 목록 / 수동 생성 |
| POST | `/api/meetings/upload/` | 음성 파일 업로드 → STT 초안 생성 |
| POST | `/api/meetings/{id}/summarize/` | 회의록 AI 요약 |
| GET/POST | `/api/portfolios/` | 포트폴리오 목록 / 생성 |
| POST | `/api/portfolios/generate/` | AI 포트폴리오 초안 자동 생성 |
| POST | `/api/portfolios/{id}/star-entries/{id}/summarize/` | STAR 항목 AI 요약 |

전체 명세: [Swagger UI](https://port-0-recor-d-be-moibwvfm46c84723.sel3.cloudtype.app/api/docs/) _(서버 미가동 시 접속 불가)_

---

## ERD

[ERD Cloud](https://www.erdcloud.com/d/E23uQY3p3nFSTBz9H)

---

## 로컬 실행

```bash
# 1. 의존성 설치
pip install -r requirements.txt
pip install pytest pytest-django

# 2. 환경변수 설정
cp .env.example .env
# .env 파일에 SECRET_KEY, GOOGLE_AI_API_KEY, OPENAI_API_KEY, KAKAO_* 값 입력

# 3. DB 마이그레이션
python manage.py migrate

# 4. 서버 실행
python manage.py runserver

# 5. 테스트 실행
pytest
```

### 필수 환경변수

| 변수 | 설명 |
|------|------|
| `SECRET_KEY` | Django 시크릿 키 |
| `GOOGLE_AI_API_KEY` | Google AI Studio API 키 |
| `GOOGLE_AI_MODEL` | Gemini 모델명 (기본값: `gemini-2.5-flash`) |
| `OPENAI_API_KEY` | OpenAI API 키 (Whisper STT) |
| `KAKAO_REST_API_KEY` | 카카오 REST API 키 |
| `KAKAO_REDIRECT_URI` | 카카오 OAuth 리디렉션 URI |

---

## 트러블슈팅

### 1. LLM 응답 파싱 실패 — 마크다운 코드블록 혼입
**문제** Gemini가 JSON을 그대로 반환하지 않고 ` ```json ... ``` ` 형태로 감싸서 반환하는 경우 `json.loads()`가 즉시 실패했음.

**해결** 1차로 `json.loads()` 시도 후 실패 시 정규식으로 `{...}` 블록만 추출해 재파싱하는 fallback 로직을 서비스 레이어에 구현. 필수 필드(`title`, `situation`, `task`, `action`, `result`) 누락 여부도 파싱 직후 검증해 불완전한 응답을 조기에 차단함.

```python
def _parse_json_response(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', text, flags=re.DOTALL)
        if not match:
            raise ValueError('AI 응답을 포트폴리오 형식으로 변환할 수 없습니다.')
        return json.loads(match.group(0))
```

---

### 2. CloudType 배포 후 서버 크래시 — openai 버전 충돌
**문제** `openai` 패키지를 버전 고정 없이 설치했더니 CloudType 배포 환경에서 최신 버전이 설치되어 기존 API 호출 방식과 충돌, 서버가 기동 직후 크래시됨. 또한 health check 엔드포인트가 없어 크래시 원인 파악이 늦어짐.

**해결** `requirements.txt`에 `openai>=1.0.0,<2.0.0`으로 버전 범위를 고정하고, `/health/` 엔드포인트를 추가해 배포 직후 서버 상태를 즉시 확인할 수 있도록 함.

---

### 3. 프로젝트 삭제 시 연관 데이터 유실 — CASCADE → SET_NULL
**문제** `Todo`, `Schedule`의 `project` FK가 `CASCADE`로 설정되어 있어 프로젝트 삭제 시 연관된 모든 할 일과 일정이 함께 삭제됨. 포트폴리오 생성 재료가 되는 데이터가 의도치 않게 사라지는 문제였음.

**해결** `on_delete=models.SET_NULL`로 변경해 프로젝트 삭제 후에도 투두·일정 데이터는 보존되도록 설계 변경.

---

### 4. Swagger 스키마 생성 시 인증 에러 — `swagger_fake_view` 미처리
**문제** `get_queryset()`에서 `request.user`로 필터링하는 구조였는데, drf-spectacular가 스키마를 생성할 때 인증 없이 뷰를 호출해 `AnonymousUser` 관련 에러가 발생하고 Swagger 문서가 깨짐.

**해결** 각 `get_queryset()` 최상단에 `swagger_fake_view` 가드를 추가해 스키마 생성 시점에는 빈 queryset을 반환하도록 처리.

```python
def get_queryset(self):
    if getattr(self, 'swagger_fake_view', False):
        return Meeting.objects.none()
    return Meeting.objects.filter(created_by=self.request.user)
```

---

### 5. AI 모델 하드코딩으로 인한 코드 수정 반복
**문제** `core/ai/client.py`에 `'gemini-1.5-flash'`가 하드코딩되어 있어 모델 업그레이드 시마다 코드를 직접 수정하고 재배포해야 했음.

**해결** `GOOGLE_AI_MODEL` 환경변수로 교체. `.env`만 변경하면 코드 수정 없이 모델을 교체할 수 있도록 개선. 같은 이유로 `OPENAI_TRANSCRIPTION_MODEL`도 환경변수로 분리함.

---

## 프로젝트 구조

```
apps/
├── accounts/     # 인증 (카카오 로그인, JWT, 회원 탈퇴)
├── projects/     # 프로젝트 & 멤버 관리
├── todos/        # 할 일 관리
├── schedules/    # 일정 관리
├── meetings/     # 회의록 (수동 작성 / 음성 업로드 + AI 요약)
└── portfolios/   # 포트폴리오 (STAR 구조 + AI 초안 생성)
core/
└── ai/           # Gemini / Whisper 클라이언트 & 서비스 레이어
config/
└── settings/     # base / local / production 환경 분리
```
