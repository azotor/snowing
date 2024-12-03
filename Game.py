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
        self.newA = random.randint( 45, 135 )
        self.newSpeed = random.randint( 20, 100 )
        self.a = self.newSpeed
        self.windDir = pygame.Vector2( math.cos( self.a * math.pi / 180 ), math.sin( self.a * math.pi / 180 ) ).normalize()
        self.windSpeed = self.newSpeed
        self.windCoolDown = Cooldown( random.randrange( 1000, 5000  ) )
        self.windCoolDown.run()

        self.maxflakes = 200
        self.flakes = [ Flake( random.randint( -6, 800 ), random.randint( 0, 600 ) ) for i in range( self.maxflakes ) ]

        self.player = Player()
        self.playerOriginMark = True

        self.prints = []
        self.printsCoolDown = Cooldown( 200 )
        
        self.font = pygame.font.SysFont( "Arial", 18, True )
        self.windText = self.font.render( "Wiatr", True, '#222222' )
        
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
        
        self.windCoolDown.update()
        
        if not self.windCoolDown.isRunning():
            self.newA = random.randint( 45, 135 )
            self.newSpeed = random.randint( 20, 100 )
            self.windCoolDown.setTime( random.randint( 1000, 5000 ) )
            self.windCoolDown.run()
        
        if self.a > self.newA:
            self.a -= 2
            if self.a <= self.newA:
                self.a = self.newA
            self.windDir = pygame.Vector2( math.cos( self.a * math.pi / 180 ), math.sin( self.a * math.pi / 180 ) ).normalize()
        elif self.a < self.newA:
            self.a += 2
            if self.a >= self.newA:
                self.a = self.newA
            self.windDir = pygame.Vector2( math.cos( self.a * math.pi / 180 ), math.sin( self.a * math.pi / 180 ) ).normalize()
        
        if self.windSpeed > self.newSpeed:
            self.windSpeed -= 1
            if self.windSpeed <= self.newSpeed:
                self.windSpeed = self.newSpeed
        elif self.windSpeed < self.newSpeed:
            self.windSpeed += 1
            if self.windSpeed >= self.newSpeed:
                self.windSpeed = self.newSpeed
        
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
            
        self.window.blit( self.windText, ( 700, 480 ) )
        
        arrow = pygame.Surface( ( self.windSpeed, 20 ) ,pygame.SRCALPHA, 32 )
        pygame.draw.line( arrow, 'red', ( 0, 10 ), ( self.windSpeed, 10 ), 2 )
        pygame.draw.line( arrow, 'red', ( self.windSpeed - 10, 0 ), ( self.windSpeed, 10 ), 2 )
        pygame.draw.line( arrow, 'red', ( self.windSpeed - 10, 20 ), ( self.windSpeed, 10 ), 2 )
        arrow = pygame.transform.rotate( arrow, -self.a )
        rect = arrow.get_rect()
        rect.center = ( 725, 548 )
        self.window.blit( arrow, rect )
        pygame.draw.circle( self.window, 'red', ( 725, 548 ), 50, 2 )
        
        pygame.display.update()