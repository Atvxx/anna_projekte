from settings import *
from player import Player
import pygame
from sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
    def __init__(self):
        pygame.init()
        
        # Stoppt die vorherige Musik, falls vorhanden
        if pygame.mixer.get_init():
            pygame.mixer.stop()
        
        # Display    
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('FREE MAI !!')
        self.clock = pygame.time.Clock()

        # Timer
        self.start_time = pygame.time.get_ticks()
        self.time_limit = 30  # Sekunden
        self.font = pygame.font.Font(None, 36)
        
        # Spielstatus
        self.running = True
        self.game_over = False
        self.won = False  # Zustand für gewonnen

        self.map_width = 0
        self.map_height = 0

        # Gruppen von Sprites
        self.all_sprites = None
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.timer_sprites = pygame.sprite.Group()

        # Timer für die Gun
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        # Timer für enemies
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []

        # Audio
        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot5.wav'))
        self.shoot_sound.set_volume(0.3)
        self.aufprall_sound = pygame.mixer.Sound(join('audio', '21_Debuff_01.wav'))
        self.aufprall_sound.set_volume(0.2)
        self.music = pygame.mixer.Sound(join('audio', 'Fair_Fight_(Battle).wav'))
        self.music.set_volume(0.3)
        self.music.play(loops=-1)
        
        # Punktzahl hinzufügen
        self.score = 0  # Punktzahl starten

        # Setup
        self.setup()
        self.load_images()

        # Bilder Enemies + Gun 
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'guns', 'patrone.png')).convert_alpha()
        
        all_folders = list(walk(join('images', 'enemies')))[0][1]
        
        #ein Wörterbuch, das die Gegner-Grafiken speichert
        self.enemy_frames = {}

        # Jeden Unterordner durchgehen
        for folder in all_folders:
            self.enemy_frames[folder] = []  # Liste für die Bilder in diesem Ordner

            
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)): 
                sorted_files = sorted(file_names, key=lambda name: int(name.split('.')[0])) #Dateien sortieren, damit die Reihenfolge stimmt (z. B. 1.png, 2.png, ...)

                #Jede Datei laden
                for file_name in sorted_files:
                    full_path = join(folder_path, file_name)  #Voller Dateipfad
                    surf = pygame.image.load(full_path).convert_alpha()  #Bild laden+konvertieren
                    self.enemy_frames[folder].append(surf)  #Bild zur Liste hinzufügen

    # Hier Mausklick fürs schießen
    def input(self):
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] and self.can_shoot:
            self.shoot_sound.play()

            gun_position = self.gun.rect.center  
            bullet_direction = self.gun.player_direction  
            bullet_offset = bullet_direction * 50  
            bullet_position = gun_position + bullet_offset  

            # Eine neue Kugel erstellen
            Bullet(self.bullet_surf, bullet_position, bullet_direction, 
                (self.all_sprites, self.bullet_sprites))

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    # "timer bzw. berechner" für die Patronen/Schüsseabstände
    def gun_timer(self):
        if self.can_shoot == False:  
            current_time = pygame.time.get_ticks()  
            time_passed = current_time - self.shoot_time  #wie viel Zeit seit dem letzten Schuss vergangen ist
            if time_passed >= self.gun_cooldown:  
                self.can_shoot = True  

    def setup(self):
        map = load_pygame(join("data", "map", "newmaptest2.tmx"))
        self.map_width = map.width * TILE_SIZE
        self.map_height = map.height * TILE_SIZE
        
        self.all_sprites = AllSprites(self.map_width, self.map_height)

        #ansatz mit ChatGPT generiert
        #qualität: der Code ist klar strukturiert und erstellt automatisch Sprites
        #Was fehlt/mögl. Verbesserungen: evtl. dass man erstmal prüft, ob die layer überhaupt v.H. sind
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name('Ground1').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name('Ground2').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            if not obj.image:
                print(f"Warning: Object at ({obj.x}, {obj.y}) has no image.")
            else:
                CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites) 
        for obj in map.get_layer_by_name('Timer'):
            TimerObject((obj.x, obj.y), pygame.image.load(join('images', 'clock.png')).convert_alpha(), 
                (self.all_sprites, self.timer_sprites))
        for obj in map.get_layer_by_name('Charas'):
            if obj.name == 'Player': 
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.map_width, self.map_height)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    
    def bullet_collision(self):
        for bullet in self.bullet_sprites: #Für jede Kugel prüfen, ob sie mit einem Gegner kollidiert
            collision_sprites = pygame.sprite.spritecollide( #hier wird geprüft, ob die Kugel mit einem oder mehreren Gegnern kollidiert
                bullet, self.enemy_sprites, True, pygame.sprite.collide_mask
            )
            
            # Wenn es Kollisionen gibt
            if collision_sprites:
                self.aufprall_sound.play() #Aufprall sounds
                for sprite in collision_sprites:
                    sprite.destroy()  
                    self.score += 1  #Einen Punkt für jeden getroffenen Gegner im score anzeiger hinzufügen
                bullet.kill()  # Kugel löschen, da sie verbraucht ist


    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.game_over = True     

    #generiert mit ChatGPT
    #Qualität: sauber, klar, funktionstüchtig
    #Was fehlt/mögl. Verbesserungen: zB eine bestimmte Position, bestimmte font und/oder Hervorhebungen, wenn die Zeit kritisch wird oder wenn man die Uhren aufgesammelt hat
    def display_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        remaining_time = max(self.time_limit - elapsed_time, 0)
        timer_text = f"Time: {remaining_time}s"
        timer_surface = self.font.render(timer_text, False, (255, 255, 255))
        timer_rect = timer_surface.get_rect(topleft=(10, 10))
        self.display_surface.blit(timer_surface, timer_rect)

    #generiert mit ChatGPT
    #Qualität: funktioniert und ist klar
    #Was fehlt/mögl. Verbesserungen: zB eine bestimmte Position, eine bestimmte font und/oder ein Highscoresystem
    def display_score(self):
        score_text = f"Score: {self.score}"
        score_surface = self.font.render(score_text, False, (255, 255, 255))
        score_rect = score_surface.get_rect(topleft=(10, 50))
        self.display_surface.blit(score_surface, score_rect)
    
    # extra Zeit für den timer mit den aufgesammelten Uhren
    def gather_timer_objects(self):
        collected_objects = pygame.sprite.spritecollide(self.player, self.timer_sprites, True)
        if collected_objects:
            self.time_limit += 10  # 10 sekunden zur zeit hinzufügen


    def show_game_over(self):
        self.display_surface.fill((255, 0, 0))
        
        #generiert mit ChatGPT
        #Qualität: Texte sind präzise auf dem Bildschirm platziert
        #Was fehlt/mögl. Verbesserungen: evtl. ein smootherer Verlauf von Spielfeld zu Anzeige
        # "You lose"-Text
        font = pygame.font.Font(None, 72)
        text = font.render("MAI IS MINE NOW MUHAHAHA!!!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))#mittig horizontal| miitig vertikal, aber 50 Pixel über der Mitte
        self.display_surface.blit(text, text_rect)

        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render("Your Score: LOSER!", True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.display_surface.blit(score_text, score_text_rect)

        small_font = pygame.font.Font(None, 36)
        restart_text = small_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.display_surface.blit(restart_text, restart_rect)

    def show_game_won(self):
        self.display_surface.fill((50, 205, 50)) 

        #generiert mit ChatGPT
        #Qualität: Texte sind präzise auf dem Bildschirm platziert
        #Was fehlt/mögl. Verbesserungen: evtl. ein smootherer Verlauf von Spielfeld zu Anzeige
        # "You Win"-Text
        font = pygame.font.Font(None, 72)
        win_text = font.render("YOU SAVED MAI!!", True, (255, 255, 255))
        win_text_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))#mittig horizontal| mittig vertikal, aber 100 Pixel über der Mitte
        self.display_surface.blit(win_text, win_text_rect)
        
        #generiert mit ChatGPT
        # Punktzahl anzeigen
        # Qualität ist sehr gut und hat unsere Anforderungen umgesetzt
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.display_surface.blit(score_text, score_text_rect)
        
        #generiert mit ChatGPT
        # Neustart-/Beenden-Anweisungen
        # Qualität ist sehr gut
        small_font = pygame.font.Font(None, 36)
        restart_text = small_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))#mittig horizontal| mittig vertikal, aber 100 Pixel unter der Mitte
        self.display_surface.blit(restart_text, restart_rect)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000 # Zeit pro Frame berechnen

            # Alle Ereignisse prüfen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == self.enemy_event and not self.game_over and not self.won:
                    # Gegner erstellen
                    Enemy(
                        choice(self.spawn_positions),
                        choice(list(self.enemy_frames.values())),
                        (self.all_sprites, self.enemy_sprites),
                        self.player,
                        self.collision_sprites,
                    )

            # Wenn das Spiel vorbei ist, Eingaben prüfen
            if self.game_over or self.won:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.__init__()  # Spiel neu starten
                if keys[pygame.K_q]:
                    self.running = False  # Spiel beenden
                self.show_game_won() if self.won==True else self.show_game_over()
                pygame.display.update()
                continue  # Rest der Schleife überspringen

            #zeitlimit prüfen
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            if elapsed_time == self.time_limit:
                self.won = self.score >= 127  #spieler gewinnt ab 127 punkte
                self.game_over = not self.won

            #aktualisierungen im spiel
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()

            # umgebung bewegt sich zum spieler
            self.all_sprites.draw(self.player.rect.center)
            
            self.display_timer()

            #alle zeitbasierten Objekte sammeln
            self.gather_timer_objects()

            #anzeige aktueller punktestand auf dem bildschirm 
            self.display_score()

            #Bildschirm aktualisieren
            pygame.display.update()

        # Spiel beenden
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
