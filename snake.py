import pygame

import mar 
import Fruit


class Game():
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)

    def __init__(self, screen_width, screen_height, block_size):
       
        pygame.init()

        self.game_over = False

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.block_size = block_size

        
        self.game_font = pygame.font.SysFont(None, 25)
        self.running = True

      
        self.game_display = pygame.display.set_mode((self.screen_width, self.screen_height))

        
        self.clock = pygame.time.Clock()
        self.fps = 15

       
        self.snake = mar(self.game_display, self.block_size)

       
        self.fruit = Fruit(self.screen_width, self.screen_height, self.block_size)

       
        pygame.display.set_caption("Snake")

    def main_loop(self):
        while self.running:

            
            if self.game_over:
                self.game_over_dialog()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.turn_left()
                        break
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.turn_right()
                        break
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.turn_up()
                        break
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.turn_down()
                        break

                   
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game()

          
            self.snake.move()
           
            if self.check_collision():
                self.game_over = True

            
            if self.check_fruit_collision():
                self.snake.add_segment()
                self.fruit.respawn(self.screen_width, self.screen_height, self.snake)

            
            self.game_display.fill(self.white)
            self.draw_fruit(self.fruit)
            self.draw_snake(self.snake)
            pygame.display.flip()
           
            self.clock.tick(self.fps)

    
    def check_collision(self):
        if self.snake.segments[0].pos_x < 0 or \
                self.snake.segments[0].pos_x > self.screen_width - self.snake.block_size:
            return True
        if self.snake.segments[0].pos_y < 0 or \
                self.snake.segments[0].pos_y > self.screen_height - self.snake.block_size:
            return True

        
        head_pos_x = self.snake.segments[0].pos_x
        head_pos_y = self.snake.segments[0].pos_y
        for s in self.snake.segments[1:]:
            if head_pos_x == s.pos_x and head_pos_y == s.pos_y:
                return True
        return False

   
    def check_fruit_collision(self):
        if self.fruit.pos_y == self.snake.segments[0].pos_y and self.fruit.pos_x == self.snake.segments[0].pos_x:
            return True
        return False

    
    def put_message(self, message):
        pause_text = self.game_font.render(message, True, self.red)
        self.game_display.blit(pause_text, [self.screen_width / 2, self.screen_height / 2])

   
    def game_over_message(self):
        message = "Game over, press ENTER/SPACE to continue or ESC to quit"
        pause_text = self.game_font.render(message, True, self.red)
        self.game_display.blit(pause_text, [self.screen_width / 5, self.screen_height / 2])

    
    def pause_game(self):
        paused = True
        self.put_message("Game is Paused")
        pygame.display.update()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
            self.clock.tick(30)

    
    def game_over_dialog(self):
        while self.game_over:
            self.game_display.fill(self.white)
            self.game_over_message()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.reset_game()
                        return
                    if event.key == pygame.K_ESCAPE:
                        self.exit_game()

    
    def reset_game(self):
        self.snake.reset_snake()
        self.game_over = False
        self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
        pygame.display.flip()

   
    def draw_snake(self, snake):
        for s in self.snake.segments:
            self.game_display.fill(self.snake.color, rect=[s.pos_x, s.pos_y, snake.block_size, snake.block_size])

    def draw_fruit(self, fruit):
        self.game_display.fill(self.red, rect=[fruit.pos_x, fruit.pos_y, fruit.block_size, fruit.block_size])

    def exit_game(self):
        pygame.quit()
        quit()