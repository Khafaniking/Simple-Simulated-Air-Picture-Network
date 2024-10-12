#This file is supposed to be responsible
#for sending simulated traffic to each of our
#five radar nodes in Radar Stations.py

import zmq

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
