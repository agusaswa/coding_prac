from dataclasses import dataclass
from typing import Optional, List
from enum import Enum, auto

class LoadType(Enum):
    """
    This class include enum of class Load attributes, included below:\n
    SELF_WEIGHT -> load_processor.SelfWeight\n
    DEAD_LOAD -> load_processor.DeadLoad\n
    LIVE_LOAD -> load_processor.LiveLoad\n
    SDL -> load_processor.SDL\n
    """
    SELF_WEIGHT = auto()
    DEAD_LOAD = auto()
    LIVE_LOAD = auto()
    SDL = auto()


@dataclass
class SelfWeight:
    unit_weight: float
    des_thickness: float

    def magnitude(self) -> float:
        return self.unit_weight * self.des_thickness / 1000

@dataclass
class DeadLoad:
    unit_weight: float
    des_thickness: float

    def magnitude(self) -> float:
        return self.unit_weight * self.des_thickness / 1000

@dataclass
class SDL_Data:
    category_name: str
    unit_weight: Optional[float] = None
    des_thickness: Optional[float] = None
    predef_magnitude: Optional[float] = None

    def magnitude(self) -> float:
        if self.unit_weight is None and self.des_thickness is None:
            return self.predef_magnitude or 0
        return (self.unit_weight * self.des_thickness) / 1000

@dataclass
class SDL:
    sdl_data: List[SDL_Data] 

    def magnitude(self) -> float:
        return sum(sdl.magnitude() for sdl in self.sdl_data)
    
@dataclass
class LiveLoad:
    predef_magnitude: float

    def magnitude(self) -> float:
        return self.predef_magnitude

@dataclass
class LoadRecord:
    self_weight: Optional[SelfWeight] = None
    dead_load: Optional[DeadLoad] = None
    live_load: Optional[LiveLoad] = None
    sdl: Optional[SDL] = None

    def __post_init__(self):
        # This method is called automatically after the dataclass is initialized
        if self.sdl is None:
            self.sdl = SDL(sdl_data=[])
