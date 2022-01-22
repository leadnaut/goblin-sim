#World Generation
TERRAIN_BOUNDS = {(0, 0.3):"Deep Ocean", 
                 (0.3, 0.45): "Medium Ocean",
                 (0.45, 0.5): "Shallow Ocean",
                 (0.5, 0.52): "Beach",
                 (0.52, 0.75): "Flatlands",
                 (0.75, 0.8): "Hills",
                 (0.8, 1.1): "Mountains"}

LAND_TERRAINS = ["Beach", "Flatlands", "Hills", "Mountains", "River", "Settlement", "Road"]
OCEAN_TERRAINS = ["Deep Ocean", "Medium Ocean", "Shallow Ocean", "Sea Route"]

TERRAIN_COLOURS = {"Deep Ocean": (2, 7, 93),
                  "Medium Ocean": (0, 65, 194),
                  "Shallow Ocean": (173, 216, 230),
                  "Beach": (220, 192, 139),
                  "Flatlands": (44, 109, 8),
                  "Hills": (68, 76, 56),
                  "Mountains": (58, 59, 60),
                  "River": (144, 204, 224),
                  "Settlement": (255, 0, 0),
                  "Road": (188, 74, 60),
                  "Sea Route": (116, 187, 251)}

#Path-finding
#Represents the relative costs of moving through a terrain type (higher => less likely to pathfind through)
PATH_COSTS = {"Deep Ocean": 25,
              "Medium Ocean": 20,
              "Shallow Ocean": 15,
              "Beach": 15,
              "Flatlands": 5,
              "Hills": 10,
              "Mountains": 15,
              "River": 15,
              "Settlement": 5,
              "Road": 0,
              "Sea Route": 0}

SETTLEMENT_DISTANCE = 20
ROAD_SEARCH_DISTANCE = 75
EMBARKMENT_COST = 40