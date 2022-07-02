import atexit
import datetime
import RPi.GPIO as GPIO

class Stepper:
    def __init__(self, number_of_steps,motor_pin_1, motor_pin_2, motor_pin_3, motor_pin_4):
        atexit.register(self._cleanup)
        self.step_number = 0
        self.direction = 0 # 1 = clockwise
        self.last_step_time = 0 # time stamp in us of the last step taken
        self.number_of_steps = number_of_steps # 8 is the number of steps for half-step of 28BYJ-40 steppers
        self.motor_pins = [motor_pin_1,motor_pin_2,motor_pin_3, motor_pin_4]
        self.setSpeed(10) # Start with an RPM of 10.  setSpeed sets the step_delay based on the requested RPM.
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        # Set the four motor pins to output and initialize to 0 V (False)
        for pin in self.motor_pins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin,False)
        return


    def _cleanup(self):
        GPIO.cleanup()
        return

    def board(self):
        return "Raspberry Pi"

    def firmware(self):
        return "0.0"

        
    def step(self,steps_to_move):
        '''Move the motor 1 half step.  there are 8 half steps in one gear rotation.
        '''
        
        steps_left = abs(steps_to_move)
        self.direction = 1 if steps_to_move > 0 else 0
        time_since_last = 0
        while (steps_left>0):
            now = datetime.datetime.now().microsecond
            time_since_last = now + self.last_step_time if (now < self.last_step_time) else now - self.last_step_time
            # move only if the appropriate delay has passed
            if time_since_last >= self.step_delay:
                # get the timestamp of when the step is taken
                self.last_step_time = now
                if (self.direction == 1):
                    self.step_number += 1
                    if self.step_number == self.number_of_steps:
                        self.step_number = 0
                else:
                    if self.step_number == 0:
                        self.step_number = self.number_of_steps
                # Decrement the steps left.
                steps_left -= 1
                self.stepMotor(self.step_number % 8)
        return



    def stepMotor(self,thisStep):


        # It easier to see how the motor is energized to move around if we look at
        # the half-step sequences.  A full revolution of the motor takes 8 steps.
        step_sequences = [
            [1,0,0,1],
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1]
        ]
        # print(f'step number: {thisStep}')
        # Stepper coils are energized if the GPIO pin associated with the coil is set to 1.
        for i in range(4): # 4 GPIO pins
            # thisStep is between 0 and 7.  These are the 8 half-steps.
            GPIO.output(self.motor_pins[i],step_sequences[thisStep][i])
        return

    def setSpeed(self,whatSpeed):
        self.step_delay = 60 * 1000 * 1000 /self.number_of_steps / whatSpeed
        # might as well return the value...although perhaps doing so is confusing.
        return self.step_delay

    def version(self):
        return 0

    def releaseMotor(self,which_motor):
        self.assertIn(which_motor,range(self.n_motors)) # Make sure which motor is between 0 and n_motors (usually, always? x, y, and z)
        for i in range(4):
            GPIO.output(self.motor_pins[i],0)
        return


        