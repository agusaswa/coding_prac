import pandas as pd

class Section:
    def __init__(self, sect_data: pd.DataFrame) -> None:
        if not isinstance(sect_data, pd.DataFrame):
            raise ValueError("Section data must be a pandas Dataframe.")
        if "Size" not in sect_data.columns:
            raise ValueError("Section data must have a 'Size' column.")
        
        self._sect_data = sect_data
        self._sect_label = None

    @property
    def sect_label(self):
        return self._sect_label
    
    @sect_label.setter
    def sect_label(self, label: str) -> str:
        if label not in self._sect_data['Label'].values:
            raise ValueError(f"{label} is not a valid section label or not in the database.")
        self._sect_label = label

    def calc_flange_class(self):
        return None

    

