chord
=====

 A simulator to understand Chord's stabilization protocol under various conditions

Run it as: # python chord.py [options]

Usage: chord.py [options]

Options:
  -h, --help            show this help message and exit
  -f SCENARIO, --file=SCENARIO
                        scenarios for node joins/fails
  -t SIMTIME, --simtime=SIMTIME
                        total simulation time steps
  -l MAXLAT, --latency=MAXLAT
                        max latency between nodes
  -p PROB, --prob=PROB  P(success) for a network message
  -s STABPERIOD, --stab=STABPERIOD
                        stabilize every ... timesteps
  -r MAXSUCC, --maxsucc=MAXSUCC
                        max size of successor list
  -v, --verbose         print diagnostics/debugging

