from data import *
import png

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


def tmap_to_png(world):
    pnglist = []
    tmap = world.get_tmap()
    for row in tmap:
        pngrow = []
        for tval in row:
            colour = TERRAINCOLOURS.get(tval)
            pngrow += list(colour)
        pnglist.append(pngrow)
    image = png.from_array(pnglist, "RGB")
    image.save(f"{world.get_name()}_tmap.png")

def world_stats(world):
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