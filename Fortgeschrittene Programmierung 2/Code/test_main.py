from test_setting import * # unsere Base, also blackscreen!!!

class Game:
    def __init__(self):
        # erstes Spielsetup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('FREE MAI !!')
        self.clock = pygame.time.Clock()  # Kontrolle Geschwindigkeit, FPS
        self.running = True




    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000  # Delta Time (dt) und es geht in millisekunden

            for event in pygame.event.get():  # Überprüfung Eingabe und schließen vom Fenster
                if event.type == pygame.QUIT:
                    self.running = False

            # update

            # draw
            pygame.display.update()

        pygame.quit()  # unser Exit


if __name__ =='__main__':
    game = Game()
    game.run()