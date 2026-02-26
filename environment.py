class Environment:

    def __init__(self, env_map: str):
        self.robot_ori = None 
        self.station_ori = None       
        self.world = self.generate_map(env_map)
        
        self.robot_location = self.get_pos(["^", "v", "<", ">"])
        self.chargestation_location = self.get_pos(["u", "d", "l", "r"])

        if self.robot_location:
            x, y = self.robot_location
            self.occupied_pos = self.world[y][x]
        else:
            self.occupied_pos = None



    def generate_map(self, env_map):
        """
        Reads input str .txt file and converts it into a 2D grid.

        :param env_map: Path to environment map file
        :return: 2D list representing the map
        """
        try:

            grid = []
            with open(env_map, "r") as file:

                for line in file:
                    grid.append(list(line.strip()))

            return grid
        
        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            return None
        
    def get_pos(self, objects: list) -> tuple | None:
        """
        Searches the internal 2D map and returns the robot's position.

        :return: tuple (x, y of the robot) or None the robot has not been found. 
                Robot pos returned as x, y tuple into self.robot_location
                x, y index start 0 (top, left of grid)                
        """

        try:

            # loop through file
            for y, row in enumerate(self.world):
                for x, char in enumerate(row):
                    if char in objects:
                        
                        # set robort start ori
                        if char in ["^", "v", "<", ">"]:
                            self.robot_ori = char
                        
                        # set chargestation start ori
                        if char in ["u", "d", "l", "r"]:
                            self.station_ori = char

                        return x, y
            
            return None

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            self.robot_location = None
            return None
        

    def get_cells(self, pos: tuple) -> dict | None:
        """
        Using internal 2D map, return values north, east, south, west of curr pos (x, y)

        :param pos: tuple of x, y of the object
        :return: dict (str of values, north, east, south, west, current cells of input pos) or None (err)           
        """
        try:
            x, y = pos

            sensors_dic = {
                "north"   : self.world[y-1][x],
                "east"    : self.world[y][x+1],
                "south"   : self.world[y+1][x],
                "west"    : self.world[y][x-1],
                "pos"     : self.occupied_pos
            }

           
            return sensors_dic
        
        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            return None
        

    def clear_cell(self, position: tuple):
        """
        Using internal 2D map, update current position value (not robot) to "0" (or increment +1)
        """
        self.occupied_pos = "0"


    def move_robot(self, move_to: tuple, ori: str) -> tuple:
        """
        Using internal 2D map, attempt to move to new location (x, y). 
                return the updated pos, if hit wall, no change in x, y

        :param ori: str of the robots orientation, expected: "^", "v", "<", ">"
        :return: tuple (x, y pos)               
        """

        # gen params
        x, y = self.robot_location
        new_x, new_y = move_to

        # collision detection
        if self.world[move_to[1]][move_to[0]] in ["u", "d", "l", "r", "x"]:
            return self.robot_location
        
        else:            
            # update env data
            self.occupied_pos = self.world[new_y][new_x] #store curr pos value
            self.world[y][x] = "0" #print tail values
            self.world[new_y][new_x] = ori #move to new place
            self.robot_location = (new_x, new_y) #update env store

            return self.robot_location

    def __str__(self):
        """
        Loop through grid, and join each row to generate out map
        
        """
        return "\n".join(map("".join, self.world))
