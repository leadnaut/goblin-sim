
from data import *
import png
import random as r
import heapq
from typing import List, Tuple

def hmap_to_png(world):
    pnglist = []
    hmap = world.get_hmap()
    for row in hmap:
        pngrow = []
        for hval in row:
            colour = int(255 * (1- hval))
            pngrow.append(colour)
        pnglist.append(pngrow)
    image = png.from_array(pnglist, "L")
    image.save(f"{world.get_name()}_hmap.png")


def world_to_png(world):
    pnglist = []
    tmap = world.get_tmap()
    hmap = world.get_hmap()
    settlement_poss = world.get_settlements_pos()
    for y, row in enumerate(tmap):
        pngrow = []
        for x, tval in enumerate(row):
            if (x,y) in settlement_poss.keys() or tval == "Settlement":
                settlement = settlement_poss[(x,y)]
                colour = settlement.get_country().get_colour()
                clist = list(colour)
            else:
                height = hmap[y][x]
                colour = TERRAIN_COLOURS.get(tval)
                clist = []
                for val in colour:
                    clist.append(max(min(int(val - 60 * height), 255),0))
            
            pngrow += clist
        pnglist.append(pngrow)
    image = png.from_array(pnglist, "RGB")
    image.save(f"{world.get_name()}_map.png")


def world_stats_dialog(world) -> None:
    print("World Analysis:")
    hmap = world.get_hmap()
    lowest = 1
    highest = 0
    for row in hmap:
        if min(row) < lowest:
            lowest = min(row)
        if max(row) > highest:
            highest = max(row)
    print("  Lowest Point:", lowest)
    print("  Highest Point:", highest)
    biome_tallies = {"Deep Ocean": 0,
                     "Medium Ocean": 0,
                     "Shallow Ocean": 0,
                     "Beach": 0,
                     "Flatlands": 0,
                     "Hills": 0,
                     "Mountains": 0,
                     "River": 0,
                     "Settlement": 0,
                     "Road": 0,
                     "Sea Route": 0}
    tmap = world.get_tmap()
    for row in tmap:
        for tval in row:
            biome_tallies[tval] += 1
    print("  Biome Tile Counts:")
    for name in biome_tallies.keys():
        print("   ", name +":", biome_tallies.get(name))
    
    print("Countries")
    countries = world.get_countries()
    i = 0
    options = {}
    for country in countries:
        print(i, "-", country.get_name())
        options[i] = country
        i += 1
    selection = 0
    while selection != "99":
        selection = input("Choose a country: ")
        country = options[int(selection)]
        print(f"Capital: {country.get_capital().get_name()}")
        print(F"Size: {country.get_size()}")
        settlements = country.get_settlements()
        for settlement in settlements:
            print(settlement.get_name())
        


### PATHFINDING
class Priority_Queue:
    def __init__(self) -> None:
        self.elements = [] #List of tuples of form [priority element]
    
    def is_empty(self) -> bool:
        return not self.elements
    
    def put(self, item, priority: float) -> None:
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> "t":
        return heapq.heappop(self.elements)[1]

def a_star_pathfinding(world, start: Tuple[int, int], 
    end: Tuple[int, int]) -> List[Tuple[int, int]]:
    frontier = Priority_Queue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.is_empty():
        current = frontier.get()

        if current == end:
            break
        
        for next in world.get_adjacents(current):
            new_cost = cost_so_far[current] + world.get_cost(current, next)
            #if space not already in path or if a better path into space found
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + world.distance(next, end)
                frontier.put(next, priority)
                came_from[next] = current
    
    #Rebuild path :)
    current = end
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    return path 


### OTHER TOOLS
def generate_name(sound_length: int) -> str:
    vowel_sounds = ["a", "e", "i", "o", "ai", "ee", "oa", "oi", "ow", "ar",
                    "ay", "ou", "ea", "aw", "ir", "ier", "oo", "or", "ur", "er",
                    "'"]

    consonant_sounds = ["b", "br", "c", "ck", "cr", "d", "dr", "f", "fr", "g", 
                        "gr", "h", "j", "k", "l", "m", "n", "p", "pr", "q", 
                        "qu", "s", "st", "sh", "t", "th", "tr", "v", "x", "z"]
    last = "v"
    name = ""
    for i in range(sound_length):
        if last == "v":
            name += r.choice(consonant_sounds)
            last = "c"
        else:
            name += r.choice(vowel_sounds)
            last = "v"
    return name.capitalize()
