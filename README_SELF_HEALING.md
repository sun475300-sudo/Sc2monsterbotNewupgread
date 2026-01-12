# ? Self-Healing Orchestrator
## Gemini API를 활용한 자동 Python 버그 수정 시스템

> **한 줄 요약**: 코드를 실행하면 에러가 자동으로 감지되고, Gemini AI가 원인을 분석해 수정안을 제시하며, 파일이 자동 업데이트됩니다.

---

## ? 핵심 특징

| 기능 | 설명 |
|------|------|
| **자동 감지** | 코드 실행 후 에러 자동 캡처 |
| **AI 분석** | Gemini 2.0-Flash로 원인 분석 |
| **자동 수정** | 수정된 코드 도출 및 적용 |
| **반복 검증** | 수정 후 재실행하여 성공 확인 |
| **안전성** | 원본 파일 자동 백업 |
| **배치 처리** | 여러 파일 순차 처리 |

---

## ? 포함된 파일

```
프로젝트/
├── self_healing_orchestrator.py       ← 메인 도구 (단일 파일)
├── batch_auto_fix.py                  ← 배치 처리 도구
├── setup_self_healing.bat              ← Windows 설정 마법사
├── create_test_files.py                ← 테스트 파일 생성기
│
├── SELF_HEALING_GUIDE.md               ← 완전 사용 설명서
├── SELF_HEALING_QUICKREF.md            ← 빠른 참조 (자주 쓰는 명령)
├── SELF_HEALING_COMPLETE.md            ← 심화 가이드
└── README_SELF_HEALING.md              ← 이 파일
```

---

## ? 5분 안에 시작하기

### 1?? Gemini API 키 발급 (2분)

```
웹사이트: https://aistudio.google.com
1. "Get API Key" 클릭
2. "Create API Key" 선택
3. 키 복사
```

### 2?? 환경 변수 설정 (1분)

**PowerShell (관리자 권한)**:
```powershell
[System.Environment]::SetEnvironmentVariable(
    "GEMINI_API_KEY",
    "YOUR_KEY_HERE",
    "User"
)
```

**또는 배치 파일 실행**:
```bash
setup_self_healing.bat
```

### 3?? 패키지 설치 (1분)

```bash
pip install google-generativeai loguru
```

### 4?? 실행 (즉시)

```bash
# 테스트 파일 먼저 생성
python create_test_files.py

# 자동 수정 실행
python self_healing_orchestrator.py --file test_with_error.py
```

---

## ? 작동 원리

```
┌─────────────────┐
│  파이썬 파일 실행 │
└────────┬────────┘
         │
         ▼
    ? 성공?
    ?         ?
   ?          ?
   │            │
   │            ▼
   │      ┌──────────────────┐
   │      │ 에러 메시지 추출  │
   │      └────────┬─────────┘
   │             │
   │             ▼
   │      ┌──────────────────────────────┐
   │      │ Gemini API에 분석 요청       │
   │      │ (소스코드 + 에러 메시지)    │
   │      └────────┬─────────────────────┘
   │             │
   │             ▼
   │      ┌──────────────────────────────┐
   │      │ 수정 코드 도출               │
   │      │ (```python ... ``` 형식)   │
   │      └────────┬─────────────────────┘
   │             │
   │             ▼
   │      ┌──────────────────────────────┐
   │      │ 파일 업데이트 (백업 생성)   │
   │      └────────┬─────────────────────┘
   │             │
   │             ▼
   │      ┌──────────────────┐
   │      │  2초 대기         │
   │      └────────┬─────────┘
   │             │
   └─────────────┘
              │
              ▼
        [반복 1~5회]
              │
         ? 최대 시도 도달?
         ?              ?
        ?               ?
        │                 │
        ▼                 ▼
     완료            실패 (백업 유지)
```

---

## ? 자주 쓰는 명령어

### 단일 파일 수정

```bash
# 기본
python self_healing_orchestrator.py --file my_script.py

# 3회만 시도 (빠른 테스트)
python self_healing_orchestrator.py --file test.py -m 3

# 타임아웃 30초
python self_healing_orchestrator.py --file test.py -t 30

# 조합
python self_healing_orchestrator.py -f test.py -m 3 -t 60
```

### 여러 파일 배치 처리

```bash
# 기본 파일들만
python batch_auto_fix.py

# 특정 파일들
python batch_auto_fix.py -f file1.py file2.py file3.py

# 모든 .py 파일
python batch_auto_fix.py --all
```

### 로그 확인

```bash
# 최신 로그
type self_healing_logs\healing_*.log | tail -20

# 모든 로그 파일 목록
dir self_healing_logs\
```

---

## ? 실제 사용 예시 (Wicked Zerg 봇)

### 시나리오 1: 스타트업 에러

```bash
$ python self_healing_orchestrator.py --file test_startup.py

[시도 1/5]
? ImportError: cannot import name 'CombatManager'

[Gemini 분석 중...]

[시도 2/5]
? 성공! 모듈 경로 수정됨
```

### 시나리오 2: 메서드 시그니처 변경

```bash
$ python self_healing_orchestrator.py --file wicked_zerg_bot_pro.py

[시도 1/5]
? TypeError: update() missing 2 required arguments

[Gemini 분석 중...]

[시도 2/5]
? 성공! 모든 호출부에 인자 추가됨
```

### 시나리오 3: 배치 처리

```bash
$ python batch_auto_fix.py

[1/6] test_startup.py ?
[2/6] test_modularization.py ?
[3/6] production_manager.py ? (수정 불가능)
[4/6] combat_manager.py ?
[5/6] economy_manager.py ?
[6/6] wicked_zerg_bot_pro.py ?

? 결과: 5/6 성공 (83%)
```

---

## ? 옵션 설명

### `self_healing_orchestrator.py`

| 옵션 | 약자 | 기본값 | 설명 |
|------|-----|-------|------|
| `--file` | `-f` | **필수** | 실행할 파이썬 파일 |
| `--max-fixes` | `-m` | 5 | 최대 수정 시도 횟수 |
| `--timeout` | `-t` | 120 | 코드 실행 타임아웃 (초) |

### `batch_auto_fix.py`

| 옵션 | 설명 |
|------|------|
| `-f, --files` | 수정할 파일 목록 |
| `--all` | 모든 .py 파일 처리 |
| `--max-fixes` | 파일당 최대 시도 |
| `--timeout` | 파일당 타임아웃 |

---

## ? 출력 파일

### 자동 백업
```
my_script.py                    (원본, 수정됨)
my_script.py.bak_20260109_162348  (자동 백업)
```

### 로그 파일
```
self_healing_logs/
├── healing_20260109_162345.log      (상세 로그)
├── report_20260109_162345.json      (세션 리포트)
└── batch_report_20260109_162350.json (배치 리포트)
```

---

## ?? 시스템 요구사항

| 요구사항 | 최소 | 권장 |
|---------|-----|------|
| Python | 3.8 | 3.10+ |
| 인터넷 | 필수 | 10Mbps+ |
| API 키 | 필수 | 무료 tier |
| 메모리 | 2GB | 4GB+ |

---

## ? 문서

| 문서 | 용도 |
|------|------|
| [SELF_HEALING_GUIDE.md](SELF_HEALING_GUIDE.md) | 완전 사용 설명서 |
| [SELF_HEALING_QUICKREF.md](SELF_HEALING_QUICKREF.md) | 자주 쓰는 명령어 |
| [SELF_HEALING_COMPLETE.md](SELF_HEALING_COMPLETE.md) | 심화 설정 및 팁 |

---

## ?? 안전성

### ? 보장 사항

- ? **자동 백업**: 모든 수정 전에 원본 파일 백업
- ? **원자성**: 파일 쓰기 실패 시 원본 유지
- ? **검증**: 수정된 코드를 바로 실행하여 검증
- ? **기능 보존**: 원본 기능은 변경하지 않음

### ?? 주의사항

- 매우 큰 파일 (>10MB)는 API 토큰 제한 가능
- 네트워크 끊김 시 동작 불가
- 복잡한 의존성 에러는 여러 회 시도 필요
- 일부 에러는 자동 수정 불가능할 수 있음

---

## ? 문제 해결

### "GEMINI_API_KEY가 설정되지 않았습니다"

```powershell
# 임시 설정
$env:GEMINI_API_KEY = "YOUR_KEY"

# 영구 설정
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "YOUR_KEY", "User")
```

### "ModuleNotFoundError: No module named '...'"

```bash
# 필수 패키지 설치
pip install google-generativeai loguru burnysc2 numpy torch
```

### "Gemini API 호출 실패"

- 인터넷 연결 확인
- API 키 유효성 확인
- 속도 제한: 1분에 60회 요청 (자동 대기)

### "타임아웃 에러"

```bash
# 타임아웃 증가
python self_healing_orchestrator.py --file slow.py --timeout 300
```

---

## ? 성능

### 처리 시간

| 에러 복잡도 | 시도 횟수 | 소요 시간 |
|-----------|---------|---------|
| 단순 (구문) | 1-2 | 10-20초 |
| 중간 (논리) | 2-3 | 20-45초 |
| 복잡 (의존성) | 3-5 | 45-120초 |

### API 비용

- **무료 tier**: 1분에 60회 요청
- **토큰 제한**: 약 1,000회/일
- **대부분의 사용 사례가 무료 범위 내**

---

## ? 팁 & 트릭

### 백그라운드 실행

```bash
# PowerShell
Start-Process python -ArgumentList 'self_healing_orchestrator.py --file test.py'
```

### 정기적 자동 실행

```powershell
# 매 10분마다
while ($true) {
    python self_healing_orchestrator.py --file test.py
    Start-Sleep -Seconds 600
}
```

### 병렬 처리

```bash
REM 3개 파일 동시
start python self_healing_orchestrator.py -f file1.py
start python self_healing_orchestrator.py -f file2.py
start python self_healing_orchestrator.py -f file3.py
```

---

## ? 고급 사용법

### 자신의 API 키 사용

Gemini 외 다른 LLM API 사용 가능:

```python
# self_healing_orchestrator.py 수정
import anthropic  # Claude API
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
```

### 커스텀 모델 선택

```python
# 빠르고 저렴
model = genai.GenerativeModel("gemini-2.0-flash")

# 더 정확 (느림)
# model = genai.GenerativeModel("gemini-1.5-pro")
```

---

## ? 지원 및 피드백

- ? 버그 리포트: `self_healing_logs/`의 로그 파일 첨부
- ? 기능 제안: GitHub Issues
- ? 문의: [프로젝트 메인테이너]

---

## ? 라이선스

Wicked Zerg Challenger 프로젝트의 일부입니다.

---

## ? 시작하기

```bash
# 1. 테스트 파일 생성
python create_test_files.py

# 2. 첫 번째 자동 수정 실행
python self_healing_orchestrator.py --file test_with_error.py

# 3. 로그 확인
type self_healing_logs\healing_*.log
```

---

**Happy Debugging! ?**

*한 줄의 명령으로 수십 개의 버그를 자동으로 해결하세요.*

---

## 변경 로그

### v1.0 (2026-01-09)
- ? 초기 릴리스
- ? Gemini 2.0-Flash 통합
- ? 배치 처리 지원
- ? 상세 로깅 및 리포팅

### 예정 (v1.1)
- ? 병렬 처리
- ? 웹 대시보드
- ? 시각화 개선

### 예정 (v2.0)
- ? 자체 RL 에이전트
- ? CI/CD 통합
- ? 학습 데이터 축적

---

**마지막 업데이트**: 2026-01-09
**버전**: 1.0
**상태**: ? 프로덕션 준비 완료
