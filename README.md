# Simple-Simulated-Air-Picture-Network
Just a simple project for my Distributed Networking Class. Using ZeroMQ and sockets to simulate network traffic between radar installations. 

The concept is that we have a series of radar installations (just five in this case), that are situated at five different points in a territory, and each have a certain radius to which they can "see" and detect aircraft traffic. This unique air traffic originates from Traffic.py, which publishes simualeted/artifical traffic to the different nodes/points in RadarStations.py.

Each of these radar installations then publish what traffic they see to the communications Focal Point.py. This focal point is basically just the main hub of the radar network. The focal point then publish this information to the command center. 

Command Center.py is subscribed to the focal point, and collects all of the data from these different radar stations, and amalgamates it all together into one total air picture. This is essentially just all of what the different five radar stations can each independently see, but collated together. 

The command center, after creating the air picture, then deploys it back to the focal point, which then deploys it out to the radar stations. Mind you, the air picture isn't a graphical image, but is just a stream of data that would represent all of the air traffic that would be picked up and we would see if we did have a graphical representation of the air traffic over the territory. 

The proof should then be that we could look at any of our nodes/radar stations and be able to see logged traffic that should otherwise be outside of its range. 
