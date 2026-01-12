# -*- coding: utf-8 -*-
"""
================================================================================
                    🎖️ 유닛 생산 관리 (production_manager.py)
================================================================================
전투 유닛을 뽑고 인구수를 관리하는 핵심 루프입니다.

핵심 기능:
    1. 대군주 예측 생산 (인구수 막힘 방지)
    2. 드론 생산 (경제)
    3. 여왕 생산 (펌핑용)
    4. 테크 기반 군사 유닛 생산 (저글링 → 로치 → 히드라)
    5. 상성 기반 유닛 선택 (Counter-Build)
================================================================================
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

# Logger setup
try:
    from loguru import logger
except ImportError:
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)


class TechAdvancer:
    """기술 진행 전문가"""

    def __init__(self, production_manager):
        self.pm = production_manager
        self.bot = production_manager.bot
        self.config = production_manager.config

    async def _expand_for_gas(self):
        """
        가스 확보용 빠른 멀티 확장

        가스는 한 베이스당 2개로 제한되어 있습니다.
        즉, 가스를 많이 얻으려면 부화장(Hatchery) 개수를 늘리는 것이 유일한 길입니다.

        봇이 스스로 판단하여 미네랄이 300 이상 모이고, 가스통을 더 지을 곳이 없다면 확장
        """
        b = self.bot

        # 이미 확장 중이면 대기
        if b.already_pending(UnitTypeId.HATCHERY) > 0:
            return

        townhalls = [th for th in b.townhalls]
        current_base_count = len(townhalls)

        # 최대 8멀티까지 빠르게 확장 (가스 수입 극대화)
        if current_base_count >= 8:
            return

        # 가스통 건설 가능 여부 체크
        ready_extractors = list(
            b.units.filter(
                lambda u: u.type_id == UnitTypeId.EXTRACTOR and u.is_structure and u.is_ready
            )
        )

        # 모든 부화장의 가스통이 건설되었는지 확인
        all_gas_built = True
        for th in townhalls:
            if th.is_ready:
                try:
                    vgs = b.vespene_geyser.closer_than(15, th)
                    for vg in vgs:
                        nearby_extractors = b.structures(UnitTypeId.EXTRACTOR).closer_than(1, vg)
                        if not nearby_extractors.exists:
                            all_gas_built = False
                            break
                    if not all_gas_built:
                        break
                except:
                    pass

        # 조건 1: 미네랄이 학습된 임계값 이상이고, 모든 가스통이 건설되었으면 확장
        from config import get_learned_parameter

        gas_expand_mineral_threshold = get_learned_parameter("gas_expand_mineral_threshold", 300)

        if b.minerals >= gas_expand_mineral_threshold and all_gas_built:
            if b.can_afford(UnitTypeId.HATCHERY):
                try:
                    await b.expand_now()
                    current_iteration = getattr(b, "iteration", 0)
                    if current_iteration % 50 == 0:
                        print(
                            f"[GAS EXPAND] [{int(b.time)}s] 가스 확보용 멀티 확장: {current_base_count + 1}멀티"
                        )
                except Exception:
                    pass

        # 조건 2: 가스가 학습된 임계값 이상 남는다면 즉시 확장 (가스가 남는 상황)
        gas_expand_vespene_threshold = get_learned_parameter("gas_expand_vespene_threshold", 1000)
        gas_expand_mineral_threshold_2 = get_learned_parameter(
            "gas_expand_mineral_threshold_2", 300
        )
        if (
            b.vespene >= gas_expand_vespene_threshold
            and b.minerals >= gas_expand_mineral_threshold_2
        ):
            if b.can_afford(UnitTypeId.HATCHERY):
                try:
                    await b.expand_now()
                    current_iteration = getattr(b, "iteration", 0)
                    if current_iteration % 50 == 0:
                        print(
                            f"[GAS EXPAND] [{int(b.time)}s] 가스 과다 보유 → 멀티 확장: {current_base_count + 1}멀티"
                        )
                except Exception:
                    pass

        # 조건 3: 미네랄이 학습된 임계값 이상이고 기지가 학습된 개수 미만이면 적극 확장
        aggressive_expand_mineral_threshold = get_learned_parameter(
            "aggressive_expand_mineral_threshold", 400
        )
        max_base_count = get_learned_parameter("max_base_count", 5)
        if (
            b.minerals >= aggressive_expand_mineral_threshold
            and current_base_count < max_base_count
        ):
            if b.can_afford(UnitTypeId.HATCHERY):
                try:
                    await b.expand_now()
                    current_iteration = getattr(b, "iteration", 0)
                    if current_iteration % 50 == 0:
                        print(
                            f"[GAS EXPAND] [{int(b.time)}s] 적극적 멀티 확장: {current_base_count + 1}멀티"
                        )
                except Exception:
                    pass

    # =========================================================================
    # 7️⃣ 필수 업그레이드 자동 연구 (자원이 남을 때) - 강화 버전
    # =========================================================================

    async def _visualize_tech_progression(self, bot, tech_id: UnitTypeId, building: bool):
        """
        테크 진행 상태를 화면에 시각적으로 표시

        Args:
            bot: 봇 인스턴스
            tech_id: 건설 중인 테크 건물 ID
            building: 건설 시작 여부 (True: 건설 중, False: 자원 예약 중)
        """
        try:
            current_iteration = getattr(bot, "iteration", 0)
            # 4프레임마다 업데이트 (CPU 부담 감소)
            if current_iteration % 4 != 0:
                return

            if hasattr(bot, "client") and bot.client:
                if building:
                    status_text = f"BUILDING: {tech_id.name}"
                    color = (0, 255, 0)  # Green: 건설 중
                else:
                    status_text = f"RESERVING RESOURCES: {tech_id.name}"
                    color = (255, 255, 0)  # Yellow: 자원 예약 중

                # 화면 중앙 하단에 상태 표시
                try:
                    bot.client.debug_text_screen(status_text, pos=(0.3, 0.85), size=12, color=color)
                except Exception:
                    # debug_text_screen이 지원되지 않는 경우 무시
                    pass
        except Exception:
            # 시각화 실패는 게임 플레이에 영향을 주지 않도록 무시
            pass

    async def build_tech_structures(self):
        """
        Build tech structures - AUTONOMOUS DECISION ONLY.

        This function is now DEPRECATED - all tech building construction
        is handled by _autonomous_tech_progression() which makes decisions
        based on game state, resources, and learned parameters.

        Only handles Evolution Chamber upgrades (non-tech building).
        """
        b = self.bot

        # Tech building construction is now handled by _autonomous_tech_progression()
        # This function only handles Evolution Chamber upgrades

        # Check for idle Evolution Chambers and research upgrades
        # Use is_idle instead of is_researching for better resource management
        evolution_chambers = b.structures(UnitTypeId.EVOLUTIONCHAMBER).ready
        for evo in evolution_chambers:
            if evo.is_idle:
                # Research missile attack upgrade if affordable
                # Use correct UpgradeId name: ZERGMISSILEWEAPONSLEVEL1
                if hasattr(UpgradeId, "ZERGMISSILEWEAPONSLEVEL1"):
                    upgrade_id = UpgradeId.ZERGMISSILEWEAPONSLEVEL1  # type: ignore
                    if b.can_afford(upgrade_id):
                        if upgrade_id not in b.state.upgrades:
                            try:
                                evo.research(upgrade_id)
                            except Exception:
                                pass  # Silent fail if research fails
                # Research ground carapace upgrade if affordable
                elif hasattr(UpgradeId, "ZERGGROUNDARMORSLEVEL1"):
                    upgrade_id = UpgradeId.ZERGGROUNDARMORSLEVEL1  # type: ignore
                    if b.can_afford(upgrade_id):
                        if upgrade_id not in b.state.upgrades:
                            try:
                                evo.research(upgrade_id)
                            except Exception:
                                pass  # Silent fail if research fails
