from environment import Environment
import utils
import time


for j in range(100):

    e = Environment("./floorplans/floorplan_002.txt")

    r = utils.Robot(e.robot_location, e.robot_ori, 100, e)
    cs = utils.Station(e.chargestation_location, e.station_ori, e, r)

    for i in range(1000):
        
       
        if r.battery >= 1:
            r.act()
        else:
            break

        cs.act()
        print()
        print()

        print(r)
        print(cs)
        print(e)

    print(f"run {j}")
        
        #input()
        #time.sleep(1.5)