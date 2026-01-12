# 📱 SC2 AI Agent Mobile Monitoring System

## 🎯 Overview

**모바일 환경에서 SC2 AI 에이전트를 실시간으로 모니터링하는 시스템**

SC2는 모바일에서 실행되지 않으므로, 이 시스템은 터미널 기반 디버깅 UI를 제공하여 에러, 버그, 오류를 실시간으로 명확하게 표시합니다.

### 핵심 기능

1. **🖥️ 눈이 편한 터미널 UI** - Rich library를 사용한 아름다운 디버깅 대시보드
2. **🔄 실시간 모니터링** - 로그, 에러, 경고를 실시간으로 추적
3. **🤖 자동 수정 시스템** - AI 기반 버그 자동 감지 및 수정
4. **📊 텔레메트리 대시보드** - 게임 상태 및 성능 지표 표시
5. **🔧 자동 재시작** - 문제 발견 시 자동으로 서비스 재시작

---

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│        Terminal Mobile Dashboard (Main Interface)           │
│                 - Eye-friendly UI                           │
│                 - Real-time error display                   │
│                 - Color-coded severity levels               │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│           Autonomous Mobile Monitor                         │
│        - Continuous error detection                         │
│        - AI-powered auto-fixing                             │
│        - Service health monitoring                          │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              Backend API Server                             │
│        - REST API endpoints                                 │
│        - WebSocket for real-time updates                    │
│        - Telemetry data serving                             │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│          SC2 AI Agent (Python)                              │
│        - realtime_code_monitor.py                           │
│        - telemetry_logger.py                                │
│        - Game execution and data collection                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 설치 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

주요 라이브러리:
- `flask` - Backend API 서버
- `flask-cors` - CORS 지원
- `flask-socketio` - WebSocket 지원
- `rich` - 터미널 UI 라이브러리
- `google-genai` - AI 기반 자동 수정
- `loguru` - 로깅

### 2. 환경 변수 설정

`.env` 파일을 생성하고 Gemini API 키를 추가:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🚀 사용 방법

### 방법 1: 터미널 대시보드 실행 (권장)

**눈이 편한 터미널 UI로 모든 디버깅 정보를 한눈에 확인:**

```bash
python terminal_mobile_dashboard.py
```

옵션:
```bash
# 커스텀 리프레시 속도 (기본값: 1초)
python terminal_mobile_dashboard.py --refresh 0.5
```

**대시보드 기능:**
- ✅ 실시간 에러 및 버그 표시 (심각도별 색상 구분)
- ✅ 경고 메시지 추적
- ✅ 라이브 로그 스트리밍
- ✅ 텔레메트리 데이터 표시
- ✅ 시스템 상태 모니터링
- ✅ 디버그 정보

**색상 코드:**
- 🔴 **빨강** - Critical/Error (심각한 오류)
- 🟡 **노랑** - Warning (경고)
- 🟢 **초록** - Success/Info (정상)
- 🔵 **파랑** - Debug (디버그 정보)
- 🟣 **보라** - Header (제목)

### 방법 2: 자동 수정 시스템 실행

**AI 기반 자동 버그 수정 및 지속적 모니터링:**

```bash
python autonomous_mobile_monitor.py
```

옵션:
```bash
# 특정 시간 동안만 실행 (초 단위)
python autonomous_mobile_monitor.py --duration 3600

# 무한 실행 (기본값)
python autonomous_mobile_monitor.py --duration 0
```

**자동 수정 프로세스:**
1. 🔍 에러 감지
2. 🤖 Gemini AI로 분석 및 수정 코드 생성
3. 💾 소스코드에 자동 적용
4. 🔄 서비스 재시작
5. ✅ 수정 검증
6. 🔁 반복

### 방법 3: Backend API만 실행

**REST API 및 WebSocket 서버만 실행:**

```bash
python mobile_backend_api.py --host 0.0.0.0 --port 5000
```

옵션:
```bash
# 디버그 모드로 실행
python mobile_backend_api.py --debug

# 커스텀 포트
python mobile_backend_api.py --port 8080
```

---

## 📡 API 엔드포인트

### REST API

#### 상태 확인
```http
GET /api/status
```

응답:
```json
{
  "api_version": "1.0.0",
  "status": "online",
  "game_state": {
    "status": "running",
    "connected": true,
    "last_update": "2024-01-09T23:00:00"
  }
}
```

#### 최신 텔레메트리
```http
GET /api/telemetry/latest
```

#### 텔레메트리 히스토리
```http
GET /api/telemetry/history?limit=100
```

#### 최신 로그
```http
GET /api/logs/latest?limit=50
```

#### 로그 스트리밍 (SSE)
```http
GET /api/logs/stream
```

#### 게임 상태
```http
GET /api/game-state
```

응답:
```json
{
  "success": true,
  "data": {
    "basic_info": {
      "time": 300,
      "iteration": 5000,
      "game_phase": "mid_game"
    },
    "resources": {
      "minerals": 500,
      "vespene": 300
    },
    "supply": {
      "used": 120,
      "cap": 200,
      "army": 80
    },
    "units": {
      "army_count": 40,
      "drone_count": 60,
      "queen_count": 4
    }
  }
}
```

#### 통계
```http
GET /api/stats
```

#### 자동 수정 내역
```http
GET /api/fixes/latest
```

#### 모니터링 시작/중지
```http
POST /api/monitoring/start
POST /api/monitoring/stop
```

### WebSocket Events

**연결:**
```javascript
const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Connected to monitoring service');
});
```

**이벤트:**
- `connection_response` - 연결 응답
- `telemetry_update` - 텔레메트리 업데이트
- `log_update` - 로그 업데이트

**요청:**
```javascript
// 텔레메트리 요청
socket.emit('request_telemetry');

// 로그 요청
socket.emit('request_logs', { limit: 10 });
```

---

## 🎨 터미널 UI 사용법

### 대시보드 레이아웃

```
╔══════════════════════════════════════════════════════════════╗
║   SC2 AI MOBILE MONITORING DASHBOARD - DEBUGGING MODE       ║
╚══════════════════════════════════════════════════════════════╝
⏱  Uptime: 00:05:30  │  🔧 Backend: Running ✓  │  🔄 Refresh: 1s

┌─────────────────────────────────┬─────────────────────────┐
│ 🐛 ERRORS & BUGS                │  📊 STATISTICS          │
│ (Last 10 errors)                │  🔴 Critical: 0         │
│                                 │  ❌ Errors: 2           │
│ [12:34:56] ERROR | backend     │  ⚠️  Warnings: 5        │
│ Connection timeout...           │  ✅ Fixes: 3            │
├─────────────────────────────────┼─────────────────────────┤
│ ⚠️  WARNINGS                     │  📊 TELEMETRY DATA      │
│ (Last 5 warnings)               │  Game Time: 300s        │
│                                 │  Minerals: 500          │
│ [12:35:01] WARNING | API       │  Vespene: 300           │
│ Slow response time...           │  Supply: 120/200        │
├─────────────────────────────────┼─────────────────────────┤
│ 📜 LIVE LOGS                    │  🔍 DEBUG INFO          │
│ (Real-time streaming)           │  Backend API: ✓ Running │
│                                 │  Log Directory: ✓ Found │
│ [12:35:05] Starting monitor...  │  Telemetry: ✓ Found     │
│ [12:35:06] Backend connected... │  Self-Healing: ✓ Active │
└─────────────────────────────────┴─────────────────────────┘
```

### 키보드 단축키

- `Ctrl+C` - 대시보드 종료
- 자동 리프레시 (설정된 간격마다)

### 에러 심각도 레벨

| 레벨 | 색상 | 설명 |
|------|------|------|
| **CRITICAL** | 🔴 빨강 | 치명적 오류 (프로그램 중단) |
| **ERROR** | ❌ 빨강 | 오류 (기능 실패) |
| **WARNING** | ⚠️ 노랑 | 경고 (잠재적 문제) |
| **INFO** | ℹ️ 파랑 | 정보 (정상 작동) |
| **SUCCESS** | ✅ 초록 | 성공 (작업 완료) |

---

## 🔧 자동 수정 시스템

### 작동 원리

1. **에러 감지**
   - 백엔드 프로세스 로그 모니터링
   - 로그 파일 실시간 스캔
   - 패턴 매칭으로 에러 분류

2. **AI 분석**
   - Gemini AI에 에러 컨텍스트 전송
   - 소스코드 분석
   - 수정 방법 생성

3. **자동 수정**
   - 원본 파일 백업
   - 수정된 코드 적용
   - 수정 로그 저장

4. **재시작 및 검증**
   - 서비스 재시작
   - 헬스 체크
   - 수정 검증

### 수정 로그

모든 자동 수정은 `autonomous_healing_logs/` 디렉토리에 저장:

```json
{
  "timestamp": "2024-01-09T23:00:00",
  "error": {
    "source": "backend",
    "error_type": "TypeError",
    "error_message": "..."
  },
  "fix": {
    "analysis": "Root cause analysis",
    "root_cause": "Missing error handling",
    "fix_description": "Added try-catch block",
    "fixed_code": "..."
  },
  "file": "mobile_backend_api.py",
  "backup": "mobile_backend_api.py.backup",
  "applied": true
}
```

---

## 📊 모니터링되는 지표

### 텔레메트리 데이터
- 게임 시간 (초)
- 자원 (미네랄/베스핀)
- 보급 (사용/최대/군대)
- 유닛 수 (일꾼/군대/여왕/라바)
- 적군 정보

### 시스템 메트릭
- 에러 카운트
- 경고 카운트
- 적용된 수정 횟수
- 재시작 횟수
- 가동 시간

### 로그 카테고리
- 백엔드 API 로그
- 모바일 앱 로그 (있는 경우)
- 시스템 헬스 로그
- 자동 수정 로그

---

## 🎯 사용 시나리오

### 시나리오 1: 개발 중 디버깅

```bash
# 터미널에서 대시보드 실행
python terminal_mobile_dashboard.py

# 다른 터미널에서 AI 에이전트 실행
python main_integrated.py
```

**결과:**
- 실시간 에러 표시
- 버그 발견 시 즉시 알림
- 게임 상태 모니터링

### 시나리오 2: 자율 모니터링

```bash
# 자동 수정 시스템 실행
python autonomous_mobile_monitor.py

# 백그라운드에서 계속 실행
# 에러 발견 → 자동 수정 → 재시작 → 반복
```

**결과:**
- 24/7 자동 모니터링
- 버그 자동 수정
- 무인 운영 가능

### 시나리오 3: API 통합 테스트

```bash
# API 서버만 실행
python mobile_backend_api.py --debug

# 다른 터미널에서 API 테스트
curl http://localhost:5000/api/status
curl http://localhost:5000/api/telemetry/latest
```

**결과:**
- API 엔드포인트 테스트
- 데이터 흐름 확인
- 통합 검증

---

## 🛠️ 문제 해결

### Backend API가 시작되지 않음

```bash
# 포트 충돌 확인
lsof -i :5000

# 다른 포트 사용
python mobile_backend_api.py --port 8080
```

### 텔레메트리 데이터가 없음

```bash
# 텔레메트리 파일 확인
ls -la telemetry_*.json

# AI 에이전트가 실행 중인지 확인
ps aux | grep python
```

### 자동 수정이 작동하지 않음

```bash
# GEMINI_API_KEY 확인
echo $GEMINI_API_KEY

# .env 파일 확인
cat .env
```

### 터미널 UI가 깨짐

```bash
# Rich 라이브러리 재설치
pip install --upgrade rich

# 터미널 크기 확인 (최소 80x24 권장)
stty size
```

---

## 📝 로그 파일

### 생성되는 로그 파일

- `logs/*.log` - 일반 로그 파일
- `telemetry_*.json` - 텔레메트리 데이터
- `telemetry_*.csv` - 텔레메트리 CSV
- `training_stats.json` - 훈련 통계
- `autonomous_healing_logs/fix_*.json` - 자동 수정 로그
- `*.backup` - 소스코드 백업

---

## 🔐 보안 고려사항

1. **API 키 보호**
   - `.env` 파일을 `.gitignore`에 추가
   - API 키 노출 방지

2. **CORS 설정**
   - 프로덕션에서는 특정 origin만 허용
   - 현재는 개발 편의를 위해 모든 origin 허용

3. **포트 보안**
   - 방화벽 설정
   - 외부 접근 제한

---

## 🚀 향후 개발 계획

- [ ] React Native 모바일 앱 개발
- [ ] 푸시 알림 기능
- [ ] 더 많은 시각화 차트
- [ ] 성능 프로파일링
- [ ] 멀티 인스턴스 모니터링
- [ ] 웹 대시보드
- [ ] 알림 설정 커스터마이징
- [ ] 히스토리 분석 도구

---

## 📚 참고 자료

- [Flask 문서](https://flask.palletsprojects.com/)
- [Flask-SocketIO 문서](https://flask-socketio.readthedocs.io/)
- [Rich 문서](https://rich.readthedocs.io/)
- [Google Gemini API](https://ai.google.dev/)

---

## 🤝 기여

버그 리포트, 기능 제안, 풀 리퀘스트 환영합니다!

---

## 📄 라이선스

이 프로젝트는 메인 프로젝트의 라이선스를 따릅니다.

---

**Happy Monitoring! 🎮📊**
