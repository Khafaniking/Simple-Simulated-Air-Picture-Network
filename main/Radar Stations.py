import zmq
import time

context = zmq.Context()

#list of radar stations
radar_stations = ["Radar Station 1",
                  "Radar Station 2",
                  "Radar Station 3",
                  "Radar Station 4",
                  "Radar Station 5"]

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


#organize the pub sockets for sending messages to the
#focal point in an organized fashion
pub_sockets = [
    socket_radar_1_to_fp_pub,
    socket_radar_2_to_fp_pub,
    socket_radar_3_to_fp_pub,
    socket_radar_4_to_fp_pub,
    socket_radar_5_to_fp_pub
]

#connections from focal point.py to radar stations
sockets = []
socket_stations = {}

for i, port in enumerate(range(5562, 5567)):  # Ports for Radar Stations 1 to 5
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages
    sockets.append(socket)
    socket_stations[socket] = radar_stations[i]

#CONNECTIONS from TRAFFIC.PY to radar stations

traffic_sockets = []
traffic_socket_stations = {}
for i, port in enumerate(range(5567, 5572)):  # Ports for Radar Stations 1 to 5
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages
    traffic_sockets.append(socket)
    traffic_socket_stations[socket] = radar_stations[i]

#connection from traffic to radar stations

poller = zmq.Poller()
for socket in traffic_sockets:
    poller.register(socket, zmq.POLLIN)

while True:
    events = dict(poller.poll(10))
    for i, socket in enumerate(traffic_sockets):
        if socket in events:
            message = socket.recv_string()
            radar_station = traffic_socket_stations[socket]
            print(f"Received on {radar_station}: {message}")

            #forward our messages from the radar stations
            #to the focal point
            pub_sockets[i].send_string(message)
            print(f"{radar_station} forwarded: {message}")

