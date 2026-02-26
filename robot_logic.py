import random

class RobotLogicSystem:
    
    def __init__(self):
        self.rules = []
        self.facts = set()
        self.direction_priority = ["north", "east", "south", "west"]

    def add_rule(self, conditions, conclusion):
        self.rules.append({"conditions": conditions, "conclusion": conclusion})

    def add_fact(self, fact):
        self.facts.add(fact)

    def update_last_action(self, last_action):
        """
        last action performed
        """

        if last_action == "random_direction":
            fact = "on_to_glory"
        else:
            fact = "spin_to_win"

        self.add_fact(fact)

    def update_battery_life(self, battery):
        """
        battery: int 0-100
        """
        
        if battery <= 1:
            fact = "battery_dead"
        else:
            fact = "battery_ok"

        self.add_fact(fact)


    def update_facts_from_sensors(self, sensors: dict, orientation: str):
        """
        sensors: dict like {"pos": "d", "north": " ", "south": "d", ...}

        :param: sensors  dict like {"pos": "d", "north": " ", "south": "d", ...}
                orientation  str like "^", "v", "<", ">"
        """
        if sensors["pos"] not in ["u", " ", "d", "l", "r", "x", "^", "v", "<", ">"] and not sensors["pos"].isdigit():
            self.add_fact("current_cell_dirty")

        directions_clear = 0

        # random compass directions
        random.shuffle(self.direction_priority)

        # check front sensers as Prio
        if sensors[self.ori_lookup(orientation)] not in ["u", " ", "d", "l", "r", "x"] and not sensors[self.ori_lookup(orientation)].isdigit():
            self.add_fact(f"front_dirty")
            directions_clear += 1

        elif sensors[self.ori_lookup(orientation)] in [" "] or sensors[self.ori_lookup(orientation)].isdigit():
            self.add_fact(f"front_clear")
            directions_clear += 1

        # check remaining sensers
        # prio dirty, blocked, then visited
        for direction in self.direction_priority:

            if sensors[direction] not in ["u", " ", "d", "l", "r", "x"] and not sensors[direction].isdigit():
                self.add_fact(f"{direction}_dirty")
                directions_clear += 1
                break

            elif sensors[direction] in ["u", "d", "l", "r", "x"]:
                self.add_fact(f"{direction}_blocked")
            
            # elif sensors[direction].isdigit():
            #     self.add_fact(f"{direction}_visited")

        # pick random direction that is clear 
        for direction in self.direction_priority:
            
            if sensors[direction] in [" "] or sensors[direction].isdigit():
                self.add_fact(f"{direction}_clear")
                directions_clear += 1
                break

        if directions_clear == 0:
            self.add_fact("surrounded")                    

    def decide_action(self):
        # Evaluate rules
        for rule in self.rules:
            if all(condition in self.facts for condition in rule["conditions"]):
                return rule["conclusion"]
            
        # Default if no rules match
        return "robot_lost"
    
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
    
    def reset_facts(self):
        self.facts.clear()