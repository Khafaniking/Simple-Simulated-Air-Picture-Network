import zmq

context = zmq.Context()

#CONNECTIONS TO THE FOCAL POINT

#sockets for publishing to the focal point

socket_radar_1_to_fp_pub = context.socket(zmq.PUB)
socket_radar_2_to_fp_pub = context.socket(zmq.PUB)
socket_radar_3_to_fp_pub = context.socket(zmq.PUB)
socket_radar_4_to_fp_pub = context.socket(zmq.PUB)
socket_radar_5_to_fp_pub = context.socket(zmq.PUB)

socket_radar_1_to_fp_pub.bind(f"tcp://localhost:5557")
socket_radar_2_to_fp_pub.bind(f"tcp://localhost:5558")
socket_radar_3_to_fp_pub.bind(f"tcp://localhost:5559")
socket_radar_4_to_fp_pub.bind(f"tcp://localhost:5560")
socket_radar_5_to_fp_pub.bind(f"tcp://localhost:5561")

#sockets for subscribing to the focal point
#socket_radar_1_to_fp_sub = context.socket(zmq.SUB)
#socket_radar_2_to_fp_sub = context.socket(zmq.SUB)
#socket_radar_3_to_fp_sub = context.socket(zmq.SUB)
#socket_radar_4_to_fp_sub = context.socket(zmq.SUB)
#socket_radar_5_to_fp_sub = context.socket(zmq.SUB)

sockets = []
for port in range(5562, 5567):  # Ports for Radar Stations A to E
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages
    sockets.append(socket)

#CONNECTIONS TO TRAFFIC.PY

traffic_sockets = []
for port in range(5567, 5572):  # Ports for Radar Stations A to E
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages
    traffic_sockets.append(socket)
