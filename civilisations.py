from itertools import count
import world as w
import tools as tls
from typing import List, Tuple

class Country(object):
    def __init__(self, name:str, world: "w.World", colour: Tuple[int]) -> None:
        self.name = name
        self.colour = colour
        self.world = world
        self.settlements = []
        self.capital = None
    
    def add_settlement(self, settlement: "Settlement"):
        self.settlements.append(settlement)
        if "Capital" in settlement.get_tags():
            self.capital = settlement
        
    def get_name(self)-> str:
        return self.name
    
    def get_colour(self) -> Tuple[int, int, int]:
        return self.colour
    
    def get_size(self) -> int:
        return len(self.settlements)
    
    def get_capital(self):
        return self.capital
    
    def get_settlements(self):
        return self.settlements


class Settlement(object):
    def __init__(self, name:str, world: "w.World", position: Tuple[int, int]) -> None:
        self.name = name
        self.world = world
        self.position = position
        self.tags = []
        self.country = None
        self.population = []
        self.stores = {}
    
    def get_name(self) -> str:
        return self.name
    
    def get_population_size(self) -> int:
        return len(self.population)
    
    def get_position(self) -> Tuple[int, int]:
        return self.position
    
    def get_tags(self) -> List[str]:
        return self.tags
    
    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)
    
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