class ChargingStationLogicSystem:
    
    def __init__(self):
        self.rules = []
        self.facts = set()

    def add_rule(self, conditions, conclusion):
        self.rules.append({"conditions": conditions, "conclusion": conclusion})

    def add_fact(self, fact):
        self.facts.add(fact)

    def update_facts_from_sensors(self, sensors: dict):
        """
        sensors: dictionary of values, north, east ... of the current station position

        :param: sensors  dict like {"pos": "d", "north": " ", "south": "d", ...}
        """

        for direction in ["north", "south", "east", "west"]:
            
            if sensors[direction] in ["^", "v", "<", ">"]:                
                self.add_fact(f"{direction}_robot")


    def decide_action(self):
        # Evaluate rules

        for rule in self.rules:
            if all(condition in self.facts for condition in rule["conditions"]):
                return rule["conclusion"]
            
        # Default if no rules match
        return "chargingstation_idle"
    
    def ori_lookup(self, input_dir) -> str:
        """
        Change dir into robot direction symbol

        :param: str dir, expected values north, east, south, west
        :return: str   values "^", "v", "<", ">"
        """

        directions = {
            "north": "u",
            "south": "d",
            "west": "l",
            "east": "r"
        }

        # reverse mapping
        directions.update({v: k for k, v in directions.items()})
        
        return directions[input_dir]
    
    def reset_facts(self):
        self.facts.clear()


if __name__ == "__main__":

    station = ChargingStationLogicSystem()
    station.reset_facts()

    # Clean current cell if dirty
    station.add_rule(["chargingstation_idle"], "idle")

    # Battery dead. End program
    station.add_rule(["north_robot"], "charge_north")
    station.add_rule(["east_robot"], "charge_east")
    station.add_rule(["south_robot"], "charge_south")
    station.add_rule(["west_robot"], "charge_west")


    station.update_facts_from_sensors({'north': ' ', 'east': '^', 'south': 'u', 'west': ' ', 'pos': '^'})


    print(station.decide_action())
