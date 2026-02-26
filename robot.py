from environment import Environment
from robot_logic import RobotLogicSystem
import random

class Robot():

    def __init__(self, position: tuple, ori: str, charge: int, env: object):        
        self.logic = RobotLogicSystem()
        self.setup_logic_rules()        
        self.enviroment = env
        self.battery = charge
        self.position = position
        self.decision = None
        self.senser_values = self.sense()
        self.orientation = ori
        self.last_action = None
        self.counter = 0

    def setup_logic_rules(self):
        """
        Expert System logic / rules        
        """
        # Clean current cell if dirty
        self.logic.add_rule(["current_cell_dirty"], "clean")

        # Battery dead. End program
        self.logic.add_rule(["battery_dead"], "battery_dead")

        # Move forward if Filth is present
        self.logic.add_rule(["front_dirty", "battery_ok"], "move_forward")

        # Rotate to closest Filth
        self.logic.add_rule(["north_dirty", "battery_ok"], "rotate_north")
        self.logic.add_rule(["east_dirty", "battery_ok"], "rotate_east")
        self.logic.add_rule(["south_dirty", "battery_ok"], "rotate_south")
        self.logic.add_rule(["west_dirty", "battery_ok"], "rotate_west")

        # Prioritise Clear
        # Move Forward
        self.logic.add_rule(["front_clear", "battery_ok"], "move_forward")

        # Rotate
        self.logic.add_rule(["north_clear", "battery_ok"], "rotate_north")
        self.logic.add_rule(["east_clear", "battery_ok"], "rotate_east")
        self.logic.add_rule(["south_clear", "battery_ok"], "rotate_south")
        self.logic.add_rule(["west_clear", "battery_ok"], "rotate_west")

        # Last resort
        # Randomly move
        self.logic.add_rule(["surrounded", "spin_to_win", "battery_ok"], "random_direction")
        self.logic.add_rule(["surrounded", "on_to_glory", "battery_ok"], "random_keep_swimming")


    def charge_consumption(self, usage: int) -> bool:
        """
        Update the charge value for the robot on usage input
        """
        if self.battery <= 0:
            self.battery = 0
            return False

        self.battery -= usage
        if self.battery < 0:
            self.battery = 0

        return True

    def sense(self):
        """
        Get values around the robot, store within self.values
            Expected values : dict (str of values, north, east, south, west 
                                and current value of input pos) 
                OR None
        """
        self.senser_values = self.enviroment.get_cells(self.position)


    def decide(self) -> str:
        """
        Cycle through senser_values for clean or move logic
                Order of operations
                    - clean (if POS is filth)
                    - check for any 'filthy' tiles to clean
                        - if front filth, move
                        - else rotate to filth (n,e,s,w order)
                    - Move forward if no collision
                        - if collision infront, 
                            randomly rotate to non-collision
                
        :return: str: the decision, move, clean or rotate (north, east, south, west)
        """

        # Pass facts from sensors/battery
        self.logic.reset_facts()
        self.logic.update_facts_from_sensors(self.senser_values, self.orientation)
        self.logic.update_battery_life(self.battery)
        self.logic.update_last_action(self.last_action)

        # Decide on action
        return self.logic.decide_action()

    def move(self):
        """
        Move robot forward 1 place
        """
        
        # get new pos for move
        new_pos = self.movement_lookup(self.ori_lookup(self.orientation))
        
        # attempt move
        self.position = self.enviroment.move_robot(new_pos, self.orientation)

        if self.position == new_pos:
            self.last_action = 'moved'
        else:
            self.last_action = 'crash!!!'


    def rotate(self):
        """
        Rotate robot
        """
        # update robot
        self.orientation = self.ori_lookup(self.decision.split("_")[1])

        # update env
        self.enviroment.robot_ori = self.ori_lookup(self.decision.split("_")[1])
        x, y = self.position
        self.enviroment.world[y][x] = self.orientation


    def act(self):
        """
        Run sensers and call decide function. Compare all results and commit to an action
        
        """
        if self.battery <= 0:
            return

        self.sense()
        self.decision = self.decide()

        if "clean" in self.decision:
            self.enviroment.clear_cell(self.position)
            self.last_action = 'cleaned'
        
        elif "move" in self.decision:
            self.move()

        elif "rotate" in self.decision:
            self.rotate()
            self.last_action = 'rotated'
        
        elif "random" in self.decision:
            
            if "keep_swimming" in self.decision:
                self.move()
            else:
                directions = ["north", "east", "south", "west"]
                random.shuffle(directions)

                self.decision = f"random_{directions[0]}"
                self.rotate()
                self.last_action = "random_direction"
        
        self.counter += 1
        self.charge_consumption(1)

    def movement_lookup(self, direction) -> tuple:
        """
        Input direction, north, west ... etc. Return self.position movement in that direction
                        as tuple value

        :param: str direction = north, west, east, south
        :return: tuple   x, y for respective movement
        """
        x, y = self.position
       
        movement_dict = {
            "north": (x, y-1),
            "south": (x, y+1),
            "west": (x-1, y),
            "east": (x+1, y)
        }        

        return movement_dict[direction]


    def ori_lookup(self, input_dir) -> str:
        """
        Change dir into robot direction symbol

        :param: str dir, expected values north, east, south, west
        :return: str   values "^", "v", "<", ">"
        """

        directions = {
            "north": "^",
            "south": "v",
            "west": "<",
            "east": ">"
        }

        # reverse mapping
        directions.update({v: k for k, v in directions.items()})
        
        return directions[input_dir]
    

    def __str__(self):
        """
        Output messages
        """

        if "battery_dead" not in self.decision:
            curr_sensers = self.enviroment.get_cells(self.position)            
        else:
            curr_sensers = "Connection Lost"

        return (
            f"\n        -- Robot Data -- \n"
            f"Position                  :   {self.position} \n"
            f"Facing                    :   {self.orientation} \n"
            f"Current Sensor Values     :   {curr_sensers} \n\n"

            f"Last Sensor Values        :   {self.senser_values} \n"
            f"Last Decision             :   {self.decision} \n"
            f"Last Action               :   {self.last_action}\n"
            f"Battery                   :   {self.battery}% \n"
            f"Total Moves               :   {self.counter}\n"
            )