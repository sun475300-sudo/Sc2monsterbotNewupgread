# 📱 모바일에서 GitHub Codespaces + Cline으로 AI 개발하기

## 🎯 완벽한 조합: Codespaces + Cline + 모바일

이 가이드는 **스마트폰에서 AI 에이전트와 협업하여 코드를 자동으로 작성하고 수정하는 방법**을 알려드립니다.

---

## 🏆 왜 이 조합인가?

| 도구 | 역할 | 장점 |
|------|------|------|
| **GitHub Codespaces** | 클라우드 개발 환경 | 모바일에서 VS Code 전체 기능 사용 |
| **Cline** | AI 자율 에이전트 | 파일 생성/수정, 터미널 실행, 버그 수정 |
| **Wicked Cline Bot** | Vertex AI 통합 | 200만 토큰 컨텍스트, 프로 전략 주입 |

### ✅ 이 조합의 장점:
- 🌍 **어디서나 개발**: 스마트폰만 있으면 OK
- 🤖 **AI가 코딩**: 명령만 내리면 AI가 모든 작업 수행
- 💰 **무료 시작**: 월 120 코어 시간 무료
- 🔧 **완전한 환경**: 터미널, 디버거, Git 모두 사용 가능
- 🚀 **5분 설정**: 복잡한 설정 없이 바로 시작

---

## 🚀 5분 만에 시작하기 (모바일)

### Step 1: 저장소 생성
```
1. 모바일 브라우저에서 github.com 접속
2. 로그인 후 우측 상단 "+" 클릭
3. "New repository" 선택
4. 이름: ai-agent-test (또는 원하는 이름)
5. Public 선택
6. "Create repository" 클릭
```

### Step 2: Codespace 시작
```
1. 생성된 페이지에서 녹색 "Code" 버튼 클릭
2. "Codespaces" 탭 선택
3. "Create codespace on main" 클릭
4. 기다리면 브라우저에 VS Code 열림 (약 30초)
```

### Step 3: Cline 설치
```
1. 왼쪽 사이드바 확장(블록) 아이콘 클릭
2. 검색창에 "Cline" 입력
3. "Install" 클릭
4. 왼쪽 사이드바에 로봇 아이콘 생김
```

### Step 4: AI에게 명령하기
```
1. 로봇 아이콘 클릭
2. 채팅창에 명령 입력:
   "Python으로 간단한 웹 서버를 만들어줘. 
    Flask를 사용하고, / 경로에 접속하면 
    'Hello from AI!'를 보여주도록 해줘."
3. Enter 누르고 AI가 작업하는 걸 구경
```

---

## 💡 첫 미션 추천 (연구용)

### 미션 1: "AI야, 앱을 만들어줘"
```
채팅: 
"Python Flask로 TODO 앱을 만들어줘.
1. 할 일 추가 기능
2. 할 일 목록 보기
3. 완료 체크 기능
4. 간단한 HTML 프론트엔드
파일 구조부터 코드까지 전부 만들어줘."
```

### 미션 2: "AI야, 버그를 찾아서 고쳐줘"
```
채팅:
"방금 만든 코드를 실행해보고,
에러가 나면 자동으로 고쳐줘.
모든 의존성도 설치해줘."
```

### 미션 3: "AI야, 테스트를 작성해줘"
```
채팅:
"지금까지 만든 코드에 대한
단위 테스트를 작성하고 실행해서
모두 통과하는지 확인해줘."
```

### 미션 4: "AI야, 배포 준비를 해줘"
```
채팅:
"Docker로 컨테이너화하고,
README.md에 사용법을 작성하고,
requirements.txt도 만들어줘."
```

---

## 🎮 SC2 프로젝트에 적용하기

### 이 저장소를 Codespaces에서 열기

#### 방법 1: 웹에서 직접
```
1. 이 저장소 페이지로 이동
2. "Code" → "Codespaces" → "Create codespace"
3. Cline 설치
4. Wicked Cline Bot 활성화
```

#### 방법 2: URL 직접 접속
```
https://github.com/codespaces/new?repo=sun475300-sudo/sc2AIagent
```

### Codespaces에서 Wicked Cline Bot 사용하기

#### 1. 환경 변수 설정
Codespace 터미널에서:
```bash
# Secrets에 추가 (Codespaces Settings에서)
export GCP_PROJECT_ID="gen-lang-client-0209357933"
export GOOGLE_APPLICATION_CREDENTIALS="key.json"
export GEMINI_API_KEY="your_api_key"
```

#### 2. 봇 실행
```bash
python wicked_cline_bot.py --interactive
```

#### 3. 미션 예시
```
💬 You: production_manager.py를 분석하고 중복 건설 버그를 찾아서 고쳐줘

🤖 Bot: 
🛠️ [1] Tool: read_file({"filepath": "production_manager.py"})
📖 파일 읽기 완료

🛠️ [2] Tool: search_in_files({"pattern": "build.*build"})
🔍 중복 건설 패턴 발견

🛠️ [3] Tool: write_file({...})
✅ 버그 수정 완료

🛠️ [4] Tool: run_terminal({"command": "python -m pytest"})
✅ 모든 테스트 통과

완료! 중복 건설 버그를 수정했습니다.
```

---

## 🔧 Codespaces 최적화 설정

### .devcontainer/devcontainer.json 추가
이 파일을 저장소에 추가하면 Codespace가 자동으로 설정됩니다:

```json
{
  "name": "SC2 AI Agent Development",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "github.copilot",
        "saoudrizwan.claude-dev",
        "continue.continue"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "terminal.integrated.defaultProfile.linux": "bash"
      }
    }
  },
  "forwardPorts": [5000, 8000],
  "portsAttributes": {
    "5000": {
      "label": "Backend API",
      "onAutoForward": "notify"
    },
    "8000": {
      "label": "Mobile Dashboard",
      "onAutoForward": "openBrowser"
    }
  }
}
```

---

## 📱 모바일 사용 팁

### 1. 화면 최적화
```
- 가로 모드 사용
- 사이드바 자동 숨김 활성화
- 미니맵 비활성화
- 터미널 최소 높이 설정
```

### 2. 터치 제스처
```
- 두 손가락 스와이프: 스크롤
- 핀치: 확대/축소
- 길게 누르기: 컨텍스트 메뉴
- 세 손가락 탭: 명령 팔레트
```

### 3. 키보드 사용
```
- 블루투스 키보드 연결 권장
- 가상 키보드: 자동 숨김 설정
- 단축키: Ctrl+Shift+P (명령 팔레트)
```

### 4. 배터리 절약
```
- 필요 없는 확장 비활성화
- 자동 저장 간격 늘리기
- 사용 안 할 때 Codespace 일시정지
```

---

## 💰 비용 관리

### 무료 플랜 (개인 계정)
- ✅ 월 120 코어 시간 무료
- ✅ 15GB 스토리지
- ✅ 2-core 머신: 월 60시간

### 비용 절약 팁
```
1. 사용 안 할 때 Codespace 정지
2. 자동 정지 시간 설정 (30분 추천)
3. 불필요한 Codespace 삭제
4. 2-core 머신 사용 (무료 충분)
```

### 사용 시간 확인
```
Settings → Billing → Codespaces
```

---

## 🆚 Cline vs Wicked Cline Bot

| 기능 | Cline (VS Code) | Wicked Cline Bot (Python) |
|------|-----------------|---------------------------|
| **UI** | VS Code 통합 | 터미널/API |
| **모델** | Claude/Anthropic | Gemini Vertex AI |
| **컨텍스트** | 200K tokens | **2M tokens** |
| **가격** | Claude API 필요 | Vertex AI 무료 |
| **사용법** | GUI 클릭 | 명령어/스크립트 |
| **자동화** | 수동 승인 | 완전 자동 |

### 추천 사용법
```
1. Cline (VS Code): 대화형 개발, 탐색
2. Wicked Cline Bot: 자동화, 배치 처리, CI/CD
```

---

## 🔄 워크플로우 예시

### 시나리오: "모바일에서 버그 수정하기"

#### 1. 모바일 대시보드에서 버그 발견
```
http://<codespace-url>:8000
→ 버그 발견: "중복 건설 발생"
```

#### 2. Codespaces 열기
```
모바일 브라우저 → GitHub → Codespaces → Open
```

#### 3. Cline으로 빠른 수정
```
Cline 채팅:
"production_manager.py에서 중복 건설 버그를 찾아서 고쳐줘"
```

#### 4. 또는 Wicked Cline Bot으로 자동 수정
```bash
python wicked_cline_bot.py --mission "Fix duplicate construction bug in production_manager.py"
```

#### 5. 테스트 및 커밋
```
Cline: "테스트를 실행하고 통과하면 커밋해줘"
```

#### 6. 모바일 대시보드에서 확인
```
새로고침 → 버그 사라짐 확인
```

---

## 🎓 학습 리소스

### 공식 문서
- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)
- [Cline Documentation](https://github.com/cline/cline)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)

### 비디오 튜토리얼
- [Codespaces 시작하기 (YouTube)](https://www.youtube.com/results?search_query=github+codespaces+tutorial)
- [Cline 사용법 (YouTube)](https://www.youtube.com/results?search_query=cline+vscode)

### 커뮤니티
- [GitHub Discussions](https://github.com/github/feedback/discussions/categories/codespaces-feedback)
- [Cline Discord](https://discord.gg/cline)

---

## 🐛 문제 해결

### Codespace가 느림
```
- 더 강력한 머신 선택 (4-core)
- 확장 프로그램 줄이기
- 브라우저 캐시 삭제
```

### Cline이 응답 없음
```
- API 키 확인
- 네트워크 연결 확인
- VS Code 재시작
```

### 포트 포워딩 안 됨
```
- Ports 탭에서 수동 추가
- Public으로 변경
- 방화벽 설정 확인
```

---

## 🚀 다음 단계

### 연구 프로젝트 아이디어
1. **AI 페어 프로그래밍**: AI와 함께 앱 만들기
2. **자동 버그 수정**: 코드에 버그 주입 후 AI가 찾아 고치는지 테스트
3. **코드 리팩토링**: 레거시 코드를 AI가 개선하도록 시키기
4. **테스트 생성**: 코드 작성 후 AI가 테스트 자동 생성
5. **문서화**: AI가 코드 분석 후 문서 자동 생성

### 고급 사용
```python
# Wicked Cline Bot API 사용
from wicked_cline_bot import WickedClineBot

bot = WickedClineBot()

# 복잡한 미션 체인
missions = [
    "Scan all files for bugs",
    "Fix all bugs found",
    "Run tests",
    "If tests fail, fix and retry",
    "Generate report"
]

for mission in missions:
    response = bot.execute_mission(mission)
    print(f"✅ {mission}: {response[:100]}...")
```

---

## 💬 피드백

모바일에서 개발하면서 겪은 경험을 공유해주세요!

**"연구가 성공하면 알려주세요!"** 🎉

---

**Made with 📱 + 🤖 by Wicked Team**

**"Your mobile is your development machine now."** 🚀
