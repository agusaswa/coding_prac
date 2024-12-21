from dataclasses import dataclass
from enum import Enum,auto
import csv

class SectTypeEnum(Enum):
    UC = auto()
    CHS = auto()


@dataclass
class Grade:
    yield_str: float
    tensile_str: float
    E: float
    v: float

@dataclass
class Sect_UC:
    b: float
    h: float
    t_f: float
    t_w: float

@dataclass
class Sect_CHS:
    ext_dia: float
    t: float

@dataclass
class SectionFromDatabase:
    name: str
    type: SectTypeEnum
    sect_data: object
    grade: Grade

    @staticmethod
    def _get_params_from_csv(section_type_enum: SectTypeEnum, sect_name:str) -> object:
        param_mapping = {
            SectTypeEnum.UC: ['b','h','t_f','t_w'],
            SectTypeEnum.CHS: ['ext_dia','t']
        }

        with open('sect_data.csv','r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Section Type'] == section_type_enum.name and row['Name'] == sect_name:
                    params = {param: float(row[param]) for param in param_mapping[section_type_enum] if row[param]}
                    return params
                
    @staticmethod
    def _create_section_from_enum(section_type_enum: SectTypeEnum, sect_params: dict) -> object:
        sect_type_mapping={
            SectTypeEnum.UC: Sect_UC,
            SectTypeEnum.CHS: Sect_CHS
        }

        section_type_class = sect_type_mapping.get(section_type_enum)
        
        return section_type_class(**sect_params)

    @classmethod
    def create(cls,section_type_enum: SectTypeEnum,section_name: str,grade: Grade):
        sect_params = cls._get_params_from_csv(section_type_enum,section_name)
        section_data = cls._create_section_from_enum(section_type_enum,sect_params)
        return cls(name=section_name,sect_data=section_data,type=section_type_enum,grade=grade)