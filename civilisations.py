from itertools import count
import world as w
import tools as tls
from typing import List, Tuple
class Country(object):
    def __init__(self, name:str, colour: Tuple[int]) -> None:
        self.name = name
        self.colour = colour
        

class Settlement(object):
    def __init__(self, name:str, world: "w.World", position: Tuple[int, int]) -> None:
        self.name = name
        self.world = world
        self.position = position
        self.tags = []
        self.country = None
        self.population = []
        self.buildings = {}
        self.stores = {}
    
    def get_population_size(self) -> int:
        return len(self.population)
    
    def get_position(self) -> Tuple[int, int]:
        return self.position
    
    def get_tags(self) -> List[str]:
        return self.tags
    
    def get_country(self) -> str:
        return self.country

    def set_country(self, country:Country) -> None:
        self.country = country

    def generate(self):
        pass

    def update(self):
        pass
    
    def __repr__(self) -> str:
        return "Settlement(" + self.name + ")"