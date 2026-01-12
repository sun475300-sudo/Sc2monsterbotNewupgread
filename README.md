# 모니터링 시스템 가이드

## ? 모니터링 기능 개요

Wicked Zerg AI의 훈련 및 실행 상태를 모니터링하는 시스템 문서입니다.

## ? 모니터링 기능이 있는 파일

### 1. **telemetry_logger.py** (루트)
- **위치**: `d:\wicked_zerg_challenger\telemetry_logger.py`
- **기능**: 
  - 게임 내 텔레메트리 데이터 수집 (매 100프레임)
  - 훈련 통계 기록
  - JSON 형식으로 데이터 저장
  - CSV 형식 내보내기
- **사용 예시**:
  ```python
  from telemetry_logger import TelemetryLogger
  logger = TelemetryLogger(instance_id=0)
  logger.record_state(iteration, game_state)
  logger.save_data()
  ```
- **출력 파일**: `telemetry_*.json`, `telemetry_*.csv`

### 2. **self_healing_orchestrator.py** (루트)
- **위치**: `d:\wicked_zerg_challenger\self_healing_orchestrator.py`
- **기능**:
  - 실시간 오류 감지 및 자동 수정
  - Gemini API를 통한 코드 분석
  - DRY_RUN_MODE로 코드 검증
  - 게임 로그 모니터링
- **사용 예시**:
  ```python
  from self_healing_orchestrator import SelfHealingOrchestrator
  orchestrator = SelfHealingOrchestrator()
  orchestrator.check_and_fix_errors()
  ```

### 3. **config.py** (루트)
- **위치**: `d:\wicked_zerg_challenger\config.py`
- **기능**:
  - AI 행동 파라미터 설정
  - 디버그 플래그 관리
  - 로깅 레벨 설정
  - 게임 상수 정의
- **주요 설정**:
  - `DEBUG = True/False`
  - `LOG_LEVEL = "INFO"/"DEBUG"`

### 4. **각 매니저 모듈**의 내장 모니터링
매니저들은 내부에 로깅 기능을 가지고 있습니다:

- **economy_manager.py**
  - 자원 변화 추적
  - 확장 진행 상황 모니터링
  
- **production_manager.py**
  - 유닛 생산 현황
  - 애벌레 사용량 추적
  
- **combat_manager.py**
  - 전투 손실률 계산
  - 군대 구성 분석
  
- **intel_manager.py**
  - 적군 정보 업데이트
  - 맵 시야 추적
  
- **scouting_system.py**
  - 정찰 활동 기록
  - 위협 평가 데이터

## ? 폴더 구조

```
monitoring/
├── README.md (이 파일)
├── MONITORING_CHECKLIST.md
└── monitoring_examples.py
```

## ? 모니터링 시작

### 1. 텔레메트리 모니터링
```bash
# main_integrated.py 실행 시 자동으로 생성됨
python main_integrated.py

# 생성된 데이터 확인
ls telemetry_*.json
```

### 2. 훈련 로그 확인
```bash
# logs 폴더의 최신 로그 확인
cat logs/training_log.log | tail -50
```

### 3. 자동 수정 활성화
```bash
# .env 파일에 GEMINI_API_KEY 설정
export GEMINI_API_KEY="your-api-key"

# 자동 수정 활성화
python main_integrated.py  # 오류 발생 시 자동으로 시도
```

## ? 모니터링 데이터 분석

### 텔레메트리 데이터 필드
- `iteration`: 게임 프레임 번호
- `minerals`: 현재 미네랄
- `vespene`: 현재 가스
- `supply_used`: 사용 중인 인구
- `supply_cap`: 최대 인구
- `army_size`: 군대 크기
- `worker_count`: 일꾼 수
- `building_count`: 건물 수
- `enemy_detected`: 적 발견 여부
- `game_result`: 게임 결과 (승리/패배/진행중)

### 데이터 시각화
```python
import json
import pandas as pd

# 텔레메트리 데이터 로드
with open('telemetry_0.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(df[['iteration', 'minerals', 'vespene', 'army_size']])
```

## ?? 커스텀 모니터링

### 커스텀 메트릭 추가
`telemetry_logger.py`의 `record_state()` 메서드를 확장:

```python
def record_custom_metric(self, iteration, metric_name, value):
    self.telemetry_data.append({
        'iteration': iteration,
        'metric': metric_name,
        'value': value
    })
```

### 실시간 대시보드 연결
정적 파일 없이도 로그를 실시간 모니터링할 수 있습니다:

```bash
# Windows
tail -f logs/training_log.log

# Git Bash / WSL
tail -f logs/training_log.log | grep -i "error\|warning"
```

## ? 트러블슈팅

### 1. 텔레메트리 파일이 생성되지 않음
- `telemetry_logger.py`가 초기화되었는지 확인
- `logs/` 폴더의 권한 확인
- 디스크 공간 확인

### 2. 로그가 너무 많이 생성됨
- `config.py`에서 `LOG_LEVEL`을 "WARNING"으로 변경
- 매니저의 로깅 주기를 조정 (e.g., `iteration % 100 == 0`)

### 3. 자동 수정이 작동하지 않음
- Gemini API 키가 올바른지 확인
- `.env` 파일 확인
- `self_healing_orchestrator.py`의 DRY_RUN_MODE 설정 확인

## ? 모니터링 체크리스트

자세한 모니터링 항목은 [MONITORING_CHECKLIST.md](MONITORING_CHECKLIST.md) 참조

## ? 지원

문제가 발생하면:
1. 로그 파일 확인
2. 텔레메트리 데이터 분석
3. config.py 설정 검토
4. 자동 수정 시스템 활성화

---

**마지막 업데이트**: 2026-01-12  
**상태**: ? 활성
