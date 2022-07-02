
import json
from datetime import datetime
from openflexure_microscope.stage.stepperpi import Stepper
# Create the 3 Stepper motor instances.  This requires all pins defined and tested.
# Set steps remaining for each motor to 0.


class SangaboardPi(Stepper):

    # The names of the sangaboard's axes.  NB this also defines the number of axes
    axis_names = ("x", "y", "z")

    def __init__(self):
        self.motors = []
        self.n_motors = 3
        # x-axis stepper motor
        self.motors.append(Stepper(8, 12, 15, 11, 13))
        # y-axis stepper motor
        self.motors.append(Stepper(8, 37, 35, 33, 31))
        # z-axis stepper motor
        self.motors.append(Stepper(8, 40, 38, 36, 32))
        self.steps_remaining = [0 for _ in range(self.n_motors)]
        self.min_step_delay = 0
        self.current_position = []
        try:
            with open('/var/openflexure/application/openflexure-microscope-server/openflexure_microscope/stage/sangaboardpiconfig.json') as config_file:
                data = json.load(config_file)
                self._min_step_delay = data['min_step_delay']
                self.current_position = data['current_position']
                print(self.current_position)
        except FileNotFoundError:
            # TODO: More robust no file error handling
            pass


    def list_modules(self):
        """Return a list of strings detailing optional modules.

        Each module will correspond to a string of the form ``Module Name: Model

        MJ: NOT IMPLEMENTED.
        """
        return["No optional modules."]

    def move_abs(self, final, **kwargs):
        """Make an absolute move to a position

        NB the sangaboard only accepts relative move commands, so this first
        queries the board for its position, then instructs it to make about
        relative move.
        """
        rel_mov = [f_pos - i_pos for f_pos, i_pos in zip(final, self.position)]
        return self.move_rel(rel_mov, **kwargs)
        

    def move_abs(self,final, **kwargs):
        pass

    def move_rel(self,displacement,axis=None):
        pass

    def move_rel(self, displacement, axis=None):
        """Make a relative move.

        displacement: integer or array/list of 3 integers
        axis: None (for 3-axis moves) or one of 'x','y','z'
        """
        
        if axis is not None:
            assert axis in self.axis_names, "axis must be one of {}".format(
                self.axis_names
            )
            self.query("mr{} {}".format(axis, int(displacement)))
        else:
            # TODO: assert displacement is 3 integers
            self.query("mr {} {} {}".format(*list(displacement)))
    def position(self):
        # TODO
        pass

    def mrx(self, n_steps):
        self._move_axis(0 ,n_steps)

    def _move_axis(self, axis, n_steps):
        displacement = [0 for _ in range(self.n_motors) ]
        displacement[axis] = n_steps
        self.move_axes(displacement)


    def move_axes(self,disp):
        direction = [(1 if disp[i] > 0 else 0) for i in disp]
        displacement = [disp[i]*dir[i] for i in disp]
        max_steps = 0.0
        # Scale the step delays so the move goes in a straight line, with >= 1 motor
        # running at max. speed.
        step_delay = [(max_steps/displacement[i]*self._min_step_delay if displacement[i] > 0 else 999999999) for i in range(self.n_motors)]
        # Actually make the move.
        distanced_moved = [0 for _ in range(self.n_motors)]
        start = datetime.now().microsecond
        final_scaled_t = max_steps * self._min_step_delay
        finished = False
        # while not finished:
        #     endstop_break = 0
        #     endstop_break = [( dir[i]*(i+1) if endstoppedTriggered() ) for i in range(self.n_motors)]



    def stepMotor(self, motor, dx):
        self.current_pos[motor] += dx
        self.motors[motor].stepMotor(((self.current_pos[motor] % 8) + 8 ) % 8)  # If it was me, I'd just do % 8 but this is how the Arduino code handles it...
        

    def releaseMotor(self, motor):
        self.motors[motor].release()

    def close(self):
        # Not using a serial interface. No port to close.
        pass

    def position(self):
        print(f" {self.current_position[0]} {self.current_position[1]} {self.curret_position[3]}")
        return

    def get_min_step_delay(self):
        return self._min_step_delay
    
    def set_min_step_delay(self,value):
        self._min_step_delay = value
        return

    min_step_delay = property(get_min_step_delay,set_min_step_delay)
    


