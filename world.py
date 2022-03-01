from numpy import seterrcall
import tools as tls
import civilisation as c
from data import *

import random as r
import time as t
import math as m
import opensimplex
from typing import Dict, Tuple, List

class World(object):
    def __init__(self, name: str, width =  500, height = 500) -> None:
        self.name = name
        self._width = width
        self._height = height
        self._hmap = [[0 for i in range(width)] for i in range(height)]
        self._tmap = [["" for i in range(width)] for i in range(height)]
        self._countries = []
        self._settlements = []

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
    
    def get_settlements(self) -> str:
        return self._settlements

    def get_settlements_pos(self) -> Dict[tuple, c.Settlement]:
        dictionary = {}
        for settlement in self._settlements:
            dictionary[settlement.get_position()] = settlement
        return dictionary
    
    def get_countries(self):
        return self._countries

    def get_cost(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Returns 'cost' of moving between the two positions
        Used in path finding.
        """
        cost = 0
        terrains = self.get_tvals([pos1, pos2])
        heights = self.get_hvals([pos1, pos2])
        if ("Settlement" not in terrains and 
            len([h for h in heights if h <= OCEAN_CUTOFF]) == 1):
            #If exactly 1 of the two terrains is land add a en/disembark fee
            cost = EMBARKMENT_COST
        return (PATH_COSTS[terrains[0]] + PATH_COSTS[terrains[1]])/2 + cost + 100 * abs(heights[0] - heights[1])
    
    def get_tvals(self, qposs: List[Tuple[int, int]]) -> List[str]:
        """
        Returns a list of the terrains of each of the positions in qposs
        """
        vals = []
        for qpos in qposs:
            x, y = qpos    
            vals.append(self._tmap[y][x])
        return vals
    
    def get_hvals(self, qposs: List[Tuple[int, int]]) -> List[str]:
        """
        Returns a list of the terrains of each of the positions in qposs
        """
        vals = []
        for qpos in qposs:
            x, y = qpos    
            vals.append(self._hmap[y][x])
        return vals
    
    def distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calculates the Euclidean distance between two points.
        Used as a close enough heuristic in pathfinding
        """
        x1, y1 = pos1
        x2, y2 = pos2
        return m.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

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

    def generate_civilisation(self, num_countries: int, num_settlements: int) -> None:
        """
        Generates settlements and countries into the world
        Parameters:
            num_countries = number of countries to group settlements into
            num_settlements = number of settlements
        """
        #Cities will either be next to river or surrounded by at least 4 grassland tiles
        print("Finding potential settlement locations...")
        tic = t.perf_counter()
        settlement_poss = []
        scores = []
        tmap = self.get_tmap()
        for y, row in enumerate(tmap):
            for x, tval in enumerate(row):
                if tval not in ["River", "Shallow Ocean", "Medium Ocean", "Deep Ocean"]:
                    adj_tvals = self.get_tvals(self.get_adjacents((x,y)))
                    if "River" in adj_tvals or adj_tvals.count("Flatlands") + adj_tvals.count("Beach") >= 4:
                        score = adj_tvals.count("Flatlands")
                        score += adj_tvals.count("River") * 50
                        score += adj_tvals.count("Shallow Ocean") * 10
                        settlement_poss.append((x,y))
                        scores.append(score)
        toc = t.perf_counter()
        print(f"Done! ({toc - tic:0.4f} seconds, {len(settlement_poss)} locations found)")

        print("Choosing settlement locations...")
        tic = t.perf_counter()
        for i in range(num_settlements):
            if settlement_poss:
                distance = -1
                while distance < SETTLEMENT_DISTANCE:
                    spos = r.choices(settlement_poss, weights = scores)[0]
                    distances = []
                    for settlement in self._settlements:
                        pos = settlement.get_position()
                        distances.append(self.distance(spos, pos))
                    distance = min(distances, default = 999)
                name = tls.generate_name(4)
                settlement = c.Settlement(name, self, spos)
                self._tmap[spos[1]][spos[0]] = "Settlement"
                self._settlements.append(settlement)
        toc = t.perf_counter()
        print(f"Done! ({toc - tic:0.4f} seconds)")

        print("Building Roads...")
        tic = t.perf_counter()
        #For each settlement pathfind to close (not all - it takes way too long) settlements
        road_count = 0
        roads = [] #List of tuples pf connected settlements
        for start in self._settlements:
            close_ends = [x for x in self._settlements if self.distance(start.get_position(), x.get_position()) < ROAD_SEARCH_DISTANCE ]
            for end in close_ends:
                if start != end and (start, end) not in roads and (end, start) not in roads:
                    roads.append((start, end))
                    path = tls.a_star_pathfinding(self, start.get_position(), end.get_position())
                    road_count += 1                   
                    for pos in path:
                        tval = self.get_tvals([pos])[0]
                        if tval == "Settlement":
                            if pos != path[0]:
                                #Add road to register (should cut down on duplicates)
                                for settlement in self._settlements:
                                    if settlement.get_position() == pos:
                                        break
                                    roads.append((start, settlement))
                                break
                        else:
                            if tval in LAND_TERRAINS:                          
                                self._tmap[pos[1]][pos[0]] = "Road"
                            else:
                                self._tmap[pos[1]][pos[0]] = "Sea Route"
        toc = t.perf_counter()
        print(f"Done! ({toc - tic:0.4f} seconds, and {road_count} roads found)")
        
        print("Cleaning up ports...")
        tic = t.perf_counter()
        count = 0
        for y, row in enumerate(self._tmap):
            for x, tval in enumerate(row):
                if tval == "Road":
                    adjacents = self.get_adjacents((x,y))
                    atval = self.get_tvals(adjacents)
                    if "Sea Route" in atval and "Settlement" not in atval:
                        count += 1
                        name = tls.generate_name(4)
                        settlement = c.Settlement(name, self, (x,y))
                        self._settlements.append(settlement)
                        self._tmap[y][x] = "Settlement"
        toc = t.perf_counter()
        print(f"Done! ({toc - tic:0.4f} seconds, and {count} ports added)")

        print("Creating Countries...")
        tic = t.perf_counter()
        #Pick a random settlement to make a capital
        settlements = self._settlements.copy()
        while settlements:
            country = c.Country(tls.generate_name(6), self, r.choice(COUNTRY_COLOURS))
            self._countries.append(country)
            capital = r.choice(settlements)
            capital.add_tag("Capital")
            for settlement in settlements:
                if self.distance(settlement.get_position(), capital.get_position()) < 150:
                    settlement.set_country(country)
                    country.add_settlement(settlement)
                    settlements.remove(settlement)          

        toc = t.perf_counter()
        print(f"Done! ({toc-tic:0.4f} seconds)")
        print("Generating settlements...")
        tic = t.perf_counter()
        for settlement in self._settlements:
            settlement.generate()
        toc = t.perf_counter()
        print(f"Done! ({toc-tic:0.4f} seconds)")
                        