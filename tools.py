from data import *
import png
import random as r
import heapq
from typing import List, Tuple

def hmap_to_png(world: "World"):
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

def world_to_png(world: "World"):
    pnglist = []
    cmap = world.get_tmap()
    for y, row in enumerate(cmap):
        pngrow = []
        for x, tval in enumerate(row):
            colour = TERRAIN_COLOURS.get(tval)
            pngrow += list(colour)
        for i, cval in enumerate(pngrow):
            pngrow[i] = min(max(int(cval + r.normalvariate(0,2)), 0), 255)
        pnglist.append(pngrow)
    image = png.from_array(pnglist, "RGB")
    image.save(f"{world.get_name()}_tmap.png")

def world_stats(world: "World"):
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
                     "River": 0}
    tmap = world.get_tmap()
    for row in tmap:
        for tval in row:
            biome_tallies[tval] += 1
    print("  Biome Tile Counts:")
    for name in biome_tallies.keys():
        print("   ", name +":", biome_tallies.get(name))


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

def a_star_pathfinding(world: "World", start: Tuple[int, int], 
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
