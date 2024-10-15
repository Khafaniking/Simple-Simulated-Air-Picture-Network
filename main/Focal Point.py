import zmq
import time

context = zmq.Context()

#CONECTIONS WITH THE COMMAND CENTER

iata_ports = {
    "AA": 5551,  # Radar Station 1
    "BB": 5552,  # Radar Station 2
    "CC": 5553,  # Radar Station 3
    "DD": 5554,  # Radar Station 4
    "EE": 5555   # Radar Station 5
}

socket_cc_to_fp_sub = {}
for iata_code, port in iata_ports.items():
    socket_cc_to_fp_sub[iata_code] = context.socket(zmq.SUB)
    socket_cc_to_fp_sub[iata_code].connect(f"tcp://localhost:{port}")
    socket_cc_to_fp_sub[iata_code].setsockopt_string(zmq.SUBSCRIBE, "")

#socket for publishing to the command center
socket_fp_to_cc_pub = context.socket(zmq.PUB)
socket_fp_to_cc_pub.bind("tcp://localhost:5556")

#CONNECTIONS WITH THE RADAR STATIONS
#subscribing to the radar stations
sockets = []
for port in range(5557, 5562):  # Ports for Radar Stations 1-5
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{port}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages
    sockets.append(socket)

#publishing to the radar stations

socket_fp_to_radar_pub = {}
for iata_code, port in iata_ports.items():
    socket_fp_to_radar_pub[iata_code] = context.socket(zmq.PUB)
    socket_fp_to_radar_pub[iata_code].bind(f"tcp://localhost:{5562 + list(iata_ports).index(iata_code)}")

#connection from radar stations to focal point

poller = zmq.Poller()
for socket in sockets:
    poller.register(socket, zmq.POLLIN)
for sub_socket in socket_cc_to_fp_sub.values():
    poller.register(sub_socket, zmq.POLLIN)

processed_messages = set()
forwarded_messages = set()

while True:
    events = dict(poller.poll(10))
    # radar stations
    for i, socket in enumerate(sockets):
        if socket in events:
            message = socket.recv_string()
            print(f"Received from Radar Station {i+1}: {message}")
            
            # forward the messages to the command center
            if message not in processed_messages:
                socket_fp_to_cc_pub.send_string(message)
                processed_messages.add(message)
                print(f"Forwarded to Command Center: {message}")

    # process messages from the command center
    for iata_code, sub_socket in socket_cc_to_fp_sub.items():
        if sub_socket in events:
            message = sub_socket.recv_string()

            #ensure the message is only forwarded once
            #was having issue where because of how command center forwards messages to be distribtued to other
            #radar stations, it was being duplicated four times
            if message not in forwarded_messages:
                try:
                    parts = message.split(", ") #similar to what we have in cc.py
                    for part in parts:
                        if "IATA:" in part:
                            source_iata = part.split(": ")[1] #grab the iata code
                            break
                    print(f"Received from Command Center (Source IATA {source_iata}): {message}")

                    # forward to all radar stations except the one that generated it
                    for target_code, pub_socket in socket_fp_to_radar_pub.items():
                        if target_code != source_iata:
                            pub_socket.send_string(message)
                            print(f"Forwarded to Radar Station {target_code} (from {source_iata}): {message}")

                    forwarded_messages.add(message) #log the forwarded message so it cant be sent duplicate times

                except Exception as e:
                    print(f"Error processing message: {e}")

