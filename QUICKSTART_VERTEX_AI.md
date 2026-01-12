# ? Vertex AI 즉시 시작 (5분)

## 1단계: 패키지 설치 (1분)

```powershell
pip install google-cloud-aiplatform
```

## 2단계: GCP 인증 (2분)

### 옵션 A: 간단한 방법 (권장)

```powershell
gcloud auth application-default login
```

브라우저가 열리면 Google 계정으로 로그인하세요.

### 옵션 B: 프로젝트 ID가 없는 경우

```powershell
gcloud auth login
gcloud projects list
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
```

## 3단계: 환경변수 설정 (1분)

### Windows PowerShell (영구 설정)

```powershell
# 프로젝트 ID 확인
gcloud config get-value project

# 환경변수 설정 (영구)
[Environment]::SetEnvironmentVariable("GCP_PROJECT_ID", "your-project-id", "User")
[Environment]::SetEnvironmentVariable("GCP_LOCATION", "us-central1", "User")

# 재부팅 또는 PowerShell 재시작
```

### Windows CMD (세션용)

```cmd
set GCP_PROJECT_ID=your-project-id
set GCP_LOCATION=us-central1
```

## 4단계: 즉시 테스트 (1분)

```powershell
# 간단한 파일 수정 테스트
python self_healing_orchestrator.py --file wicked_zerg_bot_pro.py --model gemini-1.5-pro-002 --no-game

# 또는 전체 분석 (프로젝트 수정)
python self_healing_orchestrator.py --file production_manager.py --full-context --model gemini-1.5-pro-002
```

---

## ? 주요 명령어

### Pro 모델 + 전체 프로젝트 분석 (권장)

```powershell
python self_healing_orchestrator.py `
  --file wicked_zerg_bot_pro.py `
  --model gemini-1.5-pro-002 `
  --full-context
```

### Flash 모델 (빠르고 저렴)

```powershell
python self_healing_orchestrator.py `
  --file economy_manager.py `
  --model gemini-1.5-flash-002
```

### 게임 없이 코드 검증만

```powershell
python self_healing_orchestrator.py `
  --file production_manager.py `
  --full-context `
  --no-game
```

---

## ? 비용 (매우 저렴!)

### Pro 모델
- 일반적인 사용: **$0.01-$0.05 per execution**
- 월 예상: **~$50** (500회 실행)

### Flash 모델
- 매우 저렴: **$0.001-$0.01 per execution**
- 월 예상: **~$5** (500회 실행)

---

## ? 문제 해결

### "GCP_PROJECT_ID not set"

```powershell
# 현재 프로젝트 확인
gcloud config get-value project

# 설정된 환경변수 확인
$env:GCP_PROJECT_ID

# 다시 설정
gcloud config set project your-project-id
[Environment]::SetEnvironmentVariable("GCP_PROJECT_ID", "your-project-id", "User")
```

### "Permission denied"

```powershell
# 인증 다시 설정
gcloud auth application-default login
```

### API 활성화 안됨

```powershell
# Vertex AI API 활성화
gcloud services enable aiplatform.googleapis.com
```

---

## ? 다음 단계

- [전체 설정 가이드](VERTEX_AI_SETUP.md) 읽기
- [모델 비교](VERTEX_AI_SETUP.md#모델-선택-가이드) 및 선택
- 자동 수정 루프 시작!

---

**준비 완료! ? Vertex AI로 StarCraft 2 AI 봇을 개선하세요!**
