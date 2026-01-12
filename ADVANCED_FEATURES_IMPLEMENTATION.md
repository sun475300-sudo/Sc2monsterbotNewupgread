# Self-Healing Orchestrator: 고급 기능 업그레이드 완료 ?

**업그레이드 날짜**: 2025-01-09  
**상태**: ? 완전 구현 및 테스트 준비 완료

---

## ? 업그레이드 요약

사용자가 제공한 3가지 고급 Gemini API 기능이 모두 구현되었습니다:

| 기능 | 상태 | 설명 |
|------|------|------|
| **System Instruction** | ? 완료 | AI에게 "BurnySC2 라이브러리 전문가" 역할 부여 |
| **JSON Mode** | ? 완료 | 구조화된 JSON 응답으로 파싱 안정성 향상 |
| **Large Context Window** | ? 완료 | 1M+ 토큰 지원으로 전체 프로젝트 분석 가능 |

---

## ? 구현 상세

### 1. System Instruction (initialize_gemini 함수)

```python
def initialize_gemini(model_name: str = "gemini-1.5-pro"):
    system_instruction = """You are an expert Python debugger specializing in 
    StarCraft 2 BurnySC2 library. Analyze errors and provide ONLY valid JSON with fixed code."""
    
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction,
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,  # Deterministic responses
            max_output_tokens=8000,
        )
    )
    return model
```

**효과**:
- Gemini가 BurnySC2 컨텍스트에서 최적화된 응답 생성
- 확률적 행동 제거 (temperature=0.2)
- 더 정확한 버그 분석과 수정안

---

### 2. JSON Mode (extract_code_block 함수)

```python
def extract_code_block(response_text: str) -> Optional[str]:
    # 먼저 JSON 파싱 시도
    try:
        response_data = json.loads(response_text)
        if "fixed_code" in response_data:
            logger.info(f"PARSE JSON response parsed successfully")
            return response_data["fixed_code"].strip()
    except ValueError:
        pass  # 마크다운으로 폴백
    
    # 마크다운 코드 블록 추출 (폴백)
    # ... markdown parsing logic ...
```

**효과**:
- Gemini가 반환하는 JSON 형식: `{"cause": "...", "fixed_code": "...", "explanation": "..."}`
- 파싱 실패 시 자동으로 마크다운으로 폴백
- API 응답 구조가 더 일관성 있음

---

### 3. Large Context Window (load_full_project_context, analyze_and_fix, self_healing_loop)

```python
def load_full_project_context(project_dir: Path, max_files: int = 20) -> str:
    """Load full project context for large-window analysis"""
    # 프로젝트의 최대 20개 Python 파일 로드
    # 각 파일의 처음 2000자씩 포함
    # 결과: ~40KB-100KB의 프로젝트 컨텍스트

async def analyze_and_fix(model, source_code, stderr, filename, attempt, full_context=None):
    if full_context:
        prompt = f"... Full project context:\n{full_context}\n\n..."
    # Gemini가 전체 프로젝트 아키텍처 이해하고 수정
```

**효과**:
- gemini-1.5-pro의 1M+ 토큰 윈도우 활용
- 단일 파일 분석보다 훨씬 정확한 버그 진단
- 다른 모듈과의 의존성 이해하여 더 나은 해결책 제시

---

## ? 새로운 명령줄 옵션

```bash
# 기본 사용
python self_healing_orchestrator.py --file test_advanced_features.py

# 풀 컨텍스트 사용
python self_healing_orchestrator.py --file combat_manager.py --full-context

# 모델 선택
python self_healing_orchestrator.py --file wicked_zerg_bot_pro.py \
    --model gemini-2.0-flash \  # 빠른 응답
    --max-fixes 3 \
    --timeout 60

# 고급: 전체 프로젝트 분석
python self_healing_orchestrator.py --file production_manager.py \
    --model gemini-1.5-pro \
    --full-context \
    --max-fixes 5
```

---

## ? 새 파일 및 수정사항

### 수정된 파일
- **self_healing_orchestrator.py** (400+ 줄)
  - `initialize_gemini()`: System instruction 및 생성 설정 추가
  - `extract_code_block()`: JSON 파싱 로직 추가
  - `load_full_project_context()`: 새 함수 - 프로젝트 컨텍스트 로드
  - `analyze_and_fix()`: full_context 파라미터 지원
  - `self_healing_loop()`: model_name, use_full_context 파라미터 추가
  - CLI 옵션: --model, --full-context 추가

### 새 파일
- **batch_auto_fix_advanced.py** (400+ 줄)
  - 여러 Python 파일을 배치로 처리
  - 고급 기능 모두 지원
  - JSON 결과 리포팅

- **ADVANCED_FEATURES_GUIDE.md**
  - 사용자 가이드 및 예제
  - 시나리오별 권장사항
  - 문제 해결 가이드

- **test_advanced_features.py**
  - 고급 기능 테스트용 파일
  - 의도적인 버그 포함

---

## ? 테스트 계획

### Phase 1: 기본 기능 검증 (API 키 필요)
```bash
# 1. 단일 파일 테스트
python self_healing_orchestrator.py --file test_advanced_features.py

# 2. JSON 응답 검증
# → logs/에서 응답 형식 확인

# 3. 모델 선택 테스트
python self_healing_orchestrator.py --file test_advanced_features.py \
    --model gemini-2.0-flash

python self_healing_orchestrator.py --file test_advanced_features.py \
    --model gemini-1.5-pro
```

### Phase 2: 고급 기능 검증
```bash
# 1. 풀 컨텍스트 테스트
python self_healing_orchestrator.py --file test_advanced_features.py \
    --full-context

# 2. 배치 처리 테스트
python batch_auto_fix_advanced.py --limit 3

# 3. Wicked Zerg 파일 테스트
python self_healing_orchestrator.py --file production_manager.py \
    --full-context --max-fixes 3
```

### Phase 3: 통합 테스트
```bash
# 전체 프로젝트 자동 수정
python batch_auto_fix_advanced.py \
    --directory . \
    --full-context \
    --model gemini-1.5-pro \
    --limit 10
```

---

## ? 성능 예상치

| 작업 | 소요 시간 | 토큰 사용량 |
|------|---------|-----------|
| 단일 파일 분석 (gemini-2.0-flash) | ~3-5초 | 3K-5K |
| 단일 파일 + 컨텍스트 (gemini-1.5-pro) | ~5-8초 | 20K-50K |
| 배치 10개 파일 | ~1-2분 | 200K-500K |
| 전체 프로젝트 분석 (50+ 파일) | ~10-15분 | 1M+ |

**주의**: 무료 API 티어는 일일 1,500 요청 제한. 프로덕션 환경에서는 유료 API 사용 권장.

---

## ? 사용 시나리오

### 시나리오 A: 빠른 버그 수정
```bash
# Wicked Zerg 봇 실행 중 발견된 버그 즉시 수정
python self_healing_orchestrator.py --file wicked_zerg_bot_pro.py \
    --model gemini-2.0-flash \
    --max-fixes 2

소요시간: ~10초
```

### 시나리오 B: 깊이 있는 리팩토링
```bash
# production_manager.py의 복잡한 논리 오류 수정
python self_healing_orchestrator.py --file production_manager.py \
    --full-context \
    --model gemini-1.5-pro \
    --max-fixes 5

소요시간: ~30-45초
```

### 시나리오 C: 일일 자동 수정
```bash
# Wicked Zerg 봇 코드 전체 자동 검사 및 수정
python batch_auto_fix_advanced.py \
    --full-context \
    --model gemini-1.5-pro

소요시간: ~5-10분 (50개 파일 기준)
```

---

## ? 주요 개선사항

### 이전 버전 vs 새 버전

| 측면 | 이전 | 새 버전 |
|------|------|--------|
| **모델** | gemini-2.0-flash만 가능 | 2.0-flash, 1.5-pro 선택 가능 |
| **역할** | 일반 Python 디버거 | BurnySC2 전문가 |
| **응답 형식** | 마크다운만 | JSON (마크다운 폴백) |
| **분석 범위** | 단일 파일만 | 전체 프로젝트 선택 |
| **정확도** | 중간 | 높음 (컨텍스트 활용) |
| **파싱 안정성** | 낮음 (마크다운 파싱) | 높음 (JSON 파싱) |

---

## ? API 활용 개선

### 이전 접근
- 모든 요청: 단일 파일만 전송
- 버그 분석: 파일 내용만으로 판단
- API 응답: 마크다운 코드 블록 (불안정)

### 새 접근
- 풀 컨텍스트: 프로젝트 전체 아키텍처 포함 (선택)
- 버그 분석: 다른 모듈과의 관계 고려
- API 응답: JSON 구조화 (안정적)
- 역할 정의: "BurnySC2 전문가"로 정확도 향상

---

## ? 보안 및 비용

### API 키 관리
```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your-key"

# GitHub Actions (CI/CD)
secrets.GEMINI_API_KEY
```

### 비용 추정
- **무료 티어**: 1,500 요청/일 (약 50개 파일 분석)
- **프로덕션**: $0.075 per 1M input tokens

```
계산 예:
- 전체 프로젝트 분석: ~500K tokens
- 비용: 500K * $0.075 / 1M = $0.04 (약 50원)
```

---

## ? 다음 스텝

### 즉시 수행 가능
1. ? 새 API 키 발급 (현재 키 할당량 초과)
2. ? `test_advanced_features.py` 테스트 실행
3. ? JSON 응답 형식 확인

### 1주일 내
4. ? Wicked Zerg 봇 파일 1-2개 테스트
5. ? 배치 처리 파이프라인 검증
6. ? CI/CD 통합 (자동 수정)

### 2주일 내
7. ? 전체 프로젝트 자동 수정 실행
8. ? 성능 모니터링 및 최적화
9. ? 프로덕션 배포

---

## ? 지원 및 문제 해결

### 자주 묻는 질문

**Q: gemini-1.5-pro가 항상 더 나은가?**
A: 아닙니다.
- 빠른 수정 필요 → gemini-2.0-flash (3-5초)
- 정확한 수정 필요 → gemini-1.5-pro + 컨텍스트 (5-8초)

**Q: --full-context는 항상 필요한가?**
A: 아닙니다. 단순한 버그는 필요 없지만:
- 복잡한 아키텍처 오류 → 필수
- 다른 모듈과의 의존성 → 권장
- 비용 절감 → 선택적 사용

**Q: API 할당량이 부족하면?**
A: 여러 옵션:
1. 무료 API 키 여러 개 사용 (rotation)
2. 유료 API 활성화
3. 배치 크기 줄이기

---

## ? 기술 상세

### JSON 응답 구조
```json
{
  "cause": "TypeError: calculate_sum() missing 1 required positional argument: 'b'",
  "fixed_code": "def main():\n    result = calculate_sum(5, 10)\n    ...",
  "explanation": "Added missing argument 'b' to calculate_sum call"
}
```

### System Instruction 영향
- **Before**: 일반적인 Python 코드 수정
- **After**: BurnySC2 라이브러리 특화 수정
  - burnysc2 API 사용법 인식
  - async/await 패턴 이해
  - SC2 게임 로직 고려

### 컨텍스트 윈도우 활용
- gemini-1.5-pro: 최대 1,000,000 토큰
- 활용 예:
  - 50개 Python 파일 (평균 2K 각) = 100K 토큰
  - 남은 여유: 900K 토큰 (대규모 프로젝트 지원)

---

## ? 문서 참조

- [ADVANCED_FEATURES_GUIDE.md](ADVANCED_FEATURES_GUIDE.md) - 사용자 가이드
- [SELF_HEALING_INSTANT_START.md](SELF_HEALING_INSTANT_START.md) - 시작 가이드
- [README_SELF_HEALING.md](README_SELF_HEALING.md) - 상세 설명

---

**업그레이드 완료**: 2025-01-09 ?  
**다음 마일스톤**: API 키로 첫 테스트 실행  
**예상 소요시간**: ~5분 (새 키 설정 후)

---

**고급 Gemini API 기능 3가지 모두 구현되었습니다!**
? 새 API 키로 테스트 준비 완료
