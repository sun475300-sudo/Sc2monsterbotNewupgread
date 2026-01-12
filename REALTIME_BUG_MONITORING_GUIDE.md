# 🐛 실시간 버그 모니터링 가이드
# Real-time Bug Monitoring Guide

## 📋 개요

이 시스템은 SC2 AI Agent (monsterbot) 코드베이스를 실시간으로 스캔하여 버그, 에러, 코드 냄새를 자동으로 감지하고 리포트합니다.

**주요 기능:**
- ✅ 실시간 코드 스캔
- ✅ 버그 자동 감지
- ✅ 심각도별 분류 (CRITICAL/HIGH/WARNING)
- ✅ 타입별 분류 (문법 에러, Import 에러, 비동기 에러 등)
- ✅ JSON 리포트 생성
- ✅ Watch 모드 (지속적 모니터링)

---

## 🚀 빠른 시작

### Windows
```bash
start_bug_monitor.bat
```

### Linux/Mac
```bash
chmod +x start_bug_monitor.sh
./start_bug_monitor.sh
```

### Python 직접 실행
```bash
# 단일 스캔
python realtime_bug_monitor.py --scan-only

# Watch 모드 (10초마다 스캔)
python realtime_bug_monitor.py --watch --interval 10

# 상세 리포트 (50개 버그 표시)
python realtime_bug_monitor.py --scan-only --limit 50

# JSON 리포트 생성
python realtime_bug_monitor.py --scan-only --output my_report.json
```

---

## 📊 현재 버그 상태 (최신 스캔 결과)

### 전체 요약
- **총 이슈**: 2,023개
- **Critical**: 0개 ✅
- **High**: 750개 ⚠️
- **Warning**: 1,273개 ⚠️

### 타입별 분류
1. **CODE_SMELL** (1,273개) - 코드 냄새
   - Debug print문
   - TODO/FIXME 주석
   - Wildcard import
   - Bare except clause

2. **ASYNC_ERROR** (557개) - 비동기 관련
   - async/await 사용 패턴
   - Coroutine 관련

3. **TYPE_ERROR** (78개) - 타입 에러
   - TypeError 패턴
   - AttributeError 패턴

4. **IMPORT_ERROR** (43개) - Import 관련
   - ImportError
   - ModuleNotFoundError

5. **VALUE_ERROR** (38개) - 값 에러
   - ValueError, KeyError, IndexError

6. **PROTOBUF_ERROR** (24개) - Protobuf 관련
   - Protobuf 버전 충돌 관련 코드

7. **SYNTAX_ERROR** (6개) - 문법 에러
   - SyntaxError, IndentationError

8. **NAME_ERROR** (4개) - 이름 에러
   - NameError, UnboundLocalError

---

## 📁 파일별 버그 분포 (Top 10)

1. **wicked_zerg_bot_pro.py** - 565개 ⚠️
2. **production_manager.py** - 225개 ⚠️
3. **economy_manager.py** - 173개 ⚠️
4. **main_integrated.py** - 162개 ⚠️
5. **parallel_train_integrated.py** - 95개
6. **zerg_net.py** - 73개
7. **combat_manager.py** - 61개
8. **verify_vertex_ai_setup.py** - 59개
9. **production_resilience.py** - 58개
10. **realtime_bug_monitor.py** - 55개

---

## 🎯 버그 감지 패턴

### 1. 문법 에러 (SYNTAX_ERROR)
- SyntaxError
- IndentationError
- TabError

### 2. Import 에러 (IMPORT_ERROR)
- ImportError
- ModuleNotFoundError
- 상대 import 문제

### 3. 이름 에러 (NAME_ERROR)
- NameError (미정의 변수/함수)
- UnboundLocalError (할당 전 참조)

### 4. 타입 에러 (TYPE_ERROR)
- TypeError
- AttributeError

### 5. 값 에러 (VALUE_ERROR)
- ValueError
- KeyError
- IndexError

### 6. 비동기 에러 (ASYNC_ERROR)
- await 사용 패턴
- async def 정의
- Coroutine 미대기

### 7. 코드 냄새 (CODE_SMELL)
- Debug print문
- TODO/FIXME 주석
- Wildcard import (`import *`)
- Bare except clause

### 8. Protobuf 에러 (PROTOBUF_ERROR)
- Protobuf 버전 충돌
- Descriptor 생성 에러

---

## 💡 사용 예시

### 예시 1: 실시간 모니터링
```bash
python realtime_bug_monitor.py --watch --interval 5
```
**출력:**
```
🔍 Scan #1 - 2026-01-10 00:11:55
============================================================
      🐛 Bug Scan Summary       
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Category             ┃ Count ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Total Issues         │  2023 │
│ Critical             │     0 │
│ High                 │   750 │
│ Warning              │  1273 │
└──────────────────────┴───────┘

#1 [HIGH] IMPORT_ERROR
   📁 production_manager.py:40
   💬 Import error
   📝 except ImportError:
...
⏰ Next scan in 5 seconds...
```

### 예시 2: 단일 스캔 + 리포트
```bash
python realtime_bug_monitor.py --scan-only --output today_bugs.json
```
**결과:** `today_bugs.json` 파일에 모든 버그 정보 저장

### 예시 3: 상세 버그 목록
```bash
python realtime_bug_monitor.py --scan-only --limit 50
```
**결과:** 심각도 순으로 정렬된 50개 버그 표시

---

## 🔧 커스터마이징

### 스캔 간격 변경
```bash
# 30초마다 스캔
python realtime_bug_monitor.py --watch --interval 30

# 1초마다 스캔 (빠른 개발용)
python realtime_bug_monitor.py --watch --interval 1
```

### 무시할 디렉토리 추가
`realtime_bug_monitor.py` 파일 수정:
```python
self.ignore_dirs = {
    ".git", "__pycache__", ".venv", "venv", "env",
    "node_modules", ".pytest_cache", ".mypy_cache",
    "build", "dist", ".eggs",
    "your_custom_dir"  # 추가
}
```

### 버그 패턴 추가
```python
self.bug_patterns = {
    "MY_CUSTOM_BUG": [
        (r"pattern1", "Description 1"),
        (r"pattern2", "Description 2"),
    ],
}
```

---

## 📈 워크플로우 예시

### 개발 중 실시간 모니터링
1. 터미널 1: 코드 작성/수정
2. 터미널 2: `python realtime_bug_monitor.py --watch --interval 10`
3. 코드 저장 시 자동으로 버그 감지

### 커밋 전 버그 체크
```bash
# 커밋 전 체크
python realtime_bug_monitor.py --scan-only

# 버그가 0개면 커밋 진행
git add .
git commit -m "Fix bugs"
```

### CI/CD 통합
```yaml
# GitHub Actions 예시
- name: Run Bug Monitor
  run: |
    python realtime_bug_monitor.py --scan-only --output bugs.json
    
- name: Upload Bug Report
  uses: actions/upload-artifact@v2
  with:
    name: bug-report
    path: bugs.json
```

---

## 🐛 알려진 이슈 및 해결책

### 이슈 1: Rich 라이브러리 없음
**증상:**
```
⚠️  Rich library not installed. Using basic output.
```

**해결:**
```bash
pip install rich
```

### 이슈 2: 너무 많은 CODE_SMELL 경고
**해결책:**
- CODE_SMELL은 Warning이므로 무시 가능
- 필요시 패턴에서 제거:
```python
# realtime_bug_monitor.py에서 주석 처리
# "CODE_SMELL": [...],
```

### 이슈 3: 스캔이 너무 느림
**해결책:**
- Import 체크 비활성화 (이미 주석 처리됨)
- 무시 디렉토리 추가
- 스캔 간격 늘리기

---

## 📚 JSON 리포트 구조

```json
{
  "scan_time": "2026-01-10T00:11:55.276426",
  "scan_count": 1,
  "summary": {
    "total": 2023,
    "critical": 0,
    "high": 750,
    "warning": 1273,
    "by_type": {...},
    "by_file": {...}
  },
  "bugs": [
    {
      "severity": "HIGH",
      "type": "IMPORT_ERROR",
      "file": "production_manager.py",
      "line": 40,
      "message": "Import error",
      "code": "except ImportError:"
    },
    ...
  ]
}
```

---

## 🎯 다음 단계

### 우선 수정 대상
1. **wicked_zerg_bot_pro.py** (565개 이슈)
   - 가장 많은 버그 포함
   - 핵심 봇 파일

2. **production_manager.py** (225개 이슈)
   - 생산 관리 핵심
   - 많은 비동기 관련 이슈

3. **economy_manager.py** (173개 이슈)
   - 경제 관리 핵심

### 자동 수정 가능한 버그
- Debug print문 → 제거 또는 logger로 변경
- TODO/FIXME → 이슈 트래커로 이동
- Wildcard import → 명시적 import로 변경

### 수동 검토 필요한 버그
- 비동기 에러 (ASYNC_ERROR)
- 타입 에러 (TYPE_ERROR)
- Import 에러 (IMPORT_ERROR)

---

## 🔗 관련 도구

### 다른 모니터링 시스템과 통합
```bash
# Wicked Cline Bot과 함께 사용
python wicked_cline_bot.py --mission "Fix bugs in production_manager.py"

# Hyperfast Inspector와 함께 사용
python hyperfast_code_inspector.py

# Mobile Dashboard에 연동
python mobile_backend_api.py
```

---

## 💬 FAQ

**Q: 버그가 너무 많아요!**
A: 대부분 CODE_SMELL (Warning)입니다. CRITICAL과 HIGH를 먼저 수정하세요.

**Q: 실시간 감지가 안 돼요!**
A: Watch 모드를 사용하세요: `--watch --interval 10`

**Q: 특정 파일만 스캔하고 싶어요!**
A: 현재는 전체 스캔만 지원합니다. 추후 업데이트 예정입니다.

**Q: 버그를 자동으로 수정할 수 있나요?**
A: 현재는 감지만 가능합니다. 자동 수정은 `wicked_cline_bot.py` 또는 `autonomous_mobile_monitor.py`를 사용하세요.

---

## 📞 지원

문제가 발생하면 다음을 확인하세요:
1. Python 버전: 3.9 이상
2. 필수 패키지: `pip install rich`
3. 버그 리포트: `bug_report.json` 확인

---

**마지막 업데이트:** 2026-01-10
**버전:** 1.0.0
**작성자:** Copilot AI

🎉 **Happy Bug Hunting!** 🐛🔍
