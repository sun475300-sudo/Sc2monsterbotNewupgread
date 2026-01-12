# ? Quick Start Guide - Maximum Speed Training

## ? 최종 설정 완료 체크리스트

### 1. GPU 인식 확인 (필수)

터미널에서 실행:
```powershell
python check_gpu.py
```

**예상 출력 (GPU 인식 성공 시):**
```
======================================================================
GPU Detection Check
======================================================================
? PyTorch installed: 2.x.x+cu121
? CUDA available: True
? CUDA version: 12.1
? GPU count: 1
? GPU name: NVIDIA GeForce RTX 2060
? GPU memory: 6.00 GB

======================================================================
? SUCCESS: GPU is ready for training!
======================================================================
```

**GPU가 인식되지 않으면:**
```powershell
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
python check_gpu.py
```

---

### 2. 최대 속도 학습 시작

**방법 1: 배치 파일 사용 (권장)**
```powershell
.\start_parallel_max_speed.bat
```

**방법 2: 직접 실행**
```powershell
$env:SHOW_WINDOW='false'
python parallel_train_integrated.py
```

---

### 3. 학습 중 모니터링

**GPU 메모리 확인 (다른 터미널):**
```powershell
nvidia-smi -l 1
```

**예상 VRAM 사용량:**
- 인스턴스 1개: ~0.8GB
- RTX 2060 (6GB): 최대 4~5개 인스턴스 안전
- 시스템 예약: ~1.0GB

**인스턴스 수 조정:**
`start_parallel_max_speed.bat` 파일에서:
```batch
set NUM_INSTANCES=4  # 1에서 4로 변경 (RTX 2060 기준)
```

---

### 4. 학습 로그 확인

학습이 진행되면 다음 파일들이 생성됩니다:
- `logs/log_YYYYMMDD_HHMMSS.txt` - 게임 로그
- `data/training_stats.json` - 학습 통계
- `models/zerg_net_0.pt` - 학습된 모델

---

## ? 성능 최적화 확인

### ? 완료된 최적화:
- [x] `realtime=False` - 최대 속도 실행
- [x] `early_defense` 오타 수정
- [x] DeprecationWarning 해결
- [x] GPU 인식 준비 완료

### ? 예상 성능:
- **CPU 모드**: ~1x 속도
- **GPU 모드**: ~10x 속도 (CUDA 가속)
- **realtime=False**: CPU/GPU 최대 활용

---

## ?? 문제 해결

### GPU가 인식되지 않을 때:
1. NVIDIA 드라이버 최신 버전 확인
2. CUDA Toolkit 설치 확인
3. PyTorch CUDA 버전 재설치

### 학습이 너무 느릴 때:
1. `realtime=False` 확인 (로그에서 확인)
2. GPU 인식 확인 (`python check_gpu.py`)
3. 인스턴스 수 줄이기 (`NUM_INSTANCES=1`)

---

## ? 학습 진행 확인

학습이 정상적으로 진행되면:
- 로그에 `[GPU] GPU Available: ...` 표시
- `Performance: realtime=False (Maximum Speed)` 표시
- 게임이 빠르게 진행됨 (화면이 보이지 않음)

---

**모든 준비가 완료되었습니다! ?**

