# Self-Healing Orchestrator: 고급 기능 가이드

## ? 새로운 기능

### 1. System Instruction (역할 기반 AI)
- AI에게 "StarCraft 2 BurnySC2 전문가" 역할을 부여
- 더 정확하고 관련성 높은 버그 분석 및 수정 제안

### 2. JSON Mode (구조화된 응답)
- Gemini가 JSON 형식으로 응답 반환
- 파싱이 용이하고 안정적
- 마크다운 코드 블록으로의 자동 폴백 지원

### 3. Large Context Window (1M+ 토큰)
- gemini-1.5-pro 모델로 전체 프로젝트 컨텍스트 전달 가능
- 더 정확한 버그 수정과 아키텍처 이해
- 단일 파일 분석보다 수십 배 강력

---

## ? 사용 방법

### 기본 사용 (단일 파일 분석)
```bash
python self_healing_orchestrator.py --file test_advanced_features.py
```

### 풀 컨텍스트 분석 (전체 프로젝트 포함)
```bash
python self_healing_orchestrator.py --file test_advanced_features.py --full-context
```

### 모델 선택 (빠른 수정 vs 깊은 분석)
```bash
# 빠른 수정 (gemini-2.0-flash)
python self_healing_orchestrator.py --file test_advanced_features.py --model gemini-2.0-flash

# 깊은 분석 (gemini-1.5-pro, 기본값)
python self_healing_orchestrator.py --file test_advanced_features.py --model gemini-1.5-pro --full-context
```

### 최대 수정 시도 횟수 조정
```bash
python self_healing_orchestrator.py --file test_advanced_features.py --max-fixes 3
```

### 실행 타임아웃 설정
```bash
python self_healing_orchestrator.py --file test_advanced_features.py --timeout 60
```

---

## ? 명령어 옵션 상세 설명

| 옵션 | 단축형 | 설명 | 기본값 |
|------|-------|------|-------|
| `--file` | `-f` | 수정할 Python 파일 (필수) | - |
| `--max-fixes` | `-m` | 최대 수정 시도 횟수 | 5 |
| `--timeout` | `-t` | 코드 실행 타임아웃 (초) | 30 |
| `--full-context` | - | 전체 프로젝트 컨텍스트 포함 | False |
| `--model` | - | 사용할 Gemini 모델 | gemini-1.5-pro |

---

## ? 추천 사용 시나리오

### 시나리오 1: 빠른 버그 수정
```bash
# Wicked Zerg 봇의 단순한 오류 빠르게 수정
python self_healing_orchestrator.py --file wicked_zerg_bot_pro.py --model gemini-2.0-flash --max-fixes 3
```

### 시나리오 2: 아키텍처 이해하며 수정
```bash
# 전체 프로젝트 컨텍스트를 활용한 심층 분석
python self_healing_orchestrator.py --file combat_manager.py --full-context --model gemini-1.5-pro
```

### 시나리오 3: 배치 자동 수정
```bash
# 여러 파일을 순차적으로 수정
for file in *.py; do
    python self_healing_orchestrator.py --file "$file" --full-context
done
```

---

## ? 고급 설정

### API 키 설정
```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your-key-here"

# Windows CMD
set GEMINI_API_KEY=your-key-here

# Linux/Mac
export GEMINI_API_KEY=your-key-here
```

### 로깅 레벨
프로그램이 자동으로 `self_healing_logs/` 디렉토리에 상세 로그 저장

---

## ? 성능 비교

| 모델 | 처리 속도 | 컨텍스트 | 분석 품질 |
|------|---------|--------|---------|
| gemini-2.0-flash | ??? 빠름 | 제한됨 | 중간 |
| gemini-1.5-pro | ?? 보통 | 1M+ 토큰 | 높음 |

---

## ? 예상 동작

### 성공 케이스
```
START Auto-fix loop starting
   File: test_advanced_features.py
   Max attempts: 5
   Timeout: 30s
   Model: gemini-1.5-pro
   Context: Full project (45320 chars)
================================================
[Attempt 1/5]
ERROR Detected:
TypeError: calculate_sum() missing 1 required positional argument: 'b'

ANALYZE Sending to Gemini for analysis...
SUCCESS Fixed code received (JSON format)
BACKUP Created backup: test_advanced_features.py.bak_20260109_141234

[Attempt 2/5]
SUCCESS Code executed successfully!
SUCCESS Completed! Time: 12.3s
```

### API 배액 초과 시
```
WARNING Gemini API rate limited (429 error)
WARNING Retrying after 22.71 seconds...
WARNING Retrying after 15.43 seconds...
ERROR Max attempts reached
REPORT Saved: self_healing_logs/report_20260109_141234.json
```

---

## ? 체크리스트

- [ ] GEMINI_API_KEY 환경 변수 설정됨
- [ ] google-generativeai 패키지 설치됨 (`pip install google-generativeai`)
- [ ] loguru 패키지 설치됨 (`pip install loguru`)
- [ ] self_healing_orchestrator.py가 현재 디렉토리에 있음
- [ ] 수정할 Python 파일이 존재함

---

## ? 문제 해결

### "GEMINI_API_KEY is not set"
```bash
# API 키 설정하기
$env:GEMINI_API_KEY = "AIzaSy..."
```

### "ModuleNotFoundError: No module named 'google'"
```bash
# 필수 패키지 설치
pip install google-generativeai loguru
```

### API 할당량 초과 (429 error)
- 무료 티어: 일일 1,500개 요청 제한
- 새 API 키 생성하거나 쿼터 증량 요청

---

## ? 작동 원리

```
1. 파일 실행
   ↓
2. 오류 감지 (stderr 캡처)
   ↓
3. Gemini API에 전송 (System Instruction 포함)
   ↓
4. JSON 응답 파싱
   ↓
5. 자동 백업 후 코드 수정
   ↓
6. 재실행 (최대 5회 반복)
```

---

## ? 다음 단계

1. **API 키 확인** → 실제 키로 테스트
2. **단일 파일 테스트** → `test_advanced_features.py` 실행
3. **Wicked Zerg 통합** → 실제 봇 파일에 적용
4. **배치 처리** → 여러 파일 자동 수정

---

마지막 업데이트: 2025-01-09
Advanced Gemini Features: System Instructions, JSON Mode, Large Context Window
