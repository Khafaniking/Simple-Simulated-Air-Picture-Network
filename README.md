# Simple-Simulated-Air-Picture-Network
Just a simple project for my Distributed Networking Class. Using ZeroMQ and sockets to simulate network traffic between radar installations. 

The concept is that we have a series of radar installations (just five in this case), that handle different airline traffic at different altitudes. The radar statiosn can only see their own band of airlines, and the radar stations (or they companies they belong to) do not talk to one another. 

Each of these radar installations then publish what traffic they see to the communications Focal Point.py. This focal point is basically just the main hub of the radar network. The focal point then publishes this information to the command center. 

Command Center.py is subscribed to the focal point, and collects all of the data from these different radar stations. It logs each message it gets from the focal point, and then broadcasts these to the radio stations (except its origin), again through the focal point. The Command center has the full picture of what's going on, and clues everybody else in. 

The proof should then be that we could look at any of our nodes/radar stations and be able to see logged traffic that should otherwise be outside of its range. For this we have monitor.py which watches the port that Radio Station 1/AA uses to hear traffic from traffic.py, and the other port it uses to receive messages from the command center -> focal point pipeline. 

Every file here, save traffic.py and monitory.py, which only publish and subscribe respectively, act as both a publisher and subscriber, so the definition between host and client is a bit murkier here, and has qualities of a peer-to-peer network. 
