# Vertex AI Enterprise Setup Guide

## ? 개요

`self_healing_orchestrator.py`가 **Google Cloud Vertex AI**로 업그레이드되었습니다.

### 주요 이점

| 기능 | 무료 (Google AI Studio) | 유료 (Vertex AI) |
|------|------------------------|-----------------|
| **컨텍스트 윈도우** | 32K 토큰 | **2M 토큰** |
| **할당량** | RPM 제한 엄격 | **할당량 없음** |
| **모델** | flash만 | **Pro/Ultra** |
| **속도** | 느림 | **빠름** |
| **보안** | 데이터 학습 가능 | **데이터 미학습** |
| **비용** | 무료 | Pay-as-you-go |

---

## ? 선행 조건

### 1단계: GCP 프로젝트 생성

https://console.cloud.google.com 접속:

```powershell
# 또는 gcloud CLI로 생성
gcloud projects create wicked-zerg-ai --set-as-default
```

### 2단계: 결제 수단 등록

1. GCP Console → 결제
2. 결제 계정 연결
3. 신용카드 등록

### 3단계: Vertex AI API 활성화

```powershell
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com
```

### 4단계: 인증 설정

#### 옵션 A: gcloud CLI (권장)

```powershell
gcloud auth application-default login
```

#### 옵션 B: 서비스 계정 JSON (자동화)

1. GCP Console → IAM & Admin → 서비스 계정
2. 새 서비스 계정 생성
3. 역할: "Vertex AI User" + "Service Account User"
4. JSON 키 다운로드
5. 환경변수 설정:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account.json"
```

---

## ? 설치

### 필수 패키지

```powershell
pip install google-cloud-aiplatform>=1.45.0
```

### 환경변수 설정

#### Windows PowerShell

```powershell
# 세션별 설정 (임시)
$env:GCP_PROJECT_ID = "your-project-id"
$env:GCP_LOCATION = "us-central1"

# 영구 설정 (권장)
[Environment]::SetEnvironmentVariable("GCP_PROJECT_ID", "your-project-id", "User")
[Environment]::SetEnvironmentVariable("GCP_LOCATION", "us-central1", "User")
```

또는 `.env` 파일 생성 (자동 로드):

```env
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
```

#### 프로젝트 ID 확인

```powershell
gcloud config get-value project
```

---

## ? 사용 방법

### 기본 실행 (Pro 모델, 전체 프로젝트 분석)

```powershell
python self_healing_orchestrator.py `
  --file wicked_zerg_bot_pro.py `
  --model gemini-1.5-pro-002 `
  --full-context
```

### 빠른 수정 (Flash 모델)

```powershell
python self_healing_orchestrator.py `
  --file main_integrated.py `
  --model gemini-1.5-flash-002
```

### 게임 없이 테스트

```powershell
python self_healing_orchestrator.py `
  --file production_manager.py `
  --full-context `
  --no-game
```

### 타임아웃 조정

```powershell
python self_healing_orchestrator.py `
  --file wicked_zerg_bot_pro.py `
  --timeout 600 `
  --full-context
```

---

## ? 모델 선택 가이드

### `gemini-1.5-pro-002` (권장)

- **장점**: 가장 빠르고 안정적, 2M 토큰 지원
- **비용**: ~$0.001-$0.01 per request (매우 저렴)
- **용도**: 복잡한 코드 분석, 전체 프로젝트 수정

```powershell
--model gemini-1.5-pro-002  # 기본값
```

### `gemini-2.0-pro-exp-02-05` (최신)

- **장점**: 최신 기능, 더 나은 추론
- **단점**: 실험적 (불안정할 수 있음)
- **용도**: R&D, 복잡한 논리 분석

```powershell
--model gemini-2.0-pro-exp-02-05
```

### `gemini-1.5-flash-002` (저비용)

- **장점**: 매우 저렴, 빠름
- **단점**: 간단한 버그만 처리 가능
- **용도**: 빠른 수정, 비용 절감

```powershell
--model gemini-1.5-flash-002
```

---

## ? 고급 사용법

### 시스템 로그 확인

로그는 자동으로 저장됩니다:

```powershell
Get-ChildItem self_healing_logs/ | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

### 디버그 모드

```python
# self_healing_orchestrator.py 내부에서 로거 수준 변경
logger.remove()
logger.add(sink=sys.stderr, level="DEBUG")  # 상세 로그
```

### 특정 파일만 분석

```powershell
python self_healing_orchestrator.py `
  --file economy_manager.py `
  --no-game  # 게임 실행 스킵
```

---

## ? 문제 해결

### "GCP_PROJECT_ID not set" 에러

```powershell
# 현재 설정 확인
gcloud config get-value project

# 다시 설정
gcloud config set project your-project-id

# 또는 직접 환경변수 설정
$env:GCP_PROJECT_ID = "your-project-id"
```

### "Permission denied" 에러

```powershell
# 인증 재설정
gcloud auth application-default login

# 또는 서비스 계정 JSON 경로 확인
Get-ChildItem $env:GOOGLE_APPLICATION_CREDENTIALS
```

### "Quota exceeded" 에러

이는 발생하지 않습니다. Vertex AI는 할당량이 무제한입니다.
(분당 요청 수 제한 없음)

### API 호출 실패

```powershell
# Vertex AI API 활성화 확인
gcloud services list --enabled | grep aiplatform

# 또는 활성화
gcloud services enable aiplatform.googleapis.com
```

---

## ? 비용 추정

### Pro 모델 (gemini-1.5-pro-002)

```
입력 가격: $1.25 / 100만 토큰
출력 가격: $5.00 / 100만 토큰

예상 비용 (월):
- 500회 실행 × 50K 토큰 = 25M 토큰
- 입력: (25M ÷ 1M) × $1.25 = $31.25
- 출력: (5M ÷ 1M) × $5.00 = $25.00
- **총계: ~$60/월** (매우 저렴)
```

### Flash 모델 (gemini-1.5-flash-002)

```
입력 가격: $0.075 / 100만 토큰
출력 가격: $0.30 / 100만 토큰

동일 사용량:
- 입력: (25M ÷ 1M) × $0.075 = $1.88
- 출력: (5M ÷ 1M) × $0.30 = $1.50
- **총계: ~$3.50/월**
```

---

## ? 주요 기능

### 1. 전체 프로젝트 컨텍스트 분석

`--full-context` 옵션:
- 50개 Python 파일 모두 로드
- 2M 토큰으로 전체 의존성 분석
- 매니저 간 상호작용 고려

### 2. 자동 백업

수정 전 파일 자동 백업:
```
original_file.py
original_file.py.backup.20260109_120000
```

### 3. 반복적 수정

최대 5회 시도:
```
Attempt 1: 컴파일 에러 수정
Attempt 2: 런타임 에러 수정
Attempt 3: 로직 버그 수정
...
```

### 4. JSON 응답 파싱

Vertex AI의 구조화된 응답:
```json
{
    "cause": "await keyword missing on async call",
    "affected_systems": ["ProductionManager", "EconomyManager"],
    "fix_explanation": "...",
    "fixed_code": "...",
    "testing_notes": "..."
}
```

---

## ? 예제

### 예제 1: 단일 파일 빠른 수정

```powershell
python self_healing_orchestrator.py `
  --file queen_manager.py `
  --model gemini-1.5-flash-002 `
  --timeout 60
```

### 예제 2: 전체 프로젝트 심층 분석

```powershell
python self_healing_orchestrator.py `
  --file production_manager.py `
  --model gemini-1.5-pro-002 `
  --full-context `
  --timeout 300
```

### 예제 3: 코드 검증만 (게임 실행 X)

```powershell
python self_healing_orchestrator.py `
  --file economy_manager.py `
  --full-context `
  --no-game
```

---

## ? 지원

### Vertex AI 문서

https://cloud.google.com/vertex-ai/docs

### 가격 계산기

https://cloud.google.com/products/calculator

### 문제 보고

로그 파일 위치:
```
self_healing_logs/healing_YYYYMMDD_HHMMSS.log
```

---

## ? 체크리스트

- [ ] GCP 프로젝트 생성
- [ ] 결제 수단 등록
- [ ] Vertex AI API 활성화
- [ ] `gcloud auth application-default login` 실행
- [ ] `GCP_PROJECT_ID` 환경변수 설정
- [ ] `pip install google-cloud-aiplatform` 실행
- [ ] `python self_healing_orchestrator.py --file test.py --full-context` 테스트

---

**준비 완료! ? Vertex AI로 자동 코드 수정을 시작하세요!**
