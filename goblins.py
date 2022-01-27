import world as w
from data import *
import tools as tls
import random as r

r.seed("countries")
test = w.World("test")
test.generate_terrain(75, 5)
test.generate_civilisation(1, 150)
tls.world_to_png(test)
tls.world_stats_dialog(test)