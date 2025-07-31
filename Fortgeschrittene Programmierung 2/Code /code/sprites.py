from settings import *
from math import atan2, degrees


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.ground=True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_rect(topleft=pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # Waffe soll an den Player ran
        self.player = player
        self.distance = 90 
        self.player_direction = pygame.Vector2(0,1)
        
        #setup für den gun sprite
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('images', 'guns', 'waffe.png' )).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_rect(center = self.player.rect.center + self.player_direction * self.distance)
        
    # Mausbewegung für die Waffe
    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT /2 )
        self.player_direction = (mouse_pos - player_pos).normalize()
    
    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) -90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
            self.image = pygame.transform.flip(self.image, False, True)
        
    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000 # 1000 millisekunden = 1 Sekunde, also verschwinden die bullets nach 1sek.
        
        # Dafür da, damit die Bullets in einer Richtung geschossen werden
        self.direction = direction 
        self.speed = 1200
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
class TimerObject(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        
        #image
        self.frames, self.frame_index = frames, 0 
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6
        
        #rect
        self.rect = self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 150 #Geschwindigkeit enemies
        
        # timer section
        self.death_time = 0
        self.death_duration = 400
    
    def animate(self, dt): #Für die Bewegungen
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        
    def move(self, dt):
        #Positionen abrufen
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        #Richtung berechnen
        self.direction = (player_pos - enemy_pos).normalize()

        #Bewegung des Gegners Richtung des players, Position aktualisieren 
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collisions('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collisions('vertical')
        self.rect.center = self.hitbox_rect.center
        
        #kollisionen prüfen
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                self.hitbox_rect.center -= self.direction * self.speed * dt

        # Aktualisierung des sichtbaren Rechtecks
        self.rect.center = self.hitbox_rect.center

        #generiert mit chatgpt 
        #Qualität: funktioniert und ist klar
        #Was fehlt/mögl. Verbesserungen: dass man "näher" an die collision ran kommt          
    def collisions(self, direction):
        # Durchlaufe alle Sprites in der Kollisionsgruppe
        for sprite in self.collision_sprites:
            # Prüfe, ob die Hitbox des Gegners mit der des aktuellen Sprites kollidiert
            if sprite.rect.colliderect(self.hitbox_rect):

                # Wenn die Bewegung horizontal ist (links/rechts)
                if direction == 'horizontal':
                    # Wenn sich der Gegner nach rechts bewegt (x > 0)
                    if self.direction.x > 0:
                        # Setze die rechte Kante der Hitbox an die linke Kante des kollidierenden Sprites
                        self.hitbox_rect.right = sprite.rect.left
                    # Wenn sich der Gegner nach links bewegt (x < 0)
                    if self.direction.x < 0:
                        # Setze die linke Kante der Hitbox an die rechte Kante des kollidierenden Sprites
                        self.hitbox_rect.left = sprite.rect.right

                # Wenn die Bewegung vertikal ist (oben/unten)
                else:
                    # Wenn sich der Gegner nach oben bewegt (y < 0)
                    if self.direction.y < 0:
                        # Setze die obere Kante der Hitbox an die untere Kante des kollidierenden Sprites
                        self.hitbox_rect.top = sprite.rect.bottom
                    # Wenn sich der Gegner nach unten bewegt (y > 0)
                    if self.direction.y > 0:
                        # Setze die untere Kante der Hitbox an die obere Kante des kollidierenden Sprites
                        self.hitbox_rect.bottom = sprite.rect.top           
    
    def destroy(self):
        #timer starten
        self.death_time = pygame.time.get_ticks()
        #wenn enemies sterben, dann werden in weiß verwischt
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf
    
    
    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()
    
    def update(self, dt):
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()
