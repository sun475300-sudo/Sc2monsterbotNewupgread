#!/usr/bin/env python3
"""
Wicked Zerg AI - 모니터링 예제 및 유틸리티

이 파일은 훈련 중 모니터링을 위한 실용적인 예제들을 제공합니다.
"""

import json
import csv
from pathlib import Path
from datetime import datetime
import statistics
from typing import Dict, List, Any


class MonitoringUtils:
    """모니터링 유틸리티 클래스"""
    
    @staticmethod
    def load_telemetry(telemetry_file: str) -> List[Dict[str, Any]]:
        """텔레메트리 파일 로드"""
        try:
            with open(telemetry_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] 텔레메트리 파일을 찾을 수 없음: {telemetry_file}")
            return []
    
    @staticmethod
    def analyze_telemetry(telemetry_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """텔레메트리 데이터 분석"""
        if not telemetry_data:
            return {}
        
        minerals = [d.get('minerals', 0) for d in telemetry_data]
        vespene = [d.get('vespene', 0) for d in telemetry_data]
        army_size = [d.get('army_size', 0) for d in telemetry_data]
        workers = [d.get('worker_count', 0) for d in telemetry_data]
        supply = [d.get('supply_used', 0) for d in telemetry_data]
        
        return {
            'total_frames': len(telemetry_data),
            'game_result': telemetry_data[-1].get('game_result', 'Unknown'),
            
            # 미네랄 통계
            'avg_minerals': statistics.mean(minerals),
            'max_minerals': max(minerals),
            'min_minerals': min(minerals),
            
            # 가스 통계
            'avg_vespene': statistics.mean(vespene),
            'max_vespene': max(vespene),
            'min_vespene': min(vespene),
            
            # 군대 통계
            'avg_army_size': statistics.mean(army_size),
            'max_army_size': max(army_size),
            'final_army_size': army_size[-1],
            
            # 일꾼 통계
            'avg_workers': statistics.mean(workers),
            'max_workers': max(workers),
            'final_workers': workers[-1],
            
            # 인구 통계
            'avg_supply_used': statistics.mean(supply),
            'max_supply_used': max(supply),
        }
    
    @staticmethod
    def export_to_csv(telemetry_data: List[Dict[str, Any]], output_file: str):
        """텔레메트리를 CSV로 내보내기"""
        if not telemetry_data:
            print("[ERROR] 내보낼 데이터가 없음")
            return
        
        keys = telemetry_data[0].keys()
        
        try:
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(telemetry_data)
            print(f"[SUCCESS] CSV 내보내기 완료: {output_file}")
        except Exception as e:
            print(f"[ERROR] CSV 내보내기 실패: {e}")
    
    @staticmethod
    def check_log_status(log_file: str) -> Dict[str, Any]:
        """로그 파일 상태 확인"""
        log_path = Path(log_file)
        
        if not log_path.exists():
            return {'status': 'not_found', 'message': f'로그 파일 없음: {log_file}'}
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            last_line = lines[-1] if lines else ''
            error_count = sum(1 for line in lines if 'ERROR' in line)
            warning_count = sum(1 for line in lines if 'WARNING' in line)
            
            return {
                'status': 'ok',
                'total_lines': len(lines),
                'error_count': error_count,
                'warning_count': warning_count,
                'last_update': log_path.stat().st_mtime,
                'last_line': last_line.strip()
            }
        except Exception as e:
            return {'status': 'error', 'message': f'로그 읽기 실패: {e}'}
    
    @staticmethod
    def get_recent_logs(log_file: str, lines: int = 20) -> List[str]:
        """최근 로그 라인 가져오기"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
            return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            return [f"[ERROR] 로그 읽기 실패: {e}"]


# ============================================================================
# 사용 예제
# ============================================================================

def example_1_load_and_analyze():
    """예제 1: 텔레메트리 로드 및 분석"""
    print("\n=== 예제 1: 텔레메트리 로드 및 분석 ===")
    
    telemetry_file = 'telemetry_0.json'
    data = MonitoringUtils.load_telemetry(telemetry_file)
    
    if data:
        stats = MonitoringUtils.analyze_telemetry(data)
        
        print(f"\n? 게임 통계")
        print(f"  총 프레임: {stats['total_frames']}")
        print(f"  게임 결과: {stats['game_result']}")
        
        print(f"\n? 자원")
        print(f"  평균 미네랄: {stats['avg_minerals']:.0f} (최대: {stats['max_minerals']})")
        print(f"  평균 가스: {stats['avg_vespene']:.0f} (최대: {stats['max_vespene']})")
        
        print(f"\n?? 군대")
        print(f"  평균 군대 크기: {stats['avg_army_size']:.0f}")
        print(f"  최종 군대 크기: {stats['final_army_size']}")
        
        print(f"\n? 일꾼")
        print(f"  평균 일꾼: {stats['avg_workers']:.0f}")
        print(f"  최종 일꾼: {stats['final_workers']}")


def example_2_export_csv():
    """예제 2: CSV로 내보내기"""
    print("\n=== 예제 2: CSV 내보내기 ===")
    
    telemetry_file = 'telemetry_0.json'
    data = MonitoringUtils.load_telemetry(telemetry_file)
    
    if data:
        output_file = 'telemetry_0.csv'
        MonitoringUtils.export_to_csv(data, output_file)


def example_3_check_logs():
    """예제 3: 로그 상태 확인"""
    print("\n=== 예제 3: 로그 상태 확인 ===")
    
    log_file = 'logs/training_log.log'
    status = MonitoringUtils.check_log_status(log_file)
    
    print(f"\n? 로그 상태: {status.get('status')}")
    if status['status'] == 'ok':
        print(f"  총 라인: {status['total_lines']}")
        print(f"  에러: {status['error_count']}")
        print(f"  경고: {status['warning_count']}")
        print(f"  마지막: {status['last_line']}")
    else:
        print(f"  메시지: {status.get('message')}")


def example_4_recent_logs():
    """예제 4: 최근 로그 표시"""
    print("\n=== 예제 4: 최근 로그 (마지막 10줄) ===")
    
    log_file = 'logs/training_log.log'
    recent = MonitoringUtils.get_recent_logs(log_file, lines=10)
    
    for line in recent:
        print(f"  {line.rstrip()}")


def example_5_continuous_monitoring():
    """예제 5: 지속적인 모니터링 (시뮬레이션)"""
    print("\n=== 예제 5: 지속적인 모니터링 ===")
    
    import time
    
    log_file = 'logs/training_log.log'
    telemetry_file = 'telemetry_0.json'
    
    print("\n[INFO] 모니터링 시작... (3초 간격으로 3번 체크)")
    
    for i in range(3):
        print(f"\n--- 체크 #{i+1} (시간: {datetime.now().strftime('%H:%M:%S')}) ---")
        
        # 로그 상태
        log_status = MonitoringUtils.check_log_status(log_file)
        if log_status['status'] == 'ok':
            print(f"? 로그: {log_status['total_lines']} 라인 (에러: {log_status['error_count']})")
        
        # 텔레메트리 분석
        telemetry = MonitoringUtils.load_telemetry(telemetry_file)
        if telemetry:
            stats = MonitoringUtils.analyze_telemetry(telemetry)
            print(f"? 자원: {stats['avg_minerals']:.0f} 미네랄, {stats['avg_vespene']:.0f} 가스")
            print(f"?? 군대: {stats['avg_army_size']:.0f}")
        
        if i < 2:
            time.sleep(3)
    
    print("\n[INFO] 모니터링 완료")


def example_6_performance_report():
    """예제 6: 성능 보고서 생성"""
    print("\n=== 예제 6: 성능 보고서 ===")
    
    telemetry_file = 'telemetry_0.json'
    data = MonitoringUtils.load_telemetry(telemetry_file)
    
    if data:
        stats = MonitoringUtils.analyze_telemetry(data)
        
        report = f"""
?????????????????????????????????????????????????
?        Wicked Zerg AI 성능 보고서              ?
?????????????????????????????????????????????????

? 게임 정보
  ? 총 프레임: {stats['total_frames']}
  ? 게임 결과: {stats['game_result']}
  ? 예상 게임 길이: {stats['total_frames'] * 42.4 / 60000:.1f}분 (42.4ms/frame)

? 자원 관리
  ? 미네랄: 평균 {stats['avg_minerals']:.0f} (범위: {stats['min_minerals']}-{stats['max_minerals']})
  ? 가스: 평균 {stats['avg_vespene']:.0f} (범위: {stats['min_vespene']}-{stats['max_vespene']})

?? 군사력
  ? 평균 군대: {stats['avg_army_size']:.0f}
  ? 최대 군대: {stats['max_army_size']}
  ? 최종 군대: {stats['final_army_size']}

? 경제력
  ? 평균 일꾼: {stats['avg_workers']:.0f}
  ? 최대 일꾼: {stats['max_workers']}
  ? 최종 일꾼: {stats['final_workers']}

? 효율성 지표
  ? 자원 효율: {(stats['avg_minerals'] + stats['avg_vespene'] * 1.5) / stats['avg_army_size']:.2f} (낮을수록 좋음)
  ? 인구 활용: {stats['avg_supply_used'] / 200 * 100:.1f}%

generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        print(report)
        
        # 보고서 저장
        with open('performance_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print("[SUCCESS] 보고서 저장: performance_report.txt")


# ============================================================================
# 메인 함수
# ============================================================================

if __name__ == '__main__':
    print("??????????????????????????????????????????????????")
    print("?   Wicked Zerg AI 모니터링 유틸리티              ?")
    print("??????????????????????????????????????????????????")
    
    # 모든 예제 실행
    try:
        example_1_load_and_analyze()
        example_2_export_csv()
        example_3_check_logs()
        example_4_recent_logs()
        example_5_continuous_monitoring()
        example_6_performance_report()
        
        print("\n? 모든 예제 실행 완료!")
        
    except Exception as e:
        print(f"\n? 오류 발생: {e}")
        import traceback
        traceback.print_exc()
