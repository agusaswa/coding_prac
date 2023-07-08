'''This library is for executing structe library.'''
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Load:
    name: str
    nature: str
    load_type: str
    load_val: float

    def create_dict(self) -> dict:
        load_record = {
            "name": self.name,
            "nature": self.nature,
            "load_type": self.load_type,
            "load_val": self.load_val
            }
        print(f"Load info: ***{self.name}*** is saved in the system!")
        return load_record
    
LOAD_PARAMS = {
    "nature": ["dead", "imposed"],
    "load_type": ["line","point"]
    }

class ParamsValidationStrategy(ABC):
    
    @abstractmethod
    def validate(self, params: any):
        pass
    
class LoadParamsValidation(ParamsValidationStrategy):
    def __init__(self, acceptable_val: list):
        self.acceptable_val = acceptable_val
    
    def validate(self, params:any):
        if params not in self.acceptable_val:
            raise ValueError("Invalid parameter!")

class Validator:
    def __init__(self):
        return None

    def validate_load_par(self, nature: str, load_type: str, nature_par: list, load_type_par: list):
        nature_par = LoadParamsValidation(nature_par)
        load_type_par = LoadParamsValidation(load_type_par)
        nature_par.validate(nature)
        load_type_par.validate(load_type)

class MultipleSequenceChecker(ABC):

    def __init__(self, next_checker=None):
        self.next_checker = next_checker
        self.type: str = None

    @abstractmethod
    def type_check(self, params: any):
        pass

    def handle_error(self, params: any):
        self.type_check(params)
        if self.next_checker:
            self.next_checker.handle_error(params)
            
class FloatTypeChecker(MultipleSequenceChecker):
    def __init__(self, next_checker):
        super().__init__(next_checker)
        self.type = "float"

    def type_check(self, params: any):

        if not isinstance(params, (float, int)):
            print("Not a float!")
            if self.next_checker is None: 
                raise TypeError(f"invalid parameter type! Expected parameter type is {self.type}.")
        super().type_check(params)


class IntTypeChecker(MultipleSequenceChecker):
        
    def __init__(self):
        self.type = "integer"

    def type_check(self, params: any):
        if not isinstance(params, int):
            if self.next_checker is None: 
                raise TypeError(f"invalid parameter type! Expected parameter type is {self.type}.")
        super().type_check(params)


class NoNegativeChecker(MultipleSequenceChecker):

    def __init__(self, next_checker):
        super().__init__(next_checker)

    def type_check(self, params: any):
        if params < 0:
            print("It is negative!")
            if self.next_checker is None: 
                raise ValueError("Invalid input value! Value cannot be negative.")
        else:
            super().type_check(params)
        
def store_load(name: str, nature: str, load_type: str, load_val: float) -> dict:
    '''This function is to store load information.'''
    check_par = Validator()
    check_par.validate_load_par(nature, load_type, LOAD_PARAMS["nature"], LOAD_PARAMS["load_type"])
    type_checker_2nd_round = NoNegativeChecker(None)
    type_checker_1st_round = FloatTypeChecker(type_checker_2nd_round)
    type_checker_1st_round.handle_error(load_val)
    load_obj = Load(name, nature, load_type, load_val)
    load_info = load_obj.create_dict()
    return load_info

if __name__ == "__main__":
    pass
    store_load("DL1_line","dead", "line", 50)
    store_load("DL1_line","wind", "line", 100)
    store_load("DL1_line","imposed", "triangular", 100)
    store_load("DL1_line","imposed", "point", "one hundred")
    store_load("DL1_line","imposed", "point", -20)