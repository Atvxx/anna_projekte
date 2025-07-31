from sprites import *


class AllSprites(pygame.sprite.Group):
    def __init__(self, map_width, map_height):
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.offset=pygame.Vector2()
        self.map_width = map_width
        self.map_height = map_height

    def draw(self, player_pos):
        #Kameraverschiebung
        self.offset.x=-(player_pos[0]-WINDOW_WIDTH/2)
        self.offset.y=-(player_pos[1]-WINDOW_HEIGHT/2)
        
        # 1.Kamera bleibt innerhalb der Grenzen unserer Map
        # Generiert durch ChatGPT
        #Qualität: funktioniert und ist klar
        #Was fehlt/mögl. Verbesserungen: evtl. eine Bedingung stellen, dass nur Sprites innerhalb des sichtbaren Bereiches gezeichnet werden, aber da unsere Map klein ist- es nicht so wichtig
        self.offset.x = max(min(self.offset.x, 0), -(self.map_width - WINDOW_WIDTH))
        self.offset.y = max(min(self.offset.y, 0), -(self.map_height - WINDOW_HEIGHT))

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')] 
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer,key=lambda sprite:sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)


