# A simulator to experiment with Chord's stablization/idealization protocol(s).
# Created by: Hari Balakrishnan, hari@mit.edu, June 2013.

import sys
import random

class Node:
    def __init__(self, id, network):
        self.id = id
        self.network = network        
        self.pred = None        # predecessor Node (not ID but Node)
        self.succ = self        # successor Node (not ID but Node)
        self.succlist = []
        
    def repr(self):
        p = self.pred.id if self.pred is not None else self.pred
        return "node %d [==> %s <-- %s]" % (self.id, self.succ.id, p)


    # Sort a list of Nodes in increasing NodeID order starting from self.id
    def sort(self, nodelist):
        return sorted(nodelist, key=lambda node: node.id - self.id if node.id > self.id else node.id - self.id + 2**32)


    # Node joining Chord bootstrapping with an existing node with id n1_id.
    # Assume that n1 is a valid node or is None; if None, the joining Node is
    # the first node in the system.
    def join(self, n1_id):
        print 't=%d JOIN %s' % (self.network.curtime, self.repr())
        self.pred = None
        n1 = self.network.id2node(n1_id)
        self.succ = n1.find_successor(self.id)
        if self.network.config.async == 0: # synchronous succ reconciliation
#            self.reconcile()
            self.succlist = self.succ.get_succ_list()
            self.clean_succ_list()
        print '  JOINED %s' % self.repr()

        
    # Is x inside circular range (a,b] or (a,b)? 
    # The last argument is incl=True or False, where
    # True means (a,b]; False means (a,b)
    # Note: inside(x, a, a) is True as long as x != a.
    # XXX These steps are subtle; maybe there's an easier and less bug-prone way
    # to express what we want?
    def inside(self, x, a, b, incl=True):
        if a == b: 
            return incl or x != a
        if a < b:
            if a < x:
                if incl:
                    return x <= b
                else:
                    return x < b
            else:
                return False
        else:
            if x <= a:
                if incl:
                    return b >= x
                else:
                    return b > x
            else:
                return True
                

    # Find the successor node of a specified id.
    def find_successor(self, id):
        if self.network.config.verbose:
            print '  Node %d find_succ for %d' % (self.id, id)
        if self.inside(id, self.id, self.succ.id):
            return self.succ
        else:
            n1 = self.closest_preceding_node(self.id)
            return n1.find_successor(id)


    # Search for the highest predecessor node of a specified id.
    # Without fingers, this search is linear in the number of nodes.
    def closest_preceding_node(self, id):
        if self.network.config.verbose:
            print 'node %d closest_prec for %d' % (self.id, id)
        if self.inside(self.succ.id, self.id, id, False):
            if self.network.config.verbose: 
                print '\tclosest_prec for %d: %d' % (id, self.id)
            return self.succ
        return self             # PODC version does not have this line!


    # Return successor Node list to caller; prepend our successor to the returned list.
    def get_succ_list(self):
        if self.succ == self:
            return []
        elif self.succlist is []:
            return [self.succ]
        else:
            return [self.succ] + self.succlist

    def clean_succ_list(self):
        self.succlist = self.sort(self.succlist[:self.network.config.maxsucc])
        # Make sure that neither self nor self.succ is in self.succlist
        for n in self.succlist:
            if n == self or n == self.succ:
                self.succlist.remove(n)


    # stabilize() is called periodically. 
    # Verifies immediate successor and tells successor about the node.
    # Note: stabilize() is the same as idealize() from the PODC 2002 paper.
    def stabilize(self):
        if self.network.config.verbose:
            print 't=%d STABILIZE %s' % (self.network.curtime, self.repr())

        x = self.succ.pred
        if x is not None and self.inside(x.id, self.id, self.succ.id, False):
            if self.network.config.verbose:
                print '\tsucc.pred is', x.id
            self.succ = x
        self.succ.notify(self)
        if self.network.config.async == 0:
            self.reconcile()
        self.check_predecessor()

        # Schedule re-stabilization (and check_predecessor) in the future.
        self.network.add_event((int(self.network.curtime+self.network.config.stabperiod), self.id, 's'))


    # n1 tells us of its existence; we check if n1 is our new predecessor.
    def notify(self, n1):
        if self.id not in self.network.livenodes:
            if self.network.config.verbose:
                print "t=%d %s is dead" % ( self.network.curtime, self.repr() )
            return
        if self.pred is None or self.inside(n1.id, self.pred.id, self.id, False):
            if n1 != self:
                self.pred = n1
        if self.network.config.verbose:
            print 't=%d %s NOTIFIED by %d' % (self.network.curtime, self.repr(), n1.id)
#        if self.succ is self:
#            self.succ = n1


    # Called periodically from inside stabilize(). 
    # Checks whether predecessor has failed.
    # Note: was called "fix_predecessor" in PODC 2002.
    def check_predecessor(self):
        if (self.pred is not None and self.pred.id not in self.network.livenodes):
            self.pred = None

    # From PODC: periodically update failed successor pointer, if necessary.
    # Make self.succ be the smallest live node in the successor list.
    def fix_successor(self):
        if self.succ.id not in self.network.livenodes:
            if self.network.config.verbose:
                print 't=%d %s fix_successor (succ %d failed)' % (self.network.curtime, self.repr(), self.succ.id)
                print '\tsucclist: [', 
                for n in self.succlist: print n.id,
                print ']'
            # successor has failed
            self.succ = self
            for s in self.succlist:
                if s.id in self.network.livenodes:
                    self.succlist.remove(s)
                    self.succ = s
                    break
                else:
                    self.succlist.remove(s)

            if self.network.config.verbose:
                print 'fixed succ:', self.repr()
                print '\tsucclist: [', 
                for n in self.succlist: print n.id,
                print ']'


    def reconcile(self):
        self.fix_successor()
        self.succlist = self.succ.get_succ_list()
        self.clean_succ_list()
        if self.network.config.async != 0:
            self.network.add_event((int(self.network.curtime+self.network.config.async), self.id, 'r'))


class Network:
    def __init__(self, conf, events):
        self.config = conf
        self.events = events
        self.curtime = 0
        self.livenodes = []
        self.nodeset = {}       # dict mapping nodeid --> node

    # In each "step" we execute the events that are supposed to have
    # occurred thus far since the last step. Make sure to update curtime.
    def step(self):
        self.curtime = self.events[0][0]
        rmlist = []
        i = 0
        while i < len(self.events):
            e = self.events[i]
            e_time = int(e[0])
            if e_time > self.curtime:
                for nodeid in rmlist:
                    self.remove_events(nodeid)
                return
            # event's time has come
            e_nodeid = int(e[1])
            e_type = e[2]
            if e_type == 'j':   # join
                if e_nodeid not in self.livenodes:
                    n = Node(e_nodeid, self) # make a new node
                    if len(e) >= 4:
                        e_joinat = int(e[3])
                        n.join(e_joinat)
                    else:
                        print 't=%d JOIN node %s' % (self.curtime, n.repr())
                    self.add_node(n)
                    # add a stabilization event for a future time
                    self.add_event((int(e_time+self.config.stabperiod), e_nodeid, 's'))
            elif e_type == 'f': # fail
                if e_nodeid in self.livenodes:
                    print 't=%d FAIL %s' % (self.curtime, self.id2node(e_nodeid).repr())
                    self.livenodes.remove(e_nodeid)
                    rmlist.append(e_nodeid)
            elif e_type == 's':  # stabilize
                self.id2node(e_nodeid).stabilize()
            elif e_type == "r": # "reconcile" -- assuming ASYNC stablization
                self.id2node(e_nodeid).reconcile()

            del self.events[i]

    # Add a Node to the Chord network. Really just for bookkeeping and 
    # keeping track of live nodes.
    def add_node(self, node):
        if node not in self.nodeset:
            self.nodeset[node.id] = node
            self.livenodes.append(node.id)

    def id2node(self, nodeid):
        return self.nodeset[nodeid]

    # Add an event to run in the future
    def add_event(self, event):
        # event is a tuple: time, nodeid, event_type
#        print 'events:', self.events
        for i in xrange(len(self.events)):
            if int(self.events[i][0]) > int(event[0]):
#                print 'inserting %s at %d' % (event, i)
                self.events.insert(i, event)
#                print 'events now is:', self.events
                return
#        print 'events now is:', self.events
        self.events.append(event)


    # Remove all events to be run by nodeid. Called when nodeid fails.
    def remove_events(self, nodeid):
        for e in self.events:
            if e[1] == nodeid:
                self.events.remove(e)

    # Start at some node and check if the Chord ring is proper.
    def check_ring(self):
        if len(self.livenodes) == 0:
            print 'No live nodes'
            sys.exit(0)

        ring = []
        startnode = self.id2node(self.livenodes[0])
        nextnode = startnode
        ring.append(startnode)
        while True:
            nextnode = nextnode.succ
            if nextnode == startnode or nextnode == nextnode.succ:
                return ring
            else:
                ring.append(nextnode)
                

    # Run the simulation. At the end, print out the status of the Chord ring.
    def run(self): 
        # As long as there are events to run and simtime hasn't elapsed, step through.
        while self.curtime <= self.config.simtime and self.events != []:
            self.step()

        # Done. Print out the status of the ring.
        print 'AFTER RUNNING FOR %d TIMESTEPS:' % self.config.simtime
        if self.config.verbose:
            print '***'
        for nodeid in self.livenodes:
            print self.id2node(nodeid).repr(), 'succlist is:',
            print '[',
            for n in self.id2node(nodeid).succlist:
                print "%d" % n.id,
            print ']'
        ring = self.check_ring()
        print 'Traversal of successors from %s' % ring[0].repr()
        print ' ',
        for node in ring:
            print "%d " % node.id,
        if len(ring) == len(self.livenodes):
            print '\nOne ring to rule them all!'
        else:
            print 'Something is rotten in the state of the ring!'
