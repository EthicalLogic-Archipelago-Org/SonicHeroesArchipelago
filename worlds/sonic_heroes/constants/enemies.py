"""
Constants related to Enemies
"""
from __future__ import annotations
import dataclasses
import enum
from typing import Self


from rule_builder.rules import Rule

from ..helper_functions import get_default_true_rule
from .char_ability import Team
from .stage import Stage
from .stage_objs import StageObjBase, StageObj
from ..world_base import SonicHeroesWorldBase

#enemy Enums
class EnemyHeight(enum.Enum):
    GROUND = ("Ground", 0)
    HALF_JUMP = ("Half Jump", 1)
    JUMP = ("Jump", 2)
    TALL_CHAR_JUMP = ("Tall Char Jump", 3)
    FULL_FLY_STACK_JUMP = ("Full Fly Stack Jump", 4)
    FULL_FLY_STACK_TALL_CHAR_JUMP = ("Full Fly Stack Tall Char Jump", 5)
    THUNDERSHOOT = ("Thundershoot", 6)
    JUMP_THUNDERSHOOT = ("Jump Thundershoot", 7)
    FLIGHT_THUNDERSHOOT = ("Flight Thundershoot", 8)
    JUMP_FLIGHT_THUNDERSHOOT = ("Jump Flight Thundershoot", 9)

    def __init__(self, description: str, relative_value: int) -> None:
        self.description: str = description
        self.relative_value: int = relative_value

    @property
    def next_higher(self) -> EnemyHeight:
        match self:
            case EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT:
                return EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT
                # raise ValueError(f"{self.description} is the highest Height")
            case EnemyHeight.FLIGHT_THUNDERSHOOT:
                return EnemyHeight.JUMP_FLIGHT_THUNDERSHOOT
            case EnemyHeight.JUMP_THUNDERSHOOT:
                return EnemyHeight.FLIGHT_THUNDERSHOOT
            case EnemyHeight.THUNDERSHOOT:
                return EnemyHeight.JUMP_THUNDERSHOOT
            case EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP:
                return EnemyHeight.THUNDERSHOOT
            case EnemyHeight.FULL_FLY_STACK_JUMP:
                return EnemyHeight.FULL_FLY_STACK_TALL_CHAR_JUMP
            case EnemyHeight.TALL_CHAR_JUMP:
                return EnemyHeight.FULL_FLY_STACK_JUMP
            case EnemyHeight.JUMP:
                return EnemyHeight.TALL_CHAR_JUMP
            case EnemyHeight.HALF_JUMP:
                return EnemyHeight.JUMP
            case EnemyHeight.GROUND:
                return EnemyHeight.HALF_JUMP

    @classmethod
    def match(cls, input_str: str) -> EnemyHeight:
        if input_str == "Ground":
            return cls.GROUND
        if input_str == "HalfJump":
            return cls.HALF_JUMP
        elif input_str == "Jump":
            return cls.JUMP
        elif input_str == "TallCharJump":
            return cls.TALL_CHAR_JUMP
        elif input_str == "FullFlyStackJump":
            return cls.FULL_FLY_STACK_JUMP
        elif input_str == "FullFlyStackTallCharJump":
            return cls.FULL_FLY_STACK_TALL_CHAR_JUMP
        elif input_str == "Thundershoot":
            return cls.THUNDERSHOOT
        elif input_str == "JumpAndThundershoot":
            return cls.JUMP_THUNDERSHOOT
        elif input_str == "FlightAndThundershoot":
            return cls.FLIGHT_THUNDERSHOOT
        else:
            raise ValueError(f"Unknown EnemyHeight match for {input_str}")


class EnemyType(enum.StrEnum):
    NO_ENEMY = "No Enemy (How Did We Get Here?)"
    EGG_FLAPPER = "Egg Flapper"
    EGG_PAWN = "Egg Pawn"
    KLAGEN = "Klagen"
    FALCO = "Falco"
    EGG_HAMMER = "Egg Hammer"
    #HEAVY_EGG_HAMMER = EGGHAMMER
    CAMERON = "Cameron"
    RHINO = "Rhino"
    EGG_BISHOP = "Egg Bishop"
    #EGG_MAGICIAN = EGGBISHOP
    E2000 = "E2000"
    #E2000R = E2000


class _EnemyWeapons(enum.StrEnum):
    """Weapons used by all enemies (don't use this except for the individual enemy enums)"""
    NO_WEAPON = "No Weapon"
    NEEDLE = "Needle"
    SHOT = "Shot"
    MACHINE_GUN = "Machine Gun"
    # Currently not using different machine gun types yet
    MACHINE_GUN_90 = MACHINE_GUN
    MACHINE_GUN_120 = MACHINE_GUN
    MACHINE_GUN_150 = MACHINE_GUN
    MACHINE_GUN_180 = MACHINE_GUN
    # Currently not using different machine gun types yet
    LIGHTNING = "Lightning"
    LASER = LIGHTNING
    BOMB = "Bomb"
    SEARCHLIGHT = "Searchlight"
    LANCE = "Lance"
    BAZOOKA = "Bazooka"


class _EnemyArmor(enum.StrEnum):
    """Armor used by all enemies (don't use this except for the individual enemy enums)"""
    NO_ARMOR = "No Armor"
    SILVER_ARMOR = "Silver Armor"


class _EnemyShields(enum.StrEnum):
    """Shields used by all enemies (don't use this except for the individual enemy enums)"""
    NO_SHIELD = "No Shield"
    CONCRETE_SHIELD = "Concrete Shield"
    PLAIN_SHIELD = "Plain Shield"
    SPIKE_SHIELD = "Spike Shield"


class _EnemySpecialTypes(enum.StrEnum):
    """Special/Alternate Types for all enemies (don't use this except for the individual enemy enums)"""
    REGULAR_PAWN = "Regular Pawn"
    KING_PAWN = "King Pawn"
    CASINO_PAWN_1 = "Casino Pawn 1"
    CASINO_PAWN_2 = "Casino Pawn 2"
    REGULAR_KLAGEN = "Regular Klagen"
    GOLD_KLAGEN = "Gold Klagen"
    REGULAR_EGG_HAMMER = "Regular Egg Hammer"
    HEAVY_EGG_HAMMER = "Heavy Egg Hammer"
    REGULAR_CAMERON = "Regular Cameron"
    GOLD_CAMERON = "Gold Cameron"
    EGG_BISHOP = "Egg Bishop"
    EGG_MAGICIAN = "Egg Magician"
    E2000 = "E2000"
    E2000R = "E2000R"


class EggFlapperWeapon(enum.StrEnum):
    NO_WEAPON = _EnemyWeapons.NO_WEAPON
    NEEDLE = _EnemyWeapons.NEEDLE
    BAZOOKA = _EnemyWeapons.BAZOOKA
    #SHOT = BAZOOKA # <- it is actually the same model
    MACHINE_GUN = _EnemyWeapons.MACHINE_GUN
    MACHINE_GUN_90 = MACHINE_GUN
    MACHINE_GUN_120 = MACHINE_GUN
    MACHINE_GUN_150 = MACHINE_GUN
    MACHINE_GUN_180 = MACHINE_GUN
    # LASER = _EnemyWeapons.LASER
    LIGHTNING = _EnemyWeapons.LIGHTNING
    LASER = LIGHTNING
    BOMB = _EnemyWeapons.BOMB
    SEARCHLIGHT = _EnemyWeapons.SEARCHLIGHT


class EggFlapperArmor(enum.StrEnum):
    NO_ARMOR = _EnemyArmor.NO_ARMOR
    SILVER_ARMOR = _EnemyArmor.SILVER_ARMOR


class EggPawnWeapon(enum.StrEnum):
    NO_WEAPON = _EnemyWeapons.NO_WEAPON
    LANCE = _EnemyWeapons.LANCE
    BAZOOKA = _EnemyWeapons.BAZOOKA
    MACHINE_GUN = _EnemyWeapons.MACHINE_GUN
    MACHINE_GUN_90 = MACHINE_GUN
    MACHINE_GUN_120 = MACHINE_GUN
    MACHINE_GUN_150 = MACHINE_GUN
    MACHINE_GUN_180 = MACHINE_GUN


class EggPawnShield(enum.StrEnum):
    NO_SHIELD = _EnemyShields.NO_SHIELD
    CONCRETE_SHIELD = _EnemyShields.CONCRETE_SHIELD
    PLAIN_SHIELD = _EnemyShields.PLAIN_SHIELD
    SPIKE_SHIELD = _EnemyShields.SPIKE_SHIELD


class EggPawnType(enum.StrEnum):
    REGULAR_PAWN = _EnemySpecialTypes.REGULAR_PAWN
    KING_PAWN = _EnemySpecialTypes.KING_PAWN
    CASINO_PAWN_1 = _EnemySpecialTypes.CASINO_PAWN_1
    CASINO_PAWN_2 = _EnemySpecialTypes.CASINO_PAWN_2


class KlagenType(enum.StrEnum):
    REGULAR_KLAGEN = _EnemySpecialTypes.REGULAR_KLAGEN
    GOLD_KLAGEN = _EnemySpecialTypes.GOLD_KLAGEN


class EggHammerType(enum.StrEnum):
    REGULAR_EGG_HAMMER = _EnemySpecialTypes.REGULAR_EGG_HAMMER
    HEAVY_EGG_HAMMER = _EnemySpecialTypes.HEAVY_EGG_HAMMER


class CameronType(enum.StrEnum):
    REGULAR_CAMERON = _EnemySpecialTypes.REGULAR_CAMERON
    GOLD_CAMERON = _EnemySpecialTypes.GOLD_CAMERON


class RhinoAttack(enum.StrEnum):
    RHINO_NO_ATTACK = "Rhino No Attack"
    RHINO_ATTACK = "Rhino Attack"
    RHINO_ATTACK_HOMING = "Rhino Attack Homing"


class RhinoPath(enum.StrEnum):
    NORMAL_RHINO_PATH = "Normal Rhino Path"
    LOOP_RHINO_PATH = "Loop Rhino Path"


class EggBishopType(enum.StrEnum):
    EGG_BISHOP = _EnemySpecialTypes.EGG_BISHOP
    EGG_MAGICIAN = _EnemySpecialTypes.EGG_MAGICIAN


class E2000Type(enum.StrEnum):
    E2000 = _EnemySpecialTypes.E2000
    E2000R = _EnemySpecialTypes.E2000R


@dataclasses.dataclass(kw_only=True)
class SonicHeroesEnemyBase(StageObjBase):
    """
    Base Enemy Class (inherits from StageObjBase)
    """
    enemy_type: EnemyType = dataclasses.field(init=False, default=EnemyType.NO_ENEMY)
    height: EnemyHeight = EnemyHeight.GROUND

    def __post_init__(self) -> None:
        if type(self) is SonicHeroesEnemyBase:
            raise TypeError("SonicHeroesEnemyBase cannot be instantiated directly")


@dataclasses.dataclass(kw_only=True)
class EggFlapper(SonicHeroesEnemyBase):
    armor: EggFlapperArmor = EggFlapperArmor.NO_ARMOR
    weapon: EggFlapperWeapon = EggFlapperWeapon.NO_WEAPON

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.EGG_FLAPPER)
    enemy_type: EnemyType = dataclasses.field(init=False, default=EnemyType.EGG_FLAPPER)

    def get_enemy_str(self) -> str:
        enemy_str: str = ""

        match self.armor:
            case EggFlapperArmor.NO_ARMOR:
                match self.weapon:
                    case EggFlapperWeapon.NO_WEAPON:
                        enemy_str += "Red"
                    case EggFlapperWeapon.NEEDLE:
                        enemy_str += "Gray"
                    case EggFlapperWeapon.BAZOOKA | EggFlapperWeapon.LIGHTNING:
                        enemy_str += "Green"
                    case EggFlapperWeapon.MACHINE_GUN:
                        enemy_str += "Blue"
                    case EggFlapperWeapon.BOMB:
                        enemy_str += "Pink"
                    case EggFlapperWeapon.SEARCHLIGHT:
                        enemy_str += "Yellow"

            case EggFlapperArmor.SILVER_ARMOR:
                enemy_str += "Silver Armor"

        enemy_str += f" {self.enemy_type} with {self.weapon} at {self.height} Height"
        return enemy_str


@dataclasses.dataclass(kw_only=True)
class EggPawn(SonicHeroesEnemyBase):
    weapon: EggPawnWeapon = EggPawnWeapon.NO_WEAPON
    shield: EggPawnShield = EggPawnShield.NO_SHIELD
    special_type: EggPawnType = EggPawnType.REGULAR_PAWN

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.EGG_PAWN)
    enemy_type: EnemyType = dataclasses.field(init=False, default=EnemyType.EGG_PAWN)

    def get_enemy_str(self) -> str:
        enemy_str: str = ""
        if self.special_type is EggPawnType.KING_PAWN:
            enemy_str += "King "
        if self.special_type is EggPawnType.CASINO_PAWN_1 or self.special_type is EggPawnType.CASINO_PAWN_2:
            enemy_str += "Casino "
        enemy_str += f"{self.enemy_type} with {self.shield} and {self.weapon} at {self.height} Height"
        return enemy_str


@dataclasses.dataclass(kw_only=True)
class Klagen(SonicHeroesEnemyBase):
    special_type: KlagenType = KlagenType.REGULAR_KLAGEN

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.KLAGEN)
    enemy_type: EnemyType = dataclasses.field(init=False, default=EnemyType.KLAGEN)


@dataclasses.dataclass(kw_only=True)
class Falco(SonicHeroesEnemyBase):

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.FALCO)
    enemy_type: EnemyType = dataclasses.field(init=False, default=EnemyType.FALCO)


@dataclasses.dataclass(init=False, kw_only=True)
class EggHammer(SonicHeroesEnemyBase):
    special_type: EggHammerType = EggHammerType.REGULAR_EGG_HAMMER

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.EGG_HAMMER)
    enemy_type: EnemyType = dataclasses.field(init=False, default=EnemyType.EGG_HAMMER)


@dataclasses.dataclass(kw_only=True)
class Cameron(SonicHeroesEnemyBase):
    special_type: CameronType = CameronType.REGULAR_CAMERON

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.CAMERON)
    enemy_type: EnemyType = dataclasses.field(init=False, default=EnemyType.CAMERON)


@dataclasses.dataclass(kw_only=True)
class Rhino(SonicHeroesEnemyBase):
    attack: RhinoAttack = RhinoAttack.RHINO_NO_ATTACK
    path: RhinoPath = RhinoPath.NORMAL_RHINO_PATH

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.RHINO_LINER)
    enemy_type: EnemyType = dataclasses.field(init=False, default=EnemyType.RHINO)


@dataclasses.dataclass(kw_only=True)
class EggBishop(SonicHeroesEnemyBase):
    special_type: EggBishopType = EggBishopType.EGG_BISHOP

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.EGG_BISHOP)
    enemy_type: EnemyType = dataclasses.field(init=False, default=EnemyType.EGG_BISHOP)


@dataclasses.dataclass(kw_only=True)
class E2000(SonicHeroesEnemyBase):
    special_type: E2000Type = E2000Type.E2000

    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.E2000)
    enemy_type: EnemyType = dataclasses.field(init=False, default=EnemyType.E2000)


