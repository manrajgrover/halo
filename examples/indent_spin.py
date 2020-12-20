from halo import Halo
from time import sleep

with Halo(text="Look at that bullet!", indent=" • ") as s:
    sleep(1)
    s.succeed()

