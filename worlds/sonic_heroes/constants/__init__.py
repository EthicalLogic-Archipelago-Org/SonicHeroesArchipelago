"""
All constants used by APWorld (thanks circular imports)
Can be used by multiple instances (no instance vars allowed here)
"""

from . import apworld as apworld
from . import char_ability as char_ability
from . import enemies as enemies
from . import items_events as items_events
from . import loc_region as loc_region
from . import stage as stage
from . import stage_objs as stage_objs


__all__ = ['apworld', 'char_ability', 'enemies', 'items_events', 'loc_region', 'stage', 'stage_objs']
