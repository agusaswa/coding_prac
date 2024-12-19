import load_creator as lc
from typing import Optional, List

def total_load(lr: lc.LoadRecord, load_types: Optional[List[lc.LoadType]] = None) -> float:
        load_map = {
            lc.LoadType.SELF_WEIGHT: lr.self_weight,
            lc.LoadType.DEAD_LOAD: lr.dead_load,
            lc.LoadType.LIVE_LOAD: lr.live_load,
            lc.LoadType.SDL: lr.sdl
        }

        if load_types:
            load_to_calc = [
            load_map[lt] for lt in load_types
            if load_map[lt] is not None
            ]
        else:
            load_to_calc = [
            attr for attr in load_map.values()
            if attr is not None
            ]
        return sum(load.magnitude() for load in load_to_calc if load is not None)