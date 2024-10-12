import zmq

context = zmq.Context()

#CONNECTIONS WITH THE FOCAL POINT

#socket for publishing to the focal point
socket_cc_to_fp_pub = context.socket(zmq.PUB)
socket_cc_to_fp_pub.bind("tcp://localhost:5555")

#socket for subscribing to the focal point
socket_fp_to_cc_sub = context.socket(zmq.SUB)
socket_fp_to_cc_sub.connect("tcp://localhost:5556")
socket_fp_to_cc_sub.setsockopt_string(zmq.SUBSCRIBE, "")
