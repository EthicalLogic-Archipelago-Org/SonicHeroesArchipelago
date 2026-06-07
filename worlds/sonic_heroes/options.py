"""
Options for Sonic Heroes AP
"""
import dataclasses
from typing import ClassVar

from Options import Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Toggle, Visibility, OptionError


class MakePuml(Toggle):
    """
    Should This APWorld Make a Puml File?
    """
    display_name: str = "Make Puml"
    visibility: Visibility = Visibility.none


class ProgressiveAbilityItems(DefaultOnToggle):
    """
    Replace some (but not all) ability items with a progressive ability item
    Homing -> Triangle Jump
    Tornado -> Invisible
    Thundershoot -> Flight (Dummy Rings and Cheese Cannon)
    Power Attack -> Combo Finisher
    """
    display_name: str = "Progressive Ability Items"


class RingSanityDark(Choice):
    """
    How should Ring Sanity for Dark be handled?
    """
    display_name: str = "Ring Sanity Dark"
    option_disabled: int = 0
    option_groups: int = 1
    option_all_rings: int = 2


class Difficulty(Choice):
    """
    Should various tricks be enabled based on difficulty?
    There are currently not a lot right now (mostly a placeholder)
    """
    display_name: str = "Difficulty"
    option_none: int = 0
    option_medium: int = 1
    default: ClassVar[int] = option_none

class BadnikBounce(Toggle):
    """
    Should Badnik Bounce trick be enabled logically?
    This involves jumping into enemies in order to gain extra height
    This requires jump hover frames as well
    """
    display_name: str = "Badnik Bounce"

class CollisAbuse(Toggle):
    """
    Should Collision Abuse trick be enabled logically?
    This refers to jumping into slanted walls and collision to gain extra height
    """
    display_name: str = "Collision Abuse"

class HoverFrame(Choice):
    """
    Should Hover Frames be enabled logically?
    Holding the jump button allows for a certain amount of "Hover Frames"
    Combining this with homing attack or tornado allows for extra height and distance
    """
    display_name: str = "Hover Frame"
    option_disabled: int = 0
    option_jump_hover: int = 1
    option_jump_and_homing_or_tornado_hover: int = 2
    default: ClassVar[int] = option_disabled

class Parkour(Toggle):
    """
    Should Parkour be enabled logically?
    Parkour involves tricky collision like staying on the small "guardrails" on either side of the path on Seaside Hill
    """
    display_name: str = "Parkour"

class FlyDepleteBoost(Toggle):
    """
    Should the Fly Deplete Boost trick be enabled logically?
    Gaining height exactly when the fly meter completely fills allows for going above the height cap
    """
    display_name: str = "Fly Deplete Boost"

class FlyGroundBounce(Choice):
    """
    Should the FlyGroundBounce trick be enabled logically?
    Time the flight button on the frame when hitting the ground to get a bunch of height before starting flight
    It is possible but harder to do without jump (hence the separate option)
    """
    display_name: str = "Fly Ground Bounce"
    option_disabled: int = 0
    option_with_jump: int = 1
    option_without_jump: int = 2
    default: ClassVar[int] = option_disabled






sonic_heroes_option_groups: list[OptionGroup] = \
[
    OptionGroup(name="Meta",
                options = \
                [
                    ProgressiveAbilityItems,
                    RingSanityDark,
                ]),
    OptionGroup(name="Tricks",
                options = \
                [
                    Difficulty,
                    BadnikBounce,
                    CollisAbuse,
                    HoverFrame,
                    Parkour,
                    FlyDepleteBoost,
                    FlyGroundBounce,
                ]),
    OptionGroup(name="Hidden",
                options = \
                [
                    MakePuml,
                ]),
]

@dataclasses.dataclass
class SonicHeroesOptions(PerGameCommonOptions):
    make_puml: MakePuml

    progressive_ability_items: ProgressiveAbilityItems

    ring_sanity_dark: RingSanityDark

    difficulty: Difficulty
    badnik_bounce: BadnikBounce
    collis_abuse: CollisAbuse
    hover_frame: HoverFrame
    parkour: Parkour
    fly_deplete_boost: FlyDepleteBoost
    fly_ground_bounce: FlyGroundBounce


def check_options(options: SonicHeroesOptions) -> None:
    if options.badnik_bounce == BadnikBounce.option_true and options.hover_frame == HoverFrame.option_disabled:
        raise OptionError(f"Badnik Bounce requires hover frames to be enabled")


