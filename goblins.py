import world as w
from data import *
import tools as tls

test = w.World("test")
test.generate_terrain(75, 5)
tls.tmap_to_png(test)
tls.hmap_to_png(test)