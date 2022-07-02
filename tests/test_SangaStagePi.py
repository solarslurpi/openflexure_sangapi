
import pytest

from openflexure_microscope.stage.sangaboardpi import SangaboardPi

def test_SangaboardPi_instantiation():
    assert SangaboardPi() != None