import zmq
import time

context = zmq.Context()

#CONECTIONS WITH THE COMMAND CENTER

#socket for subscribing to the command center
socket_cc_to_fp_sub = context.socket(zmq.SUB)
socket_cc_to_fp_sub.connect("tcp://localhost:5555")
socket_cc_to_fp_sub.setsockopt_string(zmq.SUBSCRIBE, "")

#socket for publishing to the command center
socket_fp_to_cc_pub = context.socket(zmq.PUB)
socket_fp_to_cc_pub.bind("tcp://localhost:5556")

#CONNECTIONS WITH THE RADAR STATIONS
#subscribing to the radar stations
sockets = []
for port in range(5557, 5562):  # Ports for Radar Stations A to E
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages
    sockets.append(socket)

#publishing to the radar stations

socket_fp_to_radar_1_pub = context.socket(zmq.PUB)
socket_fp_to_radar_2_pub = context.socket(zmq.PUB)
socket_fp_to_radar_3_pub = context.socket(zmq.PUB)
socket_fp_to_radar_4_pub = context.socket(zmq.PUB)
socket_fp_to_radar_5_pub = context.socket(zmq.PUB)

socket_fp_to_radar_1_pub.bind("tcp://localhost:5562")
socket_fp_to_radar_2_pub.bind("tcp://localhost:5563")
socket_fp_to_radar_3_pub.bind("tcp://localhost:5564")
socket_fp_to_radar_4_pub.bind("tcp://localhost:5565")
socket_fp_to_radar_5_pub.bind("tcp://localhost:5566")

#connection from radar stations to focal point

poller = zmq.Poller()
for socket in sockets:
    poller.register(socket, zmq.POLLIN)

while True:
    events = dict(poller.poll(10))
    for i, socket in enumerate(sockets):
        if socket in events:
            message = socket.recv_string()
            print(f"Received from Radar Station {i+1}: {message}")

            #forward the messages to the command center
            socket_fp_to_cc_pub.send_string(message)
            print(f"Forwarded to Command Center: {message}")
