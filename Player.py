import pygame

class Player:
    def __init__( self ):
        self.pos = pygame.Vector2( 400, 300 )
        self.dir = pygame.Vector2()
        self.speed = 100
        self.scale = 2
        self.sprite = [ pygame.image.load( 'walk1.png' ).convert_alpha(), pygame.image.load( 'walk2.png' ).convert_alpha() ]
        self.sprite = [
            pygame.transform.scale( self.sprite[ 0 ], ( self.sprite[ 0 ].get_width() / self.scale, self.sprite[ 0 ].get_height() / self.scale ) ),
            pygame.transform.scale( self.sprite[ 1 ], ( self.sprite[ 1 ].get_width() / self.scale, self.sprite[ 1 ].get_height() / self.scale ) )
        ]
        self.timer = 0
        self.stepTime = 150
        self.currentSprite = 0
        self.walk = False
        self.facing = True
    
    def update( self ):
        keys = pygame.key.get_pressed()
        
        if keys[ pygame.K_LEFT] :
            self.dir[ 0 ] = -1
            self.facing = True
        elif keys[ pygame.K_RIGHT ] :
            self.dir[ 0 ] = 1
            self.facing = False
        else:
            self.dir[ 0 ] = 0
        
        if keys[ pygame.K_UP ] :
            self.dir[ 1 ] = -1
        elif keys[ pygame.K_DOWN ] :
            self.dir[ 1 ] = 1
        else:
            self.dir[ 1 ] = 0
            
        if self.dir[ 0 ] != 0 or self.dir[ 1 ] != 0:
            self.dir = self.dir.normalize()
        
        if self.dir[ 0 ] == 0 and self.dir[ 1 ] == 0:
            self.walk = False
            self.timer = 0
            self.currentSprite = 0
        else:
            self.walk = True
        
        if self.walk == True:
            self.timer += 1000 / 60
            if self.timer >= self.stepTime:
                self.timer -= self.stepTime
                self.currentSprite = 1 if self.currentSprite == 0 else 0
        
        dt = 60 / 1000
        
        self.pos += self.dir * self.speed * dt
            
    def render( self ):
        surf = pygame.display.get_surface()
        surf.blit( pygame.transform.flip( self.sprite[ self.currentSprite ], self.facing, False ), self.getOrigin() )
        
    def getOrigin( self ):
        sprite = self.sprite[ self.currentSprite ]
        return self.pos + ( -sprite.get_width() / 2, -sprite.get_height() )