
from openflexure_microscope.stage.sangaboardpi import SangaboardPi


s = SangaboardPi()
print("BEGIN")
s.move_rel([0., 0., 4096])
print("END")