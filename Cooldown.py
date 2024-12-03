class Cooldown:
    def __init__( self, time ):
        self.time = time
        self.timer = 0
        self.running = False
    
    def setTime( self, time ):
        self.time = time
    
    def run( self ):
        self.running = True
        self.timer = 0
    
    def update( self ):
        if self.running:
            self.timer += 1000 / 60
            if self.timer >= self.time:
                self.running = False
    
    def isRunning( self ):
        return self.running