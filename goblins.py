import world as w
from data import *
import tools as tls

test = w.World(500, 500, "name")
test.generate_terrain()
tls.tmap_to_png(test)
tls.hmap_to_png(test)