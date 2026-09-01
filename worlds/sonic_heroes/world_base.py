"""
The World Base Class
"""
from typing import TYPE_CHECKING, override, ClassVar


from worlds.AutoWorld import World
from BaseClasses import MultiWorld
from Options import PerGameCommonOptions
from rule_builder.cached_world import CachedRuleBuilderWorld
from rule_builder.rules import Rule

from .constants.apworld import SONIC_HEROES
from .options import SonicHeroesOptions
from .web import SonicHeroesWebWorld



class SonicHeroesWorldBase(World):
    web: ClassVar[SonicHeroesWebWorld] = SonicHeroesWebWorld()  # pyright: ignore[reportIncompatibleVariableOverride]
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
        super().__init__(multiworld=multiworld, player=player)
        self.rule_macros = {}
        self.unplaced_items: int = 0

        self.starting_inventory_amounts: dict[str, int] = {}
        """List of item names to start with"""
