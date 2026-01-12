# ? 모니터링 기능 안내

## ? 모니터링 파일 위치

이 프로젝트의 모니터링 기능에 대한 완전한 가이드는 [monitoring/](monitoring/) 폴더에 있습니다.

### ? 폴더 구조
```
monitoring/
├── README.md                    # 모니터링 시스템 개요 및 사용법
├── MONITORING_CHECKLIST.md      # 상세한 체크리스트 및 트러블슈팅
└── monitoring_examples.py       # 실용적인 모니터링 코드 예제
```

---

## ? 빠른 시작

### 1?? 모니터링 기능 이해하기
```bash
# monitoring 폴더 README 읽기
cat monitoring/README.md
```

### 2?? 체크리스트 확인하기
```bash
# 훈련 시작 전 체크리스트
cat monitoring/MONITORING_CHECKLIST.md
```

### 3?? 모니터링 코드 실행
```bash
# 예제 실행
python monitoring/monitoring_examples.py

# 또는 특정 예제만 실행
python -c "from monitoring.monitoring_examples import example_1_load_and_analyze; example_1_load_and_analyze()"
```

---

## ? 핵심 모니터링 파일 (루트)

### 1. **telemetry_logger.py**
- 게임 텔레메트리 데이터 수집
- JSON/CSV 형식 저장
- 훈련 통계 기록

**사용법:**
```python
from telemetry_logger import TelemetryLogger

logger = TelemetryLogger(instance_id=0)
logger.record_state(iteration, game_state)
logger.save_data()
```

### 2. **self_healing_orchestrator.py**
- 실시간 오류 감지 및 자동 수정
- Gemini API 기반 코드 분석
- 게임 로그 모니터링

**사용법:**
```python
from self_healing_orchestrator import SelfHealingOrchestrator

orchestrator = SelfHealingOrchestrator()
orchestrator.check_and_fix_errors()
```

### 3. **config.py**
- AI 행동 파라미터 설정
- 디버그 플래그 관리
- 로깅 레벨 제어

---

## ? 모니터링 시작하기

### 기본 훈련 모니터링
```bash
# 1. 훈련 시작
python main_integrated.py

# 2. 다른 터미널에서 로그 모니터링
tail -f logs/training_log.log

# 3. 실시간 텔레메트리 확인
python monitoring/monitoring_examples.py
```

### 고급 모니터링
```python
# monitoring_examples.py 사용
from monitoring.monitoring_examples import MonitoringUtils

# 텔레메트리 분석
data = MonitoringUtils.load_telemetry('telemetry_0.json')
stats = MonitoringUtils.analyze_telemetry(data)

# CSV 내보내기
MonitoringUtils.export_to_csv(data, 'telemetry_0.csv')

# 로그 상태 확인
status = MonitoringUtils.check_log_status('logs/training_log.log')
print(f"에러: {status['error_count']}, 경고: {status['warning_count']}")
```

---

## ? 주요 메트릭

| 메트릭 | 설명 | 정상 범위 |
|--------|------|---------|
| **APM** | 분당 행동 수 | 200-400 |
| **Win Rate** | 승률 | 증가 추세 |
| **Memory** | 메모리 사용량 | < 4GB |
| **CPU** | CPU 사용률 | 60-80% |
| **Army Size** | 현재 군대 규모 | 증가 추세 |

---

## ? 커스터마이징

### 로그 레벨 변경 (config.py)
```python
LOG_LEVEL = "DEBUG"    # 모든 정보
LOG_LEVEL = "INFO"     # 중요 정보 (기본)
LOG_LEVEL = "WARNING"  # 경고만
LOG_LEVEL = "ERROR"    # 에러만
```

### 텔레메트리 필드 추가
```python
# telemetry_logger.py 수정
custom_metrics = {
    'iteration': self.iteration,
    'win_probability': self.win_prob,
    'resource_efficiency': self.minerals / self.supply_used
}
```

---

## ? FAQ

### Q: 텔레메트리 파일이 생성되지 않습니다
**A:** 
1. `logs/` 폴더 권한 확인
2. `telemetry_logger.py`가 초기화되었는지 확인
3. 디스크 공간 확인

### Q: 로그 파일이 너무 많습니다
**A:** 
1. `config.py`에서 `LOG_LEVEL = "WARNING"`으로 변경
2. 매니저의 로깅 주기를 조정 (e.g., `iteration % 100 == 0`)

### Q: 자동 수정이 작동하지 않습니다
**A:**
1. `.env` 파일에 `GEMINI_API_KEY` 설정 확인
2. `self_healing_orchestrator.py`의 `DRY_RUN_MODE` 설정 확인
3. API 할당량 확인

---

## ? 더 알아보기

자세한 정보는 다음 문서를 참조하세요:

- **전체 개요**: [monitoring/README.md](monitoring/README.md)
- **체크리스트**: [monitoring/MONITORING_CHECKLIST.md](monitoring/MONITORING_CHECKLIST.md)
- **코드 예제**: [monitoring/monitoring_examples.py](monitoring/monitoring_examples.py)
- **주 설정**: [config.py](config.py)

---

**마지막 업데이트:** 2026-01-12  
**상태:** ? 활성
