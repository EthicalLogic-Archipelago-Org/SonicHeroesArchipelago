"""
The World Base Class
"""
from typing import override, ClassVar

from worlds.AutoWorld import World
from BaseClasses import MultiWorld
from Options import PerGameCommonOptions
from rule_builder.cached_world import CachedRuleBuilderWorld
from rule_builder.rules import Rule


from .constants.apworld import SONIC_HEROES
from .options import SonicHeroesOptions


class SonicHeroesWorldBase(World):
    # web = SonicHeroesWebWorld()
    options_dataclass: ClassVar[type[PerGameCommonOptions]] = SonicHeroesOptions
    options: SonicHeroesOptions  # pyright: ignore[reportIncompatibleVariableOverride]

    # settings: ClassVar[SonicHeroesSettings]

    rule_macros: dict[str, Rule.Resolved]
    """
    Mapping of custom rule macro name to resolved rule
    Used for explaining custom macro rules
    """
    topology_present: bool = True
    """
    Does the world have meaningful topology? (for Logic Routing)
    """

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld, player)
        self.rule_macros = {}