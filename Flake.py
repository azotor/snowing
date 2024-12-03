import pygame, random

class Flake:
    def __init__( self, x, y ):
        self.size = random.randint( 2, 6 )
        self.pos = pygame.Vector2( x, y )
    
    def update( self, wind ):
        dt = 60 / 1000
        self.pos += wind * ( self.size / 4 ) * dt
    
    def render( self ):
        surf = pygame.display.get_surface()
        pygame.draw.circle( surf, 'white', self.pos, self.size )
        
    def out( self, wind ):
        return ( wind >= 0 and self.pos[ 0 ] > 800 ) or ( wind < 0 and self.pos[ 0 ] < -self.size * 2 ) or self.pos[ 1 ] > 600