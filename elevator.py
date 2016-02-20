UP = 1
DOWN = 2
FLOOR_COUNT = 6

class ElevatorLogic(object):
    """
    An incorrect implementation. Can you make it pass all the tests?

    Fix the methods below to implement the correct logic for elevators.
    The tests are integrated into `README.md`. To run the tests:
    $ python -m doctest -v README.md

    To learn when each method is called, read its docstring.
    To interact with the world, you can get the current floor from the
    `current_floor` property of the `callbacks` object, and you can move the
    elevator by setting the `motor_direction` property. See below for how this is done.
    """

    def __init__(self):
        # Feel free to add any instance variables you want.
        self.destination_floor = None
        self.direction = None
        self.floors = {UP:set(), DOWN:set()}
        self.callbacks = None

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        if 1 <= floor <= 6:
            self.floors[direction].add(floor)

            if not self.direction:
                self.callbacks.motor_direction(direction)
                self.destination_floor = list(self.floors[direction]).sort()[0]
            else:
                self.destination_floor = list(self.floors[direction]).sort(reverse=self.callbacks.motor_direction-1)[0]

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        if 1 <= floor <= 6:
            if self.callbacks.motor_direction -1:
                if floor > self.callbacks.current_floor:
                    self.floors[self.callbacks.motor_direction].add(floor)
            else:
                if floor < self.callbacks.current_floor:
                    self.floors[self.callbacks.motor_direction].add(floor)

            self.destination_floor = floor

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        if self.destination_floor == self.callbacks.current_floor:
            self.floors[self.direction].pop(self.destination_floor)
            if self.floors[self.direction]:
                self. destination_floor  = list(self.floors[self.callbacks.motor_direction]).sort(reverse=self.direction-1)[0]
            elif self.callbacks.motor_direction == UP:
                self.destination_floor = list(self.floors[DOWN]).sort(reverse=1)[0]
            elif self.callbacks.motor_direction == DOWN:
                self.destination_floor = list(self.floors[UP]).sort()[0]
            self.callbacks.motor_direction = None




    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        if self.destination_floor > self.callbacks.current_floor:
            self.callbacks.motor_direction = UP
        elif self.destination_floor < self.callbacks.current_floor:
            self.callbacks.motor_direction = DOWN
