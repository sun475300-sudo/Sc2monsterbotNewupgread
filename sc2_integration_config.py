# -*- coding: utf-8 -*-
"""
sc2AIagent Integration - Consolidated Bot Configuration
Copies essential configuration and enums from sc2AIagent
"""

from enum import Enum, IntEnum, auto
from dataclasses import dataclass
from typing import Dict, List

from sc2.ids.unit_typeid import UnitTypeId


class GamePhase(Enum):
    """Game phase - transitions dynamically based on scouting"""
    OPENING = auto()
    ECONOMY = auto()
    TECH = auto()
    ATTACK = auto()
    DEFENSE = auto()
    ALL_IN = auto()


class EnemyRace(Enum):
    """Opponent race detection"""
    TERRAN = auto()
    PROTOSS = auto()
    ZERG = auto()
    UNKNOWN = auto()


class StrategyMode(Enum):
    """Strategy mode enum"""
    OPENING = auto()
    MACRO = auto()
    DEFENSE = auto()
    RUSH = auto()
    ALL_IN = auto()
    LATE_GAME = auto()


class ThreatLevel(IntEnum):
    """Threat level assessment (IntEnum allows numeric comparisons)"""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass(frozen=True)
class AIConfig:
    """SC2 AI Bot Configuration (from sc2AIagent)"""
    
    # Worker Management
    MAX_WORKERS: int = 60
    WORKERS_PER_BASE: int = 16
    WORKERS_PER_GAS: int = 3
    
    # Resource Thresholds
    MINERAL_THRESHOLD: int = 500
    GAS_THRESHOLD: int = 200
    
    # All-In Build
    ALL_IN_12_POOL: bool = False
    ALL_IN_WORKER_LIMIT: int = 12
    ALL_IN_ZERGLING_ATTACK: int = 2
    
    # Army Thresholds
    ZERGLING_ATTACK_THRESHOLD: int = 12
    ROACH_THRESHOLD: int = 8
    HYDRA_THRESHOLD: int = 6
    TOTAL_ARMY_THRESHOLD: int = 60
    
    # Timing Thresholds
    RUSH_TIMING_TERRAN: int = 300
    RUSH_TIMING_PROTOSS: int = 240
    RUSH_TIMING_ZERG: int = 180
    ALL_IN_ATTACK_SUPPLY: int = 120
    
    # Combat Parameters
    RALLY_GATHER_PERCENT: float = 0.8
    MIN_DEFENSE_BEFORE_EXPAND: int = 8
    KITING_DISTANCE: float = 2.0
    ENGAGE_DISTANCE: float = 15.0
    RETREAT_HP_PERCENT: float = 0.3
    
    # Tech Timings
    SPAWNING_POOL_SUPPLY: int = 14
    ROACH_WARREN_TIME: int = 180
    LAIR_TIME: int = 300
    HYDRA_DEN_TIME: int = 360
    TECH_LAIR_MINERALS: int = 150
    
    # Scouting
    INITIAL_SCOUT_SUPPLY: int = 13
    SCOUT_INTERVAL: float = 60.0
    RUSH_DETECTION_DISTANCE: float = 30.0
    
    # Game Phases
    EARLY_GAME_TIME: int = 180
    MID_GAME_TIME: int = 360
    LATE_GAME_TIME: int = 720
    
    # Supply Management
    SUPPLY_BUFFER: int = 16
    OVERLORD_PREDICT_TIME: float = 5.0


# Unit Target Priority (for micro management)
TARGET_PRIORITY: Dict = {
    UnitTypeId.SIEGETANK: 10,
    UnitTypeId.SIEGETANKSIEGED: 12,
    UnitTypeId.MEDIVAC: 9,
    UnitTypeId.THOR: 8,
    UnitTypeId.BATTLECRUISER: 11,
    UnitTypeId.LIBERATOR: 9,
    UnitTypeId.WIDOWMINE: 7,
    UnitTypeId.MARINE: 5,
    UnitTypeId.MARAUDER: 6,
    UnitTypeId.REAPER: 5,
    UnitTypeId.GHOST: 10,
    UnitTypeId.HELLION: 4,
    UnitTypeId.CYCLONE: 6,
    UnitTypeId.COLOSSUS: 12,
    UnitTypeId.HIGHTEMPLAR: 11,
    UnitTypeId.DISRUPTOR: 10,
    UnitTypeId.IMMORTAL: 9,
    UnitTypeId.ARCHON: 8,
    UnitTypeId.CARRIER: 11,
    UnitTypeId.VOIDRAY: 7,
    UnitTypeId.STALKER: 5,
    UnitTypeId.ZEALOT: 4,
    UnitTypeId.ADEPT: 5,
    UnitTypeId.SENTRY: 6,
    UnitTypeId.LURKER: 10,
    UnitTypeId.INFESTOR: 9,
    UnitTypeId.BROODLORD: 11,
    UnitTypeId.ULTRALISK: 8,
    UnitTypeId.ROACH: 5,
    UnitTypeId.HYDRALISK: 6,
    UnitTypeId.MUTALISK: 7,
}


# Counter-Build Strategy
COUNTER_BUILD: Dict = {
    EnemyRace.TERRAN: {
        "early_units": [UnitTypeId.ZERGLING, UnitTypeId.BANELING],
        "mid_units": [UnitTypeId.ROACH, UnitTypeId.RAVAGER],
        "late_units": [UnitTypeId.HYDRALISK, UnitTypeId.LURKER],
        "priority_buildings": [UnitTypeId.BANELINGNEST, UnitTypeId.ROACHWARREN],
        "defense_building": UnitTypeId.SPINECRAWLER,
    },
    EnemyRace.PROTOSS: {
        "early_units": [UnitTypeId.ZERGLING, UnitTypeId.ROACH],
        "mid_units": [UnitTypeId.HYDRALISK, UnitTypeId.RAVAGER],
        "late_units": [UnitTypeId.CORRUPTOR, UnitTypeId.BROODLORD],
        "priority_buildings": [UnitTypeId.ROACHWARREN, UnitTypeId.HYDRALISKDEN],
        "defense_building": UnitTypeId.SPORECRAWLER,
    },
    EnemyRace.ZERG: {
        "early_units": [UnitTypeId.ZERGLING, UnitTypeId.BANELING],
        "mid_units": [UnitTypeId.ROACH, UnitTypeId.HYDRALISK],
        "late_units": [UnitTypeId.ULTRALISK, UnitTypeId.BROODLORD],
        "priority_buildings": [UnitTypeId.ROACHWARREN, UnitTypeId.BANELINGNEST],
        "defense_building": UnitTypeId.SPINECRAWLER,
    },
}


# Threat Building Priority
THREAT_BUILDINGS: Dict = {
    UnitTypeId.BARRACKS: 3,
    UnitTypeId.FACTORY: 2,
    UnitTypeId.STARPORT: 2,
    UnitTypeId.BUNKER: 5,
    UnitTypeId.STARGATE: 4,
    UnitTypeId.ROBOTICSFACILITY: 2,
    UnitTypeId.DARKSHRINE: 6,
    UnitTypeId.SPAWNINGPOOL: 2,
    UnitTypeId.ROACHWARREN: 3,
    UnitTypeId.BANELINGNEST: 4,
}
