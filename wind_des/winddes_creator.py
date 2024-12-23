from dataclasses import dataclass
from enum import Enum, auto

class WindStrClassEnum(Enum):
    """
    TYPE_1 refers to low rise roof structures up to 25 m height near the coast 
    (within 2 km from the sea), such as hangars and warehouses, to safeguard against uplift forces.\n
    TYPE_2 refers to all structures except the ones under item 1 above.
    """
    TYPE_1 = auto()
    TYPE_2 = auto()

@dataclass
class WindStrClass:
    class_enum: WindStrClassEnum

    z_val_list = [[0.003,1],[0.05,2]]
    z_vals = {WindStrClassEnum.TYPE_1: z_val_list[0],WindStrClassEnum.TYPE_2: z_val_list[1]}

    def get_z_vals(self) -> list:
        return self.z_vals[self.class_enum]