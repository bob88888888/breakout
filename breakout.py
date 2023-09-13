import pygame
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import sys
import time

pygame.init()

class Block:
    def __init__(self, Game, Ball):
        self.game = Game
        self.ball = Ball

        self.yellow = (255, 255, 0)
        self.orange = (255, 200, 0)
        self.blue =  (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        self.colors = [self.yellow, self.orange, self.blue, self.red, self.white, self.green]

        self.num_rows = 10

        self.block_x = 0
        self.block_y = 0
        self.block_w = 100
        self.block_h = 20
        self.blocks = []
        self.block_spacing = 4

        self.num_columns = self.game.win_width // self.block_w

        self.blocks = []

        for row in range(self.num_rows):
            row_blocks = []
            for col in range(self.num_columns):
                x = col * (self.block_w + self.block_spacing)
                y = row * (self.block_h + self.block_spacing)
                row_blocks.append((x, y))  # Store the position of each block
            self.blocks.append(row_blocks)

    def draw(self):
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                if self.blocks[row][col] is not None:
                    choice = (row + col) % len(self.colors)
                    x, y = self.blocks[row][col]  # Get the stored position of the block
                    pygame.draw.rect(self.game.window, self.colors[choice], (x, y, self.block_w, self.block_h))
    
    def collision(self):
        ball_rect = pygame.Rect(
            self.game.ball.ball_x, self.game.ball.ball_y, self.game.ball.ball_w, self.game.ball.ball_h
        )

        for row in range(self.num_rows):
               for col in range(self.num_columns):
                if self.blocks[row][col] is not None:
                    x, y = self.blocks[row][col]
                    block_rect = pygame.Rect(x, y, self.block_w, self.block_h)

                    if ball_rect.colliderect(block_rect):
                         if (self.game.ball.ball_x <= x + self.block_w) and (self.game.ball.ball_y >= y and self.game.ball.ball_y <= y + self.block_h):
                            self.blocks[row][col] = None
                            self.ball.speed_y = -self.ball.speed_y
                            self.ball.ball_y += self.ball.speed_y
                            self.game.score += 1
    
class Ball:
    def __init__(self, Game, Slider):
        self.game = Game
        self.slider = Slider

        self.ball_x = self.game.win_width // 2
        self.ball_y = self.game.win_height // 2
        self.ball_w = 15
        self.ball_h = 15
        self.speed_x = 5
        self.speed_y = 5

    def draw(self):
            pygame.draw.rect(self.game.window, (255, 255, 0), (self.ball_x, self.ball_y, self.ball_w, self.ball_h))
    
    def move(self):
        if self.ball_x <= 0 or self.ball_x + self.ball_w >= self.game.win_width:
            self.speed_x = -self.speed_x
        
        self.ball_x += self.speed_x

        if self.ball_y <= 0 or self.ball_y + self.ball_h >= self.game.win_height:
            self.speed_y = -self.speed_y

        elif (
            self.ball_y + self.ball_h >= self.slider.slider_y
            and self.ball_x >= self.slider.slider_x
            and self.ball_x + self.ball_w <= self.slider.slider_x + self.slider.slider_w
        ):
            self.speed_y = -self.speed_y

        self.ball_y += self.speed_y 

class Slider:
    def __init__(self, Game, slider_x, slider_y):
        self.game = Game
        self.ball = Ball(self.game, self)

        self.slider_x = self.game.win_height - 10
        self.slider_y = self.game.win_width // 2
        self.slider_w = 200
        self.slider_h = 10
        self.move_speed = 10

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.slider_x > 0:
            self.slider_x -= self.move_speed
        if keys[pygame.K_RIGHT] and self.slider_x + self.slider_w < self.game.win_width:
            self.slider_x += self.move_speed

    def draw(self):
        pygame.draw.rect(self.game.window, (255, 255, 255), (self.slider_x, self.slider_y, self.slider_w, self.slider_h))

class Game:
    def __init__(self):
        self.win_width = 1900
        self.win_height = 1000
        self.window = pygame.display.set_mode((self.win_width, self.win_height))
        self.clock = pygame.time.Clock()

        self.slider = Slider(self, self.win_width // 2, self.win_height - 20)
        self.ball = Ball(self, self.slider)
        self.block = Block(self, self.ball)
        self.score = 0
        self.life = 3
    
    def display_score(self):
        font = pygame.font.SysFont('Arial', 36)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.window.blit(text, (self.win_width // 4, self.win_height // 2))

    def display_life(self):
        font = pygame.font.SysFont('Arial', 36)
        text = font.render(f"Life: {self.life}", True, (255, 255, 255))
        self.window.blit(text, (self.win_width // 4 * 3, self.win_height // 2))
        if self.ball.ball_y + self.ball.ball_h >= self.win_height:
            self.life -= 1

    def game_over(self):
        self.ball.speed_x = 0
        self.ball.speed_y = 0
        self.ball.ball_y = self.win_height - (1 + self.ball.ball_h)

        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, (0, 0, 0), (0, 0, self.win_width, self.win_height))
        font = pygame.font.SysFont('Arial', 36)
        text = font.render(f"Game Over! You scored {self.score}. Press Enter to continue or press Escape to quit", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.win_width // 2, self.win_height // 2))
        self.window.blit(text, text_rect)      

    def quit(self):
        pygame.quit()
        sys.exit()

    def game_reset(self):
        if self.ball.ball_y + self.ball.ball_h >= self.win_height:
            time.sleep(2)
            self.ball.ball_x = self.win_width // 2
            self.ball.ball_y = self.win_height // 2

    def reset_game(self):
        self.score = 0
        self.life = 3
        self.slider.slider_x = self.win_width // 2

        # Reinitialize the blocks using the same logic as in the Block class constructor
        self.blocks = []
        for row in range(self.block.num_rows):
            row_blocks = []
            for col in range(self.block.num_columns):
                if self.block.blocks[row][col] == None:
                    x = col * (self.block.block_w + self.block.block_spacing)
                    y = row * (self.block.block_h + self.block.block_spacing)
                    self.block.blocks[row][col] = x, y

        # Reinitialize the ball
        self.ball.__init__(self, self.slider)

    def play(self):
        play = True

        while play:
            self.window.fill((0, 0, 0))
            self.block.collision()
            self.block.draw()
            self.ball.move()
            self.ball.draw()
            self.slider.draw()

            self.display_life()
            self.display_score()
            self.game_reset()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.slider.move_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.slider.move_right = True
                    elif event.key == pygame.K_ESCAPE:
                        self.quit()
                    elif event.key == pygame.K_RETURN:
                        self.reset_game()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.slider.move_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.slider.move_right = False

                elif event.type == GAME_GLOBALS.QUIT:
                    self.quit()

            if self.life <= -1:
                play = False
                self.game_over()

            self.slider.move()
            pygame.display.update()

            # Regulate frame rate to 60 FPS
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    while True:
        game.play()
