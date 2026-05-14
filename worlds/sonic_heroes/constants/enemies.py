"""
Constants related to Enemies
"""
import dataclasses
import enum
from typing import override


#enemy Enums
class EnemyHeight(enum.Enum):
    GROUND = ("Ground", 0)
    JUMP = ("Jump", 1)
    HOMING = ("Homing", 2)
    JUMP_THUNDERSHOOT = ("Jump + Thundershoot", 3)
    FLIGHT_THUNDERSHOOT = ("Flight + Thundershoot", 4)

    def __init__(self, description: str, relative_value: int) -> None:
        self.description = description
        self.relative_value = relative_value



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
    SHOT = _EnemyWeapons.SHOT
    MACHINE_GUN = _EnemyWeapons.MACHINE_GUN
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


@dataclasses.dataclass(init=False)
class SonicHeroesEnemy:
    """
    Base Enemy Class
    """
    type: EnemyType = EnemyType.NO_ENEMY

    def get_func_str(self) -> str:
        return f"{self.__class__.__name__}(type={self.type.__class__.__name__}.{self.type.name})"


@dataclasses.dataclass(init=False, kw_only=True)
class EggFlapper(SonicHeroesEnemy):
    armor: EggFlapperArmor = EggFlapperArmor.NO_ARMOR
    weapon: EggFlapperWeapon = EggFlapperWeapon.NO_WEAPON

    def __init__(self, armor: EggFlapperArmor, weapon: EggFlapperWeapon) -> None:
        self.armor = armor
        self.weapon = weapon
        self.type: EnemyType = EnemyType.EGG_FLAPPER

    @override
    def get_func_str(self) -> str:
        return f"{self.__class__.__name__}(armor={self.armor.__class__.__name__}.{self.armor.name}, weapon={self.weapon.__class__.__name__}.{self.weapon.name})"


@dataclasses.dataclass(init=False, kw_only=True)
class EggPawn(SonicHeroesEnemy):
    weapon: EggPawnWeapon = EggPawnWeapon.NO_WEAPON
    shield: EggPawnShield = EggPawnShield.NO_SHIELD
    special_type: EggPawnType = EggPawnType.REGULAR_PAWN

    def __init__(self, weapon: EggPawnWeapon, shield: EggPawnShield, special_type: EggPawnType) -> None:
        self.weapon = weapon
        self.shield = shield
        self.special_type = special_type
        self.type: EnemyType = EnemyType.EGG_PAWN

    @override
    def get_func_str(self) -> str:
        return f"{self.__class__.__name__}(weapon={self.weapon.__class__.__name__}.{self.weapon.name}, shield={self.shield.__class__.__name__}.{self.shield.name}, special_type={self.special_type.__class__.__name__}.{self.special_type.name})"


@dataclasses.dataclass(init=False, kw_only=True)
class Klagen(SonicHeroesEnemy):
    special_type: KlagenType = KlagenType.REGULAR_KLAGEN

    def __init__(self, special_type: KlagenType) -> None:
        self.special_type = special_type
        self.type: EnemyType = EnemyType.KLAGEN

    @override
    def get_func_str(self) -> str:
        return f"{self.__class__.__name__}(special_type={self.special_type.__class__.__name__}.{self.special_type.name})"


@dataclasses.dataclass(init=False, kw_only=True)
class Falco(SonicHeroesEnemy):
    def __init__(self) -> None:
        self.type: EnemyType = EnemyType.FALCO

    @override
    def get_func_str(self) -> str:
        return f"{self.__class__.__name__}()"


@dataclasses.dataclass(init=False, kw_only=True)
class EggHammer(SonicHeroesEnemy):
    special_type: EggHammerType = EggHammerType.REGULAR_EGG_HAMMER

    def __init__(self, special_type: EggHammerType) -> None:
        self.special_type = special_type
        self.type: EnemyType = EnemyType.EGG_HAMMER

    @override
    def get_func_str(self) -> str:
        return f"{self.__class__.__name__}(special_type={self.special_type.__class__.__name__}.{self.special_type.name})"


@dataclasses.dataclass(init=False, kw_only=True)
class Cameron(SonicHeroesEnemy):
    special_type: CameronType = CameronType.REGULAR_CAMERON

    def __init__(self, special_type: CameronType) -> None:
        self.special_type = special_type
        self.type: EnemyType = EnemyType.CAMERON

    @override
    def get_func_str(self) -> str:
        return f"{self.__class__.__name__}(special_type={self.special_type.__class__.__name__}.{self.special_type.name})"


@dataclasses.dataclass(init=False, kw_only=True)
class Rhino(SonicHeroesEnemy):
    attack: RhinoAttack = RhinoAttack.RHINO_NO_ATTACK
    path: RhinoPath = RhinoPath.NORMAL_RHINO_PATH

    def __init__(self, attack: RhinoAttack, path: RhinoPath) -> None:
        self.attack = attack
        self.path = path
        self.type: EnemyType = EnemyType.RHINO

    @override
    def get_func_str(self) -> str:
        return f"{self.__class__.__name__}(attack={self.attack.__class__.__name__}.{self.attack.name}, path={self.path.__class__.__name__}.{self.path.name})"


@dataclasses.dataclass(init=False, kw_only=True)
class EggBishop(SonicHeroesEnemy):
    special_type: EggBishopType = EggBishopType.EGG_BISHOP

    def __init__(self, special_type: EggBishopType) -> None:
        self.special_type = special_type
        self.type: EnemyType = EnemyType.EGG_BISHOP

    @override
    def get_func_str(self) -> str:
        return f"{self.__class__.__name__}(special_type={self.special_type.__class__.__name__}.{self.special_type.name})"


@dataclasses.dataclass(init=False, kw_only=True)
class E2000(SonicHeroesEnemy):
    special_type: E2000Type = E2000Type.E2000

    def __init__(self, special_type: E2000Type) -> None:
        self.special_type = special_type
        self.type: EnemyType = EnemyType.E2000

    @override
    def get_func_str(self) -> str:
        return f"{self.__class__.__name__}(special_type={self.special_type.__class__.__name__}.{self.special_type.name})"