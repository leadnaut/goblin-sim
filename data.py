#World Generation
TERRAIN_BOUNDS = {(0, 0.3):"Deep Ocean", 
                 (0.3, 0.45): "Medium Ocean",
                 (0.45, 0.5): "Shallow Ocean",
                 (0.5, 0.51): "Beach",
                 (0.51, 0.75): "Flatlands",
                 (0.75, 0.8): "Hills",
                 (0.8, 1.1): "Mountains"}

TERRAIN_COLOURS = {"Deep Ocean": (2, 7, 93),
                  "Medium Ocean": (0, 65, 194),
                  "Shallow Ocean": (173, 216, 230),
                  "Beach": (220, 192, 139),
                  "Flatlands": (126, 200, 80),
                  "Hills": (68, 76, 56),
                  "Mountains": (58, 59, 60),
                  "River": (144, 204, 224),
                  "Settlement": (255, 0, 0),
                  "Road": (255, 255, 255),
                  "Sea Route": (255, 255, 255)}

#Path-finding
#Represents the relative costs of moving through a terrain type (higher => less likely to pathfind through)
PATH_COSTS = {"Deep Ocean": 10,
              "Medium Ocean": 6,
              "Shallow Ocean": 5,
              "Beach": 3,
              "Flatlands": 1,
              "Hills": 2,
              "Mountains": 3,
              "River": 3,
              "Settlement": 1,
              "Road": 0}

SETTLEMENT_DISTANCE = 20
