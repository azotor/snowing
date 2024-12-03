import pygame, random, math
from Flake import Flake
from Player import Player
from Print import Print
from Cooldown import Cooldown

class Game:
    def __init__( self ):
        self.window = pygame.display.set_mode( ( 800, 600 ), pygame.SRCALPHA, 32 )
        pygame.display.set_caption( "Śnieżyca" )
        self.clock = pygame.time.Clock()

        self.run = True
        a = random.randint( 45, 135 ) * math.pi / 180
        self.windDir = pygame.Vector2( math.cos( a ), math.sin( a ) ).normalize()
        self.windSpeed = random.randint( 20, 100 )

        self.maxflakes = 200
        self.flakes = [ Flake( random.randint( -6, 800 ), random.randint( 0, 600 ) ) for i in range( self.maxflakes ) ]

        self.player = Player()
        self.playerOriginMark = True

        self.prints = []
        self.printsCoolDown = Cooldown( 200 )
        
        self.loop()
    
    def loop( self ):
        
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
            self.clock.tick( 60 )
            self.update()
            self.render()
                    
    def update( self ):
            
            if len( self.prints ):
                for print in self.prints:
                    print.update()
                    if print.ttl < 0:
                        self.prints.remove( print )
            
            self.player.update()
            
            if self.player.walk:
                if not self.printsCoolDown.isRunning():
                    self.prints.append( Print( self.player.pos ) )
                    self.printsCoolDown.run()
            
            self.printsCoolDown.update()
            
            if len( self.flakes ):
                for flake in self.flakes:
                    flake.update( self.windDir * self.windSpeed )
                    if flake.out( self.windDir[ 0 ] ):
                        self.flakes.remove( flake )
                        
            while len( self.flakes ) < self.maxflakes:
                if self.windDir[ 0 ] >= 0:
                    x = random.randint( -400, 800 )
                    y = 0
                    if x < -6:
                        x = -6
                        y = random.randint( 0, 550 )
                else:
                    x = random.randint( 0, 1200 )
                    y = 0
                    if x > 806:
                        x = 806
                        y = random.randint( 0, 550 )
                self.flakes.append( Flake( x, y ) )
    
    def render( self ):
        self.window.fill( '#dddddd' )
        
        if len( self.prints ):
                for print in self.prints:
                    print.render()
            
        self.player.render()
        
        if len( self.flakes ):
            for flake in self.flakes:
                flake.render()
        
        if self.playerOriginMark:
            pygame.draw.line( self.window, 'red', self.player.pos + ( -10, 0 ), self.player.pos + ( 10, 0 ) )
            pygame.draw.line( self.window, 'red', self.player.pos + ( 0, -10 ), self.player.pos + ( 0, 10 ) )
        
        pygame.display.update()