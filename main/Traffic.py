#This file is supposed to be responsible
#for sending simulated traffic to each of our
#five radar nodes in Radar Stations.py

import zmq
import time
import random

context = zmq.Context()
#connecting to each of the radar stations
traffic_to_radar_1_pub = context.socket(zmq.PUB)
traffic_to_radar_2_pub = context.socket(zmq.PUB)
traffic_to_radar_3_pub = context.socket(zmq.PUB)
traffic_to_radar_4_pub = context.socket(zmq.PUB)
traffic_to_radar_5_pub = context.socket(zmq.PUB)

traffic_to_radar_1_pub.bind(f"tcp://localhost:5567")
traffic_to_radar_2_pub.bind(f"tcp://localhost:5568")
traffic_to_radar_3_pub.bind(f"tcp://localhost:5569")
traffic_to_radar_4_pub.bind(f"tcp://localhost:5570")
traffic_to_radar_5_pub.bind(f"tcp://localhost:5571")

time.sleep(3) #attempting to circumvent the slow joiner problem

#radars get traffic that's banded by airline and by
#altitude
stations_config = {
    "Radar Station 1": {"iata_designator": "AA", "altitude_range": (1000, 9999)},
    "Radar Station 2": {"iata_designator": "BB", "altitude_range": (10000, 19999)},
    "Radar Station 3": {"iata_designator": "CC", "altitude_range": (20000, 29999)},
    "Radar Station 4": {"iata_designator": "DD", "altitude_range": (30000, 39999)},
    "Radar Station 5": {"iata_designator": "EE", "altitude_range": (40000, 49999)}
}

def generate_tail_number():
    return f"N{random.randint(100,999)}"

def generate_traffic():
    tail_number = generate_tail_number()
    iata_designator =  random.choice(["AA", "BB", "CC", "DD", "EE"])
    altitude_range = next(config["altitude_range"] for config in stations_config.values()
                          if config["iata_designator"] == iata_designator)
    altitude = random.randint(altitude_range[0], altitude_range[1])
    return tail_number, iata_designator, altitude

#creating and sending the traffic
while True:

    tail_number, iata_designator, altitude = generate_traffic()
    message = f"Tail: {tail_number}, IATA: {iata_designator}, Altitude: {altitude}"
    print(f"Generated traffic: {message}")

    for station, config in stations_config.items():
        if config["iata_designator"] == iata_designator and config["altitude_range"][0] <= altitude <= config["altitude_range"][1]:
            if station == "Radar Station 1":
                traffic_to_radar_1_pub.send_string(message)
            elif station == "Radar Station 2":
                traffic_to_radar_2_pub.send_string(message)
            elif station == "Radar Station 3":
                traffic_to_radar_3_pub.send_string(message)
            elif station == "Radar Station 4":
                traffic_to_radar_4_pub.send_string(message)
            elif station == "Radar Station 5":
                traffic_to_radar_5_pub.send_string(message)

    time.sleep(1)
