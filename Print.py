import pygame, random

class Print:
    def __init__( self, pos ):
        self.pos = pygame.Vector2( pos )
        self.size = random.randint( 3, 5 )
        self.ttl = 15
    
    def update( self ):
        dt = 60 / 1000
        self.ttl -= dt
    
    def render( self ):
        surf = pygame.display.get_surface()
        print = pygame.Surface( ( self.size * 2, self.size * 2 ), pygame.SRCALPHA, 32 )
        pygame.draw.circle( print, ( 100, 100, 100, self.ttl / 15 * 100 ), ( self.size, self.size ), self.size )
        surf.blit( print, self.pos )