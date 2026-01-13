---
README.md

markdown
# 🛸 Swarm Control System in StarCraft II
### 멀티 에이전트 드론 군집 연구를 위한 지능형 통합 관제 시스템  
**From Simulation to Reality: Reinforcement Learning • Self-Healing DevOps • Mobile GCS**

---

## 📌 부모님을 위한 요약 설명

> 이 프로젝트는 “게임을 한다”는 것이 아니라,  
> **구글 DeepMind(AlphaStar)**와 **미국 공군(USAF AI Flight / VISTA X-62A)**가 실제로 사용하는 방식 그대로  
> 스타크래프트 II를 **드론 군집 제어(swarm control)** 실험 환경으로 활용한 연구입니다.
>
> 실제 드론을 50–200대 동시에 띄워 실험하려면 **수천만~수억 원**이 필요하지만  
> 시뮬레이션을 활용하면 **안전하고 비용 없이** 군집 알고리즘을 실험할 수 있습니다.
>
> 이 프로젝트를 통해  
> **AI 자율비행 · 군집제어 · 클라우드 자가수복 · 모바일 원격관제(C2)** 등  
> 방산기업·국방연구소가 요구하는 핵심 기술을  
> 스스로 설계하고 구현했습니다.

---

# 🏗 Architecture

아래 코드를 그대로 두면 GitHub에서 Mermaid 다이어그램으로 자동 렌더링됩니다.

```mermaid
graph TD
    subgraph "Edge Device (Simulation Server)"
        A[StarCraft II Engine] <--> B{Wicked Zerg AI Bot}
        B --> C[Economy / Production / Swarm Manager]
    end

    subgraph "Cloud Intelligence (Vertex AI)"
        D[Gemini 1.5 Pro API]
        B -- "Traceback & Source Code" --> D
        D -- "Self-Healing Patch" --> B
    end

    subgraph "Remote Monitoring (Mobile GCS)"
        E[Flask Dashboard Server]
        F[Android App - Mobile GCS]
        B -- "Real-time Telemetry" --> E
        E <--> F
    end
````

---

# 📖 프로젝트 개요

이 프로젝트는 단순한 게임 봇(Game Bot)이 아니라
**AI Agent + Self-Healing Cloud DevOps + Mobile GCS**가 유기적으로 연결된
**지능형 통합 관제(Intelligent Integrated Control) 시스템**입니다.

핵심 목적은:

* 드론 군집(swarm)을 시뮬레이션 기반으로 연구
* 강화학습 기반의 자율 의사결정 자동화
* 클라우드 기반 자가 치유(Self-Healing) DevOps 구축
* 모바일 기반 C2(Command & Control) 통합

즉, **실제 UAV 군집 제어의 축소판을 가상 환경에서 구현한 프로젝트**입니다.

---

# 🧬 Sim-to-Real (가상 → 현실 대응표)

스타크래프트 II는 단순 게임이 아니라,
실제 군집 드론 제어 알고리즘과 1:1로 대응되는 고난도 시뮬레이션입니다.

| 스타크래프트 II (Virtual)  | 실제 드론/군집 UAV (Real)        |
| -------------------- | -------------------------- |
| Fog of War (시야 제한)   | 센서 불확실성, 통신 음영 구간          |
| 200기 유닛 실시간 제어       | 20–200대 군집 드론 동시 지휘·충돌 회피  |
| 미네랄/가스 자원 최적화        | 배터리/임무 우선순위·탑재량 관리         |
| 산란못 중복 건설 방지 로직      | 중복 명령 방지(SSoT), 시스템 자원 무결성 |
| 즉각적 전술 전환 (공격/확장/방어) | 임무 스케줄링·동적 전술 재편           |

---

# 💡 핵심 기능

## 1) Swarm Reinforcement Learning (군집 강화학습)

* 200기 저그 유닛 → **드론 군집(Multi-Agent Swarm)** 모델링
* 전투력, 적군 규모, 테크, 확장 상태 등을 **10차원 벡터**로 표현
* 공격/방어/확장 전략 **자동 전환**
* 프로게이머 **이병렬(Rogue)** 리플레이 기반 **모방학습(IL)** 적용

---

## 2) Gen-AI Self-Healing DevOps (코드 자가 수복)

* Google **Vertex AI (Gemini)** 연동
* 에러(traceback) 감지 → 자동 전송 → AI 분석
* Gemini가 수정 코드 **자동 생성 → 자동 패치 → 자동 재시작**
* 운영자 개입 없이 24/7 무중단 학습 유지

---

## 3) Mobile Ground Control Station (모바일 관제국)

* Android GCS **직접 개발**
* 실시간 정보:

  * 미네랄/가스
  * 유닛 생산/전투 상황
  * 승률 그래프
  * CPU 온도/부하
* ngrok 기반 LTE/5G **안전한 원격 접속**
* 실제 UAV C2(Command & Control) 구조의 프로토타입

---

# 🛠 Engineering Troubleshooting (핵심 문제 해결 사례)

방산/자율주행 시스템에서 가장 중요하게 보는 능력입니다.

---

## ✔ 1) await 누락 → **생산 마비 / 병력 0 문제 해결**

### 문제

* 미네랄이 8,000 이상 쌓여도 병력 생산 **0**
* AI가 완전히 **Stall(정지)** 상태

### 원인

* `larva.train()` coroutine 생성
* **await 누락**으로 SC2 엔진에 명령 전달 실패

### 해결

* 전체 생산 루틴 async 구조 **재설계**
* await 누락 구간 전수 검사
* concurrency(동시성) 순서 정리

### 결과

* **생산 성능 400% 상승**
* 자원 8,000 → 병력 0 문제 **완전 해결**

---

## ✔ 2) Race Condition → “중복 건설” 0% 해결

### 문제

* 여러 매니저가 “산란못 없음” 판단 → 2~3개 중복 건물 생성

### 해결

* Frame-level **Construction Reservation Flag** 도입
* 건설 여부를 **SSoT(Single Source of Truth)**로 관리

### 결과

* **중복 건설률 0% 달성**

---

## ✔ 3) Minerals 8000 Overflow → “Flush 알고리즘”으로 해결

### 문제

* 미네랄만 폭증 → 가스 부족 → 고급 테크 중단

### 해결

* 미네랄 500 이상 시:
  **저글링 폭생산 모드(Emergency Flush Mode)** 활성화

### 결과

* 자원 순환율 상승
* 테크 빌드 정상화

---

# 📸 README 추천 이미지

다음 이미지를 README 하단에 첨부하면 설득력이 폭발적으로 증가함:

* 📱 모바일 GCS 관제 화면 (실시간 자원/승률)
* 🐜 Flush 알고리즘 적용 후 저글링 폭발 생산 장면
* 🤖 Gemini가 코드 패치한 diff 화면

---

# 🔧 기술 스택

* **Language:** Python 3.10
* **AI:** PyTorch, RL Policy Network, SC2 Replay Mining
* **Simulation:** StarCraft II API
* **DevOps:** Auto Training Pipeline, Vertex AI Self-Healing
* **GCS:** Flask Dashboard, Android App
* **Algorithm:** Potential Field Swarm Navigation, Async Concurrency Control

---

# 🎯 Career Roadmap

이 프로젝트는 아래 분야와 직접 연결됩니다:

* UAV/UGV **자율제어 시스템**
* 방산 무인체계 **군집 알고리즘**
* AI/ML Engineer (RL, Multi-Agent AI)
* DevOps/MLOps (Self-Healing Infra)
* 로봇/자율주행 C2(Command & Control)

---

# 🌐 English Version

영어 풀버전은 `README_en.md` 파일에서 확인 가능.

---

# 📬 Contact

**장선우 (Jang S. W.)**
Drone Application Engineering
Email: **[sun475300@naver.com](mailto:sun475300@naver.com)**
GitHub Repo: [https://github.com/sun475300-sudo/Swarm-Control-in-sc2bot](https://github.com/sun475300-sudo/Swarm-Control-in-sc2bot)

---

> 이 연구에서 쌓은 인공지능 제어·군집 운용 역량은
> 앞으로 **국방과학연구소(ADD) 또는 방산 대기업**에서 활용할 수 있는
> 저만의 강력한 무기가 될 것이라 믿습니다.
> 지금까지 응원해 주신 부모님께 이 프로젝트를 작은 결과물로 보여드립니다.

```


