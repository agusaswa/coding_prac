import load_creator as create_load
import load_processor as calc
from typing import Optional,List

# Import all necessary classes from load_creator
SelfWeight = create_load.SelfWeight
DeadLoad = create_load.DeadLoad
LiveLoad = create_load.LiveLoad
SDL_Data = create_load.SDL_Data
SDL = create_load.SDL
LoadRecord = create_load.LoadRecord
LoadType = create_load.LoadType

def calculate_load(lr: LoadRecord, load_types: Optional[List[LoadType]] = None):
    """Use load_calculator to calculate the load."""
    return calc.total_load(lr, load_types)