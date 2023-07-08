'''This library is for executing structe library.'''
from dataclasses import dataclass

@dataclass
class Load:
    name: str
    nature: str
    load_type: str
    load_val: float

    def record(self) -> dict:
        load_record = {
            "name": self.name,
            "nature": self.nature,
            "load_type": self.load_type,
            "load_val": self.load_type
            }
        return load_record

def store_load(name: str, nature: str, load_type: str, load_val: float) -> dict:
    '''This function is to store load information.'''
    load_obj = Load(name, nature, load_type, load_val)
    load_info = load_obj.record()
    return load_info
    
def access_load():
    '''This function is to show the stored load in Markdown.'''
    pass