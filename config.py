class Options:
    def __init__(self):
        self.scenario = "scene.dat"
        self.simtime = 200
        self.maxlat = 1
        self.prob = 1.0
        self.stabperiod = 5
        self.maxsucc = 3
        # For the intended SYNC version, update, reconcile, and flush
        # happen synchronously with stabilize. Otherwise, set them
        # explicitly here.
        self.update = 0
        self.recon = 0
        self.flush = 0
        self.verbose = False
