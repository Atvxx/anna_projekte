from settings import * 
from player import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, map_width, map_height):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'Anna Runter', 0
        self.image = pygame.image.load(join('images', 'players','anna','Anna Runter','0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-80, -60)

        # Bewegung
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

        self.map_width = map_width
        self.map_height = map_height

    def load_images(self):
        self.frames = {'Anna Links': [], 'Anna Rechts': [], 'Anna Oben': [], 'Anna Runter': [] }

        for state in self.frames.keys():    
            for folder_path, sub_folders, file_names in walk(join('images', 'players', 'anna', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: Player.safe_convert_to_int(name.split('.')[0])):
                        #Ignoriere unerwünschte Dateien generiert mit chatgpt
                        #Qualität: sehr gut
                        if file_name.startswith('.') or not file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                            continue
                        full_path = join(folder_path, file_name)
                        try:
                            surf = pygame.image.load(full_path).convert_alpha()
                            self.frames[state].append(surf)
                        except pygame.error:
                            pass

                        
    @staticmethod #generiert mit chatgpt, qualität ist gut
    def safe_convert_to_int(value):
        try:
            return int(value)
        except ValueError:
            return float('inf')  # Gibt einen hohen Wert zurück, um solche Dateien ans Ende zu sortieren

    #Bewegung sowohl mit WASD- als auch Cursortasten!
    def input(self):
            keys = pygame.key.get_pressed()
            self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
            self.direction = self.direction.normalize() if self.direction else self.direction # Dafür da, damit man diagonal nicht schneller ist als sonst

    def move(self, dt):
        #4. Spieler bleibt so neben der Kamera auch innerhalb der Kartengrenzen
        # horizontale Bewegung
        # generiert mit ChatGPT
        #qualität: gut, hält Anna in den Grenzen der Map
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.hitbox_rect.x = max(0, min(self.hitbox_rect.x, self.map_width - self.rect.width))
        self.collision('horizontal')

        # vertikale Bewegung
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.hitbox_rect.y = max(0, min(self.hitbox_rect.y, self.map_height - self.rect.height))
        self.collision('vertical')

    # Synchronisiere sichtbare Position
        self.rect.center = self.hitbox_rect.center



        #generiert mit chatgpt
        #Qualität: funktioniert und ist klar
        #Was fehlt/mögl. Verbesserungen: dass man "näher" an die collision ran kommt
    def collision(self, direction):
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
                    
    #bewegung des spielers überprüfen, animation festzulegen            
    def animate(self, dt):
        if self.direction.x > 0:  
            self.state = 'Anna Rechts'
        elif self.direction.x < 0:  
            self.state = 'Anna Links'
        elif self.direction.y > 0:  
            self.state = 'Anna Runter'
        elif self.direction.y < 0:  
            self.state = 'Anna Oben'

        # Animation nur aktualisieren, wenn sich der Spieler bewegt
        if self.direction.x != 0 or self.direction.y != 0:
            self.frame_index += 5 * dt
        else:
            #wenn der spieler steht, dann bleibt das bild von geh richtung
            self.frame_index = 0

        #generiert mit chatgpt
        #qualität: gut, hat unsere Anforderungen erfüllt
        current_frames = self.frames[self.state]  
        frame_number = int(self.frame_index) % len(current_frames)  
        self.image = current_frames[frame_number]  


 
    def update(self, dt):
            self.input()
            self.move(dt)
            self.animate(dt)
