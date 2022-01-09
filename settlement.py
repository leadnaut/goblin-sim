import world as w
import tools as tls
from typing import List, Tuple

class Settlement(object):
    def __init__(self, name:str, world: w.World, location: Tuple[int, int]) -> None:
        self.name = name
        self.world = world
        self.location = location
        self.tags = []

        self.population = []
        self.buildings = {}
        self.stores = {}
    
    def get_population_size(self) -> int:
        return len(self.population)
    
    def get_tags(self) -> List[str]:
        return self.tags

    def generate(self):
        pass

    def update(self):
        pass