from lib.snap7_sprinkler_head import Snap7SprinklerHead

connector = Snap7SprinklerHead()
connector.connect("192.168.2.104", 0, 1)


index = 1
dis_1 = connector.get_valve_state(index)
print(dis_1)

connector.set_valve_state(index, False)
dis_1 = connector.get_valve_state(index)
print(dis_1)

connector.disconnect()
