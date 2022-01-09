import random as r
import time as t
import math as m
import opensimplex
from data import *
from typing import Tuple, List

class World(object):
    def __init__(self, name: str, width =  500, height = 500) -> None:
        self.name = name
        self._width = width
        self._height = height
        self._hmap = [[0 for i in range(width)] for i in range(height)]
        self._tmap = [["" for i in range(width)] for i in range(height)]

    def get_adjacents(self, qpos: Tuple[int, int]) -> List[Tuple[int, int]]:
        qx, qy = qpos
        xs = [max(qx - 1, 0), qx, min(qx + 1, self._width - 1)]
        ys = [max(qy - 1, 0), qy, min(qy + 1, self._height - 1)]
        adjacents = [(x,y) for x in xs for y in ys if (x,y) != qpos]
        return adjacents

    def get_hmap(self) -> List[List[int]]:
        return self._hmap
    
    def get_tmap(self) -> List[List[str]]:
        return self._tmap
    
    def get_name(self) -> str:
        return self.name

    def get_cost(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Returns 'cost' of moving between the two positions
        Used in path finding.
        """
        terrains = self.get_tvals([pos1, pos2])
        return (PATH_COSTS[terrains[0]] + PATH_COSTS[terrains[1]])/2
    
    def get_tvals(self, qposs: List[Tuple[int, int]]) -> List[str]:
        """
        Returns a list of the terrains of each of the positions in qposs
        """
        vals = []
        for qpos in qposs:
            x, y = qpos    
            vals.append(self._tmap[y][x])
        return vals
    
    def distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calculates the Euclidean distance between two points.
        Used as a close enough heuristic in pathfinding
        """
        x1, y1 = pos1
        x2, y2 = pos2
        return m.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def generate_terrain(self, rivers: int, river_distance: float) -> None:
        """
        Generates the world's terrain.
        Parameters:
            rivers(int): number of rivers to add
            river_distance(int): minimum distance between river start points
        """
        ### HEIGHT MAP
        print("Generating Height Map...")
        tic = t.perf_counter()
        hmap = self._hmap
        gen = opensimplex.OpenSimplex(seed = r.randint(1,1000))
        #Generate simplex noise over each tile
        for y, row in enumerate(hmap):
            for x in range(len(row)):
                row[x] = (0.8 * gen.noise2(x/75, y/75) +
                0.3 * gen.noise2(x/20 + 7, y/20 + 7))

                row[x] = max(min((row[x] + 1)/2, 1), 0) #Scale and clamp between 0 and 1
        self._hmap = hmap
        tmap = self._tmap
        toc = t.perf_counter()
        print(f"Done! ({toc - tic:0.4f} seconds)")
        
        ### TERRAIN MAP 
        print("Creating Terrain Map...")
        tic = t.perf_counter()
        #Classify each tile based on TERRAINBOUNDS
        for y, row in enumerate(hmap):
            for x, hval in enumerate(row):
                for bound in TERRAIN_BOUNDS:
                    if bound[0] <= hval < bound[1]:
                        tmap[y][x] = TERRAIN_BOUNDS.get(bound)
        toc = t.perf_counter()
        print(f"Done! ({toc - tic:0.4f} seconds)")

        ### RIVER GENERATION
        print("Generating Rivers...")
        fails = 0 #Fails are where river does not reach the ocean.
        tic = t.perf_counter()
        mountains = []
        stops = []
        #Find starting (mountains) and stopping points
        for y, row in enumerate(tmap):
            for x, tval in enumerate(row):
                if tval == "Mountains":
                    mountains.append((x,y))
                if tval == "Shallow Ocean":
                    stops.append((x,y))
                if x == 0 or y == 0 or x == self._width or y == self._height:
                    stops.append((x,y))

        river_starts = []
        for i in range(rivers):
            #Choose starting point sufficiently far away from other river starts
            distance = -1
            while distance < river_distance:
                pstart = r.choice(mountains)
                distances = []
                for start in river_starts:
                    distances.append(self.distance(pstart, start))
                distance = min(distances, default = 999)
            river_starts.append(pstart)

            #Start river algorithm until it hits the shallows (or gets stuck)
            cpos = pstart
            while cpos not in stops:
                cx, cy = cpos
                tmap[cy][cx] = "River"
                #Find the three lowest adjacent spaces
                cadjacents = self.get_adjacents(cpos)
                lowests = []
                for j in range(3):
                    lowest = cadjacents[0]
                    for apos in cadjacents:
                        if hmap[apos[1]][apos[0]] <= hmap[lowest[1]][lowest[0]]:
                            lowest = apos
                    cadjacents.remove(lowest)
                    lowests.append(lowest)
                
                #Add slight randomness to direction (stops straight line rivers)
                cpos = r.choice(lowests)
                #Check if river is about to loop and avoid it
                while tmap[cpos[1]][cpos[0]] == "River":
                    if len(lowests) != 0:
                        #Pick another one of the three lowests if possible
                        cpos = r.choice(lowests)
                        lowests.remove(cpos)
                    else:
                        #Pick any random direction not a river and go that way
                        if len(cadjacents) != 0:
                            cpos = r.choice(cadjacents)
                            cadjacents.remove(cpos)
                        else:
                            #if no adjacents are not rivers - stop
                            fails += 1
                            cpos = stops[0]
                        
        toc = t.perf_counter()
        print(f"Done! ({toc - tic:0.4f} seconds and {fails} fails out of {rivers} rivers)")
        
        ### SMOOTHING
        print("Smoothing Rivers...")
        tic = t.perf_counter()
        count = 0
        for y, row in enumerate(tmap):
            for x, tval in enumerate(row):
                if tval != "River":
                    adjacenttvals = self.get_tvals(self.get_adjacents((x,y)))
                    if adjacenttvals.count("River") >= 5:
                        tmap[y][x] = "River"
                        count += 1
        toc = t.perf_counter()
        print(f"Done! ({toc -tic:0.4f} seconds and {count} smoothings)")
        print("Terrain Generated!")
        self._tmap = tmap
