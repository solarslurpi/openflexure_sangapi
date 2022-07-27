import time
import pytest
from openflexure_microscope.stage.sangaboardpi import SangaboardPi

# Run pytest -s test_sangaboardPi.py
# the -s option shows print() output.d
@pytest.fixture
def sangaboard():
    sangaboard = SangaboardPi()
    return sangaboard
#     xStepper = Stepper(8,12, 15, 11, 13)
#     return xStepper
def test_initial_move(sangaboard):
    # move the z-axis 180 degrees in the positive direction
    sangaboard.move_rel([0., 0., 180.])
    # First move asked for...
    # see
    #   # Make the main movement
    #         self.board.move_rel(initial_move)
    # in sangapi.py
    # e.g.: go to Navigate enter 8 for y initial_move = [0., 0., 8.]

