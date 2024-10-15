import zmq

#monitors radar station 1, AA
context = zmq.Context()

#log listens to traffic from... traffic.py communicating to radar station 1
socket_radar_1 = context.socket(zmq.SUB)
socket_radar_1.connect("tcp://localhost:5567")
socket_radar_1.setsockopt_string(zmq.SUBSCRIBE, "")

socket_focal_point = context.socket(zmq.SUB)
socket_focal_point.connect("tcp://localhost:5562")
socket_focal_point.setsockopt_string(zmq.SUBSCRIBE, "")

print("Listening for messages on Radar Station 1...")

poller = zmq.Poller()
poller.register(socket_radar_1, zmq.POLLIN)
poller.register(socket_focal_point, zmq.POLLIN)

while True:
    events = dict(poller.poll())

    if socket_radar_1 in events:
        message = socket_radar_1.recv_string()
        print(f"Traffic logged: {message}")

    if socket_focal_point in events:
        message = socket_focal_point.recv_string()
        print(f"Additional flight data from Command Center: {message}")
