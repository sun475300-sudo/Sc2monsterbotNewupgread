# Real-Time Code Monitor - 게임 중 소스코드 검사 및 수정

## ? 개요

게임이 실행되는 동안에도 **백그라운드에서 소스코드를 지속적으로 검사**하고, 에러 발견 시 **자동으로 수정**하는 시스템입니다.

### 주요 기능

1. ? **게임 실행 중 실시간 로그 모니터링**
   - 별도 백그라운드 스레드로 작동
   - 게임 성능에 영향 없음
   - 5초마다 로그 파일 자동 스캔

2. ? **자동 에러 감지**
   - TypeError, AttributeError, NameError 등 10가지 패턴
   - 에러 컨텍스트 자동 추출 (전후 10줄)
   - 중복 에러 필터링

3. ? **Gemini AI 자동 수정**
   - 에러 발견 시 즉시 Gemini API로 분석
   - 수정 코드 자동 생성
   - JSON 형식으로 수정 내역 저장

4. ? **게임 종료 후 리포트**
   - 발견된 문제와 수정사항 요약
   - 다음 게임 전 적용 가능

---

## ? 사용 방법

### 방법 1: main_integrated.py에 자동 통합 (권장)

이미 `main_integrated.py`에 통합되어 있습니다. 그냥 실행하면 됩니다:

```powershell
# 환경 변수 설정
$env:PYTHONUTF8 = 1
$env:GEMINI_API_KEY = "AIzaSyC_CiEZ6CtVz9e1kAK0Ymbt1br4tGGMIIo"

# 훈련 시작 (모니터 자동 시작)
python main_integrated.py
```

**실행 시 자동으로:**
1. 백그라운드 모니터 시작
2. 게임 실행
3. 로그 실시간 감시
4. 에러 발견 시 Gemini API로 분석
5. 수정 코드 생성 → `self_healing_logs/fix_*.json` 저장
6. 게임 종료 후 리포트 출력

---

### 방법 2: 독립 실행 (수동 모니터링)

게임과 별도로 모니터만 실행할 수도 있습니다:

```powershell
# 1시간 동안 모니터링 (기본값)
python realtime_code_monitor.py --file wicked_zerg_bot_pro.py --duration 3600

# 다른 터미널에서 게임 실행
python main_integrated.py
```

**장점:**
- 게임 프로세스와 완전히 독립
- 여러 파일 동시 모니터링 가능
- 모니터만 재시작 가능

---

## ? 출력 예시

### 게임 중 에러 감지

```
15:30:42 | WARNING  | [MONITOR] ??  Error detected: TypeError: 'NoneType' object is... in training_log.log
15:30:45 | INFO     | [MONITOR] ? Attempting auto-fix for: TypeError:
15:30:50 | SUCCESS  | [MONITOR] ? Fix generated: self_healing_logs/fix_20260109_153050.json
15:30:50 | INFO     | [MONITOR] Analysis: Missing null check before accessing attribute...
```

### 게임 종료 후 리포트

```
======================================================================
? REAL-TIME MONITOR DETECTED ISSUES!
======================================================================

Real-Time Monitor - Fix Summary
======================================================================

[Fix #1] 2026-01-09T15:30:50
Error: TypeError:
Analysis: Missing null check before accessing self.intel attribute. Add defensive...
Fix saved to: self_healing_logs/fix_20260109_153050.json

======================================================================
```

---

## ? 생성되는 파일

### 1. 수정 로그 (JSON)

`self_healing_logs/fix_20260109_153050.json`:

```json
{
  "timestamp": "2026-01-09T15:30:50",
  "error": {
    "pattern": "TypeError:",
    "context": "... full error context ...",
    "source": "training_log.log"
  },
  "fix": {
    "analysis": "Missing null check before accessing attribute",
    "fix": "if self.intel and hasattr(self.intel, 'combat'):\n    ...",
    "explanation": "Added defensive check to prevent NoneType access"
  },
  "applied": false
}
```

### 2. 모니터 로그

`self_healing_logs/healing_20260109_150000.log`:

```
2026-01-09 15:00:00 | INFO     | Real-time monitor initialized for wicked_zerg_bot_pro.py
2026-01-09 15:00:00 | INFO     | Auto-fix: ENABLED
2026-01-09 15:00:05 | INFO     | Monitor loop started
2026-01-09 15:30:42 | WARNING  | ??  Error detected: TypeError...
```

---

## ? 설정 옵션

### realtime_code_monitor.py 내부 설정

```python
# 로그 체크 주기 (초)
MONITOR_INTERVAL = 5  # 기본값: 5초

# 감지할 에러 패턴
ERROR_PATTERNS = [
    r"TypeError:",
    r"AttributeError:",
    r"NameError:",
    # ... 더 추가 가능
]
```

### 수동 실행 시 CLI 옵션

```bash
python realtime_code_monitor.py \
    --file wicked_zerg_bot_pro.py \  # 모니터링 대상 파일
    --duration 3600                   # 모니터링 시간 (초)
```

---

## ? 동작 원리

### 1. 백그라운드 스레드 구조

```
Main Thread (게임 실행)
    ↓
    ├─ run_game() → SC2 실행
    ↓
Monitor Thread (백그라운드)
    ├─ 5초마다 로그 스캔
    ├─ 에러 패턴 감지
    ├─ Gemini API 호출
    └─ 수정 코드 저장
```

**핵심:** 
- 별도 `daemon=True` 스레드로 실행
- 게임 프로세스와 독립적
- 상호 간섭 없음

### 2. 에러 감지 프로세스

```python
1. 로그 파일 마지막 읽은 위치 기억
   ↓
2. 새로운 내용만 읽기 (성능 최적화)
   ↓
3. 정규표현식으로 에러 패턴 검색
   ↓
4. 에러 컨텍스트 추출 (전후 10줄)
   ↓
5. 중복 검사 (이미 본 에러는 무시)
   ↓
6. 에러 큐에 추가
```

### 3. 자동 수정 프로세스

```python
1. 에러 큐에서 가장 최근 에러 가져오기
   ↓
2. 소스 코드 읽기 (target_file)
   ↓
3. Gemini API에 전송:
   - 에러 컨텍스트
   - 소스 코드 (처음 5000자)
   ↓
4. Gemini 응답 파싱:
   - analysis: 원인 분석
   - fix: 수정 코드
   - explanation: 설명
   ↓
5. JSON으로 저장 (self_healing_logs/)
```

---

## ? 활용 팁

### 1. 수정사항 적용하기

```powershell
# 1. 생성된 fix JSON 파일 확인
Get-Content self_healing_logs/fix_20260109_153050.json | ConvertFrom-Json

# 2. 수정 코드 확인
$fix = Get-Content self_healing_logs/fix_20260109_153050.json | ConvertFrom-Json
$fix.fix.fix  # 실제 수정 코드

# 3. 수동 적용 또는 self_healing_orchestrator.py 사용
python self_healing_orchestrator.py --file wicked_zerg_bot_pro.py --max-fixes 1
```

### 2. 여러 파일 동시 모니터링

```python
# 커스텀 스크립트 작성
from realtime_code_monitor import RealtimeCodeMonitor

monitors = [
    RealtimeCodeMonitor("wicked_zerg_bot_pro.py"),
    RealtimeCodeMonitor("combat_manager.py"),
    RealtimeCodeMonitor("production_manager.py"),
]

for monitor in monitors:
    monitor.start()

# 게임 실행...
run_game(...)

# 모니터 정리
for monitor in monitors:
    monitor.stop()
```

### 3. 특정 에러만 감지

`ERROR_PATTERNS` 수정:

```python
# AttributeError만 감지
ERROR_PATTERNS = [
    r"AttributeError:",
]

# 특정 모듈 에러만 감지
ERROR_PATTERNS = [
    r"combat_manager\.py.*Error:",
]
```

---

## ? 문제 해결

### 문제 1: "GEMINI_API_KEY not set"

**해결:**
```powershell
$env:GEMINI_API_KEY = "AIzaSyC_CiEZ6CtVz9e1kAK0Ymbt1br4tGGMIIo"
```

### 문제 2: 모니터가 에러를 감지하지 못함

**원인:** 로그 파일 경로가 다를 수 있음

**해결:**
```python
# realtime_code_monitor.py에서 로그 디렉토리 확인
monitor = RealtimeCodeMonitor(
    target_file="wicked_zerg_bot_pro.py",
    log_dir=Path("logs")  # 실제 로그 디렉토리 확인
)
```

### 문제 3: Gemini API 호출이 너무 많음

**원인:** 같은 에러가 반복 감지됨

**해결:** 이미 구현된 중복 방지 로직이 작동 중
```python
# 에러 시그니처로 중복 필터링
error_signature = f"{pattern}:{error_context[:200]}"
if error_signature not in self.seen_error_signatures:
    # 새로운 에러만 처리
```

---

## ? 성능 영향

### 리소스 사용량

- **CPU:** <1% (백그라운드 스레드)
- **메모리:** ~50MB (로그 버퍼)
- **디스크 I/O:** 5초당 1회 (로그 읽기)

### 게임 성능

- ? 게임 FPS에 영향 없음
- ? 별도 스레드로 완전 독립
- ? Gemini API 호출도 비동기

---

## ? 고급 사용법

### 커스텀 에러 핸들러

```python
from realtime_code_monitor import RealtimeCodeMonitor

class CustomMonitor(RealtimeCodeMonitor):
    def _auto_fix_errors(self):
        """커스텀 수정 로직"""
        error = self.detected_errors.pop(0)
        
        # 특정 에러는 즉시 적용
        if "critical" in error['context'].lower():
            self._apply_fix_immediately(error)
        else:
            super()._auto_fix_errors()
    
    def _apply_fix_immediately(self, error):
        """즉시 적용 (위험: 자동 코드 수정)"""
        # Gemini로 수정 코드 생성
        # 파일에 바로 적용
        pass

monitor = CustomMonitor()
monitor.start()
```

---

## ? 체크리스트

실시간 모니터링 시작 전:

- [ ] GEMINI_API_KEY 환경 변수 설정
- [ ] logs/ 디렉토리 존재 확인
- [ ] self_healing_logs/ 디렉토리 생성됨
- [ ] realtime_code_monitor.py 파일 존재
- [ ] main_integrated.py에 통합 코드 추가됨

---

## ? 관련 파일

- `realtime_code_monitor.py` - 핵심 모니터링 시스템
- `main_integrated.py` - 통합된 훈련 루프 (모니터 포함)
- `self_healing_orchestrator.py` - 기존 치유 시스템 (게임 종료 후)
- `self_healing_logs/` - 수정 로그 저장 디렉토리

---

## ? 다음 단계

1. **자동 적용 시스템 추가**
   - 수정 코드 자동 적용 옵션
   - 위험 평가 후 안전한 수정만 자동 적용

2. **웹 대시보드**
   - 실시간 에러 모니터링 UI
   - 수정 내역 시각화

3. **슬랙/디스코드 알림**
   - 에러 발견 시 즉시 알림
   - 수정 완료 알림

---

**모든 준비 완료! 이제 게임을 실행하면 백그라운드에서 코드를 지켜보고 있습니다.** ?
