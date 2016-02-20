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
        self.floors = {UP: set(), DOWN: set()}
        self.callbacks = None
        self.motor_direction = None

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        if 1 <= floor <= 6:
            if self.motor_direction:
                if self.motor_direction == UP and self.callbacks.current_floor < floor:
                    self.floors[direction].add(floor)
                    self.destination_floor = \
                    sorted(self.floors[self.motor_direction], reverse=self.motor_direction - 1)[0]
                elif self.motor_direction == DOWN and self.callbacks.current_floor > floor:
                    self.floors[direction].add(floor)
                    self.destination_floor = \
                    sorted(self.floors[self.motor_direction], reverse=self.motor_direction - 1)[0]
            else:
                if self.callbacks.current_floor < floor:
                    self.destination_floor = floor
                    self.floors[UP].add(floor)
                elif self.callbacks.current_floor > floor:
                    self.destination_floor = floor
                    self.floors[DOWN].add(floor)
        #print 'ques %s'%self.floors
                # print 'destination = %s'%self.destination_floor, self.floors

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        if 1 <= floor <= 6:
            if self.motor_direction:
                if self.motor_direction == UP and floor > self.callbacks.current_floor:
                    self.floors[UP].add(floor)
                    self.destination_floor = sorted(self.floors[UP])[0]
                elif self.motor_direction == DOWN and floor < self.callbacks.current_floor:
                    self.floors[DOWN].add(floor)
                    self.destination_floor = sorted(self.floors[DOWN])[0]
                    # self.destination_floor = floor
                else:
                    if floor > self.callbacks.current_floor:
                        self.floors[UP].add(floor)
                    elif floor < self.callbacks.current_floor:
                        self.floors[DOWN].add(floor)
            else:
                if floor > self.callbacks.current_floor:
                    self.motor_direction = UP
                    self.floors[UP].add(floor)
                elif floor < self.callbacks.current_floor:
                    self.motor_direction = DOWN
                    self.floors[DOWN].add(floor)
                self.destination_floor = floor

        #print 'ques %s'%self.floors

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """

        if self.destination_floor == self.callbacks.current_floor:
            #print 'ques %s'%self.floors
            # print 'flooer = %s'%self.floors[self.motor_direction]

            if self.floors[self.motor_direction]:
                self.floors[self.motor_direction].remove(self.destination_floor)
                try:
                    self.destination_floor = \
                    sorted(list(self.floors[self.callbacks.motor_direction]), reverse=self.motor_direction - 1)[0]
                except IndexError:
                    self.set_direction_and_destination()
            else:
                self.set_direction_and_destination()

            self.callbacks.motor_direction = None

    def set_direction_and_destination(self):
        if self.motor_direction == UP:
            try:
                self.destination_floor = sorted(list(self.floors[DOWN]), reverse=1)[0]
            except:
                self.motor_direction = None
        elif self.motor_direction == DOWN:
            try:
                self.destination_floor = sorted(list(self.floors[UP]))[0]
            except:
                self.motor_direction = None

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """

        if self.destination_floor > self.callbacks.current_floor:
            self.callbacks.motor_direction = UP
            self.motor_direction = UP
        elif self.destination_floor < self.callbacks.current_floor:
            self.callbacks.motor_direction = DOWN
            self.motor_direction = DOWN
