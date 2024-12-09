from dataclasses import dataclass
from typing import Optional,List

@dataclass
class SelfWeight:
    unit_weight: float
    des_thickness: float

    def magnitude(self) -> float:
        return self.unit_weight * self.des_thickness/1000

@dataclass
class DeadLoad:
    unit_weight: float
    des_thickness: float

    def magnitude(self) -> float:
        return self.unit_weight * self.des_thickness/1000

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

class Load:
    def __init__(
            self,
            self_weight: Optional[SelfWeight] = None,
            dead_load: Optional[DeadLoad] = None,
            live_load: Optional[LiveLoad] = None,
            sdl: Optional[SDL] = None
            ) -> None:
        self.self_weight = self_weight
        self.dead_load = dead_load
        self.live_load = live_load
        self.sdl = sdl if sdl is not None else SDL(sdl_data=[])
    
    def total_load(self):
        total=sum(
        load.magnitude() for load in 
        [self.self_weight, self.dead_load, self.live_load, self.sdl] 
        if load is not None
        )
        
        return total