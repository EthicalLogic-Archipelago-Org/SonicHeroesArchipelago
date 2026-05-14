"""
Constants related to the APWorld itself
"""
from typing import override


class RejectDictionaryReturnToMonke(dict[object, object]):
    """
    This will ValueError if Key is already present in dict instead of silently overwriting
    """
    @override
    def __setitem__(self, key: object, value: object) -> None:
        try:
            _ = self.__getitem__(key)
            #if value != self.__getitem__(key):
            raise ValueError(f"Key ({key}: {self.__getitem__(key)}) is already present in dictionary. New Value: {value}")
            #else:
                #return super(RejectDictionaryReturnToMonke, self).__setitem__(key, value)
        except KeyError:
            return super(RejectDictionaryReturnToMonke, self).__setitem__(key, value)


SONIC_HEROES: str = "Sonic Heroes"
PARTY_TIME_THEME: str = "partyTime"
TUTORIAL_NAME: str = "Multiworld Setup Guide"
TUTORIAL_DESC: str = f"A guide to setting up the {SONIC_HEROES} randomizer connected to an Archipelago Multiworld."
TUTORIAL_LANGUAGE: str = "English"
TUTORIAL_FILE_NAME: str = "setup_en.md"
TUTORIAL_LINK: str = "setup/en"
TUTORIAL_AUTHORS: list[str] = ["EthicalLogic"]

RULE_CACHING_ENABLED_ATTR: str = "rule_caching_enabled"
RE_GEN_PASSTHROUGH_ATTR: str = "re_gen_passthrough"
GENERATION_IS_FAKE_ATTR: str = "generation_is_fake"
