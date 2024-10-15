import zmq
import time

context = zmq.Context()

#CONNECTIONS WITH THE FOCAL POINT

iata_ports = {
    "AA": 5551,  # Radar Station 1
    "BB": 5552,  # Radar Station 2
    "CC": 5553,  # Radar Station 3
    "DD": 5554,  # Radar Station 4
    "EE": 5555   # Radar Station 5
}

#sockets for publishing to the focal point, iata/radar station specific
socket_cc_to_fp_pub = {}
for iata_code, port in iata_ports.items():
    socket_cc_to_fp_pub[iata_code] = context.socket(zmq.PUB)
    socket_cc_to_fp_pub[iata_code].bind(f"tcp://localhost:{port}")

#socket for subscribing to the focal point
socket_fp_to_cc_sub = context.socket(zmq.SUB)
socket_fp_to_cc_sub.connect("tcp://localhost:5556")
socket_fp_to_cc_sub.setsockopt_string(zmq.SUBSCRIBE, "")

#filters and forwards traffic based on our iata designation codes
#any traffic received by the cc is forward to all
#other stations except the one that generated it

traffic_designator = {
    "AA": [],
    "BB": [],
    "CC": [],
    "DD": [],
    "EE": []
}

#this function grabs traffic and forwards it to every station
# besides the one that it originated from
def filter_and_forward_traffic():
    for iata_code, messages in traffic_designator.items():
        while messages:
            message = messages.pop(0)

            for target_code in traffic_designator.keys():
                if target_code != iata_code:
                    socket_cc_to_fp_pub[target_code].send_string(f"{message}")
                    print(f"Sent to Focal Point for {target_code} (from {iata_code}): {message}")

while True:
    # receives the message from whatever stations
    message = socket_fp_to_cc_sub.recv_string()
    print(f"Command Center received: {message}")
    #looks at the message, splits it into parts
    parts = message.split(", ")
    iata_code = None
    for part in parts:
        if "IATA:" in part:
            iata_code = part.split(": ")[1]  #grab the IATA code (AA, BB, etc)
            break
    #checks to make sure our iata code is in
    #traffic designator, then marks that message
    #for the filter and forward function to look at
    if iata_code and iata_code in traffic_designator:
        traffic_designator[iata_code].append(message)
        print(f"Logged traffic from {iata_code}: {message}")

    filter_and_forward_traffic()
