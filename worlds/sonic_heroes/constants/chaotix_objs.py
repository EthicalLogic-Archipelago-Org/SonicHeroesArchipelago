import dataclasses

from .stage_objs import StageObjBase, StageObj


@dataclasses.dataclass
class HermitCrabData(StageObjBase):
    obj_id: StageObj = dataclasses.field(init=False, default=StageObj.HERMIT_CRAB)