import atexit
import time
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
        (MJ added for sanity reasons...)
        
        One gear rotation moves 5.625 degrees.  The stepper motor is down geared by 64,
        i.e.: there is a 64:1 gear ratio so 360 degrees / (5.625/64) = 4096 total steps (or pulses)
        turns the stepper 360 degrees.  By pulse, I mean sending a digitalwrite(1) to one or two of the
        wires.

        So say I want to move the stage 7 steps_two_move (which perhaps would be better named half-steps).
        Notice the point about 8 half steps.  These refer to the step_sequences below.  The 7 half-steps then 
        doesn't make a gear rotation only an 1/8 step of a rotation....such fun....
        '''
        fWaitTime = 8/float(1000)
        steps_left = abs(steps_to_move)
        self.direction = 1 if steps_to_move > 0 else 0
        # Given the imprecise nature of the stepper motor, I chose to simplify here.  It wasn't working well
        # the way it was...
        while (steps_left > 0):
            if (self.direction == 1):
                 self.step_number += 1
                 if self.step_number == self.number_of_steps:
                    self.step_number = 0
            else:
                if self.step_number == 0:
                    self.step_number = self.number_of_steps
                self.step_number -= 1
            steps_left -=1
            # Get to the right step sequence -  which as you can see the input for the step sequence 
            # (self.number_of_steps) is initiatied to 0 in __init__...
            self.stepMotor(self.step_number % 8)
            time.sleep(fWaitTime)

        # time_since_last = 0
        # while (steps_left>0):
        #     now = datetime.datetime.now().microsecond
        #     time_since_last = now + self.last_step_time if (now < self.last_step_time) else now - self.last_step_time
        #     # move only if the appropriate delay has passed
        #     if time_since_last >= self.step_delay:
        #         # get the timestamp of when the step is taken
        #         self.last_step_time = now
        #         if (self.direction == 1):
        #             self.step_number += 1
        #             if self.step_number == self.number_of_steps:
        #                 self.step_number = 0
        #         else:
        #             if self.step_number == 0:
        #                 self.step_number = self.number_of_steps
        #         # Decrement the steps left.
        #         steps_left -= 1
        #         self.stepMotor(self.step_number % 8)
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


        