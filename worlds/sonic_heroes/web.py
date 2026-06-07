"""
The WebWorld
"""
from typing import ClassVar

from BaseClasses import Tutorial
from Options import OptionGroup
from worlds.AutoWorld import WebWorld

from .constants.apworld import *
from .options import sonic_heroes_option_groups

class SonicHeroesWebWorld(WebWorld):
    theme: str = PARTY_TIME_THEME
    setup_en: Tutorial = (Tutorial(
        tutorial_name=TUTORIAL_NAME,
        description=TUTORIAL_DESC,
        language=TUTORIAL_LANGUAGE,
        file_name=TUTORIAL_FILE_NAME,
        link=TUTORIAL_LINK,
        authors=TUTORIAL_AUTHORS
    ))

    tutorials: list[Tutorial] = [setup_en]
    game_info_languages: list[str] = ["en"]
    option_groups: ClassVar[list[OptionGroup]] = sonic_heroes_option_groups