import sys
from optparse import OptionParser
import random
import numpy

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-j", "--joinrate", type="float", dest="joinrate",
                      default=1, help="rate of node joins (Poisson")
    parser.add_option("-f", "--failrate", type="float", dest="failrate",
                      default=.1, help="rate of node fails (Poisson")
    parser.add_option("-t", "--time", type="int", dest="time", 
                      default=100, help="time over which to join")
    parser.add_option("-m", "--idspace", type="int", dest="m",
                      default=16, help="number of bits in ID space")

    (conf, args) = parser.parse_args()

    maxid = 2**conf.m
    livenodes = []
    deadnodes = []

    for t in xrange(conf.time):
        n = numpy.random.poisson(conf.joinrate)
        for i in xrange(n):
            id = random.randint(0, maxid)
            if id in livenodes or id in deadnodes:
                continue
            if len(livenodes) > 0:
                joinat = livenodes[random.randint(0, len(livenodes)-1)]
                print '%d %d j %d' % (t, id, joinat)
            else:
                print '%d %d j' % (t, id)
            livenodes.append(int(id))


        f = numpy.random.poisson(conf.failrate)
        for i in xrange(f):
            if len(livenodes) > 0:
                idx = random.randint(0, len(livenodes)-1)
                deadnodes.append(livenodes[idx])
                print '%d %d f' % (t, livenodes[idx])
                del livenodes[idx]
