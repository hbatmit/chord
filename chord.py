import sys
from optparse import OptionParser
from network import *

if __name__ == '__main__':
    if len(sys.argv) == 1:
        import config
        conf = config.Options()
    else:
        parser = OptionParser()
        parser.add_option("-f", "--file", type="string", dest="scenario", 
                          default="scene.dat", help="scenarios for node joins/fails")
        parser.add_option("-t", "--simtime", type="int", dest="simtime", 
                          default=1000, help="total simulation time steps")
        parser.add_option("-l", "--latency", type="int", dest="maxlat", 
                          default=1, help="max latency between nodes")
        parser.add_option("-p", "--prob", type="float", dest="prob", 
                          default=1.0, help="P(success) for a network message")
        parser.add_option("-s", "--stab", type="int", dest="stabperiod", 
                          default=5, help="stabilize every ... timesteps")
        parser.add_option("-r", "--maxsucc", type="int", dest="maxsucc", 
                          default=3, help="max size of successor list")
        parser.add_option("-v", "--verbose", action="store_true", dest="verbose", 
                          default=False, help="print diagnostics/debugging")

        (conf, args) = parser.parse_args()
    
    events = []
    f = open(conf.scenario)
    for line in f:
        data = line.split()
        if len(data) == 0 or data[0][0] is "#":
            continue
        if len(data) == 3:
            events.append( (int(data[0]), int(data[1]), data[2]) )
        elif len(data) == 4:
            events.append( (int(data[0]), int(data[1]), data[2] , int(data[3])) )

    if conf.verbose:
        print 'Initial events:', events
    net = Network(conf, events)
    net.run()
