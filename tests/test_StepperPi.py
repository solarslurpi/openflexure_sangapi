import time
import pytest
from openflexure_microscope.stage.stepperpi import Stepper

# Run pytest -s test_StepperPi.py
# the -s option shows print() output.d
@pytest.fixture
def xStepper():
    xStepper = Stepper(8,12, 15, 11, 13)
    return xStepper
 
@pytest.fixture
def yStepper():
    yStepper = Stepper(8, 37, 35, 33, 31)
    return yStepper

@pytest.fixture
def zStepper():
    zStepper = Stepper(8, 40, 38, 36, 32)
    return zStepper

@pytest.fixture
def fWaitTime():
    fWaitTime = 8/float(1000)
    return fWaitTime

def test_version_number(xStepper):
    # This test was run on version 0. Versions are integer numbers.
    assert xStepper.version() == 0
    

def test_version_type(xStepper):
    assert isinstance(xStepper.version(),int)

def test_x_set_speed(xStepper):
    step_delay_at_15RPM =  60 * 1000 * 1000 /xStepper.number_of_steps / 15
    xStepper.setSpeed(15)
    assert xStepper.step_delay == step_delay_at_15RPM

def test_x_one_rotation(xStepper,fWaitTime):
    print('Testing X rotation - watch for a full rotation of the x-axis motor.')
    for i in range(4096):
        xStepper.stepMotor(i % 8)
        time.sleep(fWaitTime)

def test_y_one_rotation(yStepper,fWaitTime):
    print('Testing Y rotation - watch for a full rotation of the x-axis motor.')
    for i in range(4096):
        yStepper.stepMotor(i % 8)
        time.sleep(fWaitTime)

def test_z_one_rotation(zStepper,fWaitTime):
    print('Testing Z rotation - watch for a full rotation of the x-axis motor.')
    for i in range(4096):
        zStepper.stepMotor(i % 8)
        time.sleep(fWaitTime)
