from environment import Environment
from chargingstation_logic import ChargingStationLogicSystem

class Station():

    def __init__(self, position: tuple, ori: str, env: object, robot: object):
        self.logic = ChargingStationLogicSystem()
        self.setup_logic_rules() 
        self.enviroment = env
        self.paired_robot = robot
        self.position = position
        self.orientation = ori
        self.senser_values = self.sense()
        self.decision = None
        self.last_action = None

    def setup_logic_rules(self):
        """
        Expert System logic / rules        
        """

        # Check for robot
        self.logic.add_rule(["north_robot"], "charge_north")
        self.logic.add_rule(["east_robot"], "charge_east")
        self.logic.add_rule(["south_robot"], "charge_south")
        self.logic.add_rule(["west_robot"], "charge_west")

        # Otherwise... idle
        self.logic.add_rule(["chargingstation_idle"], "idle")

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
        Cycle through senser_values for existing robot in front
                
        :return: str: the decision, to charge or not to charge (north, east, south, west)
        """

        # Pass facts from sensors
        self.logic.reset_facts()
        self.logic.update_facts_from_sensors(self.senser_values)

        # Decide on action     
        return self.logic.decide_action()
    
    def act(self):
        """
        Run sensers and call decide function. Compare all results and commit to an action
        
        """

        self.sense()
        self.decision = self.decide()

        if "idle" in self.decision:
            self.last_action = "idle"

        elif "charge_" in self.decision:

            # topup robot charge
            if self.paired_robot.battery >= 95:
                self.paired_robot.battery = 100
            else:
                self.paired_robot.battery += 5

            self.last_action = f"Charged Robot : {self.decision}"

    def __str__(self):
        """
        Output messages
        """
        
        curr_sensers = self.enviroment.get_cells(self.position)

        return (
            f"\n        -- ChargeStation Data -- \n"
            f"Position                  :   {self.position} \n"
            f"Last Sensor Values        :   {self.senser_values} \n"
            f"Last Decision             :   {self.decision} \n"
            f"Last Action               :   {self.last_action}\n"
            )