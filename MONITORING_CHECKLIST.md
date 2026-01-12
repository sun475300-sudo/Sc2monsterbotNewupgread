# 모니터링 체크리스트

## ? 훈련 시작 전 체크

### 1. 환경 설정
- [ ] Python 3.9+ 설치 확인
- [ ] 필수 패키지 설치: `pip install -r requirements.txt`
- [ ] GEMINI_API_KEY 설정 (자동 수정 기능용)
- [ ] StarCraft 2 설치 확인

### 2. 파일 및 폴더
- [ ] `config.py` 검토 및 파라미터 설정
- [ ] `logs/` 폴더 접근 권한 확인
- [ ] `models/` 폴더에 이전 모델 확인
- [ ] `data/` 폴더 정리

### 3. 첫 실행
- [ ] `python main_integrated.py` 실행
- [ ] 초기 로그 메시지 확인
- [ ] 텔레메트리 파일 생성 확인

---

## ? 훈련 중 모니터링

### 매 10분마다 확인
- [ ] 게임이 정상적으로 진행 중인가?
- [ ] 로그 파일에 ERROR나 WARNING이 없는가?
- [ ] 프로세스의 CPU/메모리 사용량 정상인가?

### 매 시간마다 확인
- [ ] 텔레메트리 데이터가 계속 생성되는가?
  ```bash
  ls -la logs/
  tail -20 logs/training_log.log
  ```
- [ ] 훈련 진행도 확인
  ```bash
  cat logs/training_log.log | grep -i "episode\|win rate"
  ```
- [ ] 자동 수정 시스템 활성화 여부
  ```bash
  cat logs/training_log.log | grep -i "self_healing\|auto_fix"
  ```

### 매 일일마다 확인
- [ ] 텔레메트리 데이터 분석
  ```python
  import json
  with open('data/telemetry_0.json') as f:
      data = json.load(f)
  print(f"Total frames: {len(data)}")
  print(f"Average APM: {sum(d.get('apm', 0) for d in data) / len(data)}")
  ```
- [ ] 모델 체크포인트 생성 확인
  ```bash
  ls -la models/zerg_net*.pt
  ```
- [ ] 훈련 통계 확인
  ```bash
  cat logs/training_log.log | tail -100
  ```

---

## ? 이상 탐지

### 1. 게임이 응답 없음
**증상**: 로그가 업데이트되지 않음 (5분 이상)

**대응**:
```bash
# 프로세스 확인
Get-Process python | Where-Object {$_.Name -like "*main*"}

# 강제 종료 후 재시작
Stop-Process -Name python -Force
python main_integrated.py
```

### 2. 메모리 누수
**증상**: 메모리 사용량이 계속 증가

**대응**:
```python
# main_integrated.py에서 메모리 프로파일링
import psutil
print(f"Memory: {psutil.Process().memory_info().rss / 1024 / 1024:.1f}MB")
```

### 3. 자동 수정 오류
**증상**: 
```
[ERROR] Self-healing failed: API error
```

**대응**:
1. `.env` 파일에서 GEMINI_API_KEY 확인
2. API 할당량 확인
3. `self_healing_orchestrator.py`의 DRY_RUN_MODE 활성화

### 4. 훈련이 수렴하지 않음
**증상**: Win rate이 증가하지 않음

**대응**:
1. `config.py`에서 학습률 조정
2. `curriculum_manager.py`에서 난이도 확인
3. 상대방 AI 변경
4. 모델 재초기화

---

## ? 성능 메트릭

### 주요 모니터링 지표

| 지표 | 정상 범위 | 확인 방법 |
|------|---------|---------|
| **APM** | 200-400 | `telemetry_*.json` 분석 |
| **Win Rate** | 증가 추세 | `logs/training_log.log` |
| **Memory** | < 4GB | `Get-Process python` |
| **CPU** | 60-80% | 작업 관리자 |
| **프레임율** | > 30 FPS | 게임 내 fps 디스플레이 |

### 데이터 분석 스크립트
```python
import json
from pathlib import Path

# 최신 텔레메트리 파일 로드
latest_telem = max(Path('data').glob('telemetry_*.json'))
with open(latest_telem) as f:
    data = json.load(f)

# 기본 통계
print(f"게임 길이: {len(data)} 프레임")
print(f"평균 미네랄: {sum(d['minerals'] for d in data) / len(data):.0f}")
print(f"평균 군대: {sum(d['army_size'] for d in data) / len(data):.0f}")
print(f"최종 결과: {data[-1]['game_result']}")
```

---

## ?? 모니터링 자동화

### Windows Task Scheduler로 주기적 체크
```batch
REM 매시간 로그 백업
schtasks /create /tn "Wicked Zerg Log Backup" /tr "powershell -Command (Get-Item logs/training_log.log).CopyTo('logs/training_log_$(date).log')" /sc hourly

REM 매일 데이터 분석
schtasks /create /tn "Wicked Zerg Stats" /tr "python analyze_stats.py" /sc daily /st 23:00
```

### Linux/WSL 크론 작업
```bash
# 매시간 로그 체크
0 * * * * tail -20 /path/to/logs/training_log.log | mail -s "Wicked Zerg Status" email@example.com

# 매일 백업
0 2 * * * cp /path/to/logs/training_log.log /path/to/logs/backup/training_log_$(date +%Y%m%d).log
```

---

## ? 로깅 커스터마이징

### 로그 레벨 설정 (config.py)
```python
# DEBUG: 모든 정보 (성능 저하)
LOG_LEVEL = "DEBUG"

# INFO: 중요 정보 (기본값)
LOG_LEVEL = "INFO"

# WARNING: 경고와 에러만
LOG_LEVEL = "WARNING"

# ERROR: 에러만
LOG_LEVEL = "ERROR"
```

### 커스텀 로그 포맷
텔레메트리에 추가 필드 포함:
```python
custom_metrics = {
    'iteration': self.iteration,
    'win_probability': self.win_prob,
    'resource_efficiency': self.minerals / self.supply_used,
    'tech_level': self.tech_tier
}
self.telemetry_logger.record_state(self.iteration, custom_metrics)
```

---

## ? 체크리스트 완료 후

### 1. 정상 작동 확인
- [ ] 텔레메트리 데이터 생성됨
- [ ] 로그 파일 업데이트됨
- [ ] 모델 저장됨

### 2. 백업
```bash
# 중요 파일 백업
cp models/zerg_net.pt models/zerg_net.pt.backup
cp logs/training_log.log logs/training_log.backup
```

### 3. 예상 시간
- 초기화: 2-5분
- 게임당: 5-15분
- 모니터링: 실시간

---

**마지막 업데이트**: 2026-01-12  
**작성자**: Wicked Zerg AI System
