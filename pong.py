# PONG GAME

# This is a two player pong game. Each player will control their side of paddles
# on the screen. The goal of the game is to not let the bouncing ball miss their 
# respective paddles, or they'll grant a point to the other player when ball hits the wall behind their paddle.
# First Player to reach 11 point wins, and the game will stop working.
# 
# Controls:
# -> Player 1 (left side):
#    - 'q' to move the paddle upwards
#    - 'a' to move the paddle downwards
#
# -> Player 2 (right side):
#    - 'p' to move the paddle upwards
#    - 'l' to move the paddle downwards

import pygame


# User-defined functions
def main():
   # initialize all pygame modules 
   pygame.init()
   
   # create a pygame display window
   pygame.display.set_mode((850, 550))
   
   # set the title of the display window
   pygame.display.set_caption('PONG')   
   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   
   # create a game object
   game = Game(w_surface)
   
   # start the main game loop by calling the play method on the game object
   game.play() 
   
   # quit pygame and clean up the pygame window
   pygame.quit() 

# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # General game attributes
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # Specific pong game attributes
      
      self.size = self.surface.get_size()
      self.center = [self.size[0]//2, self.size[1]//2]
      
      # --- for pong ball ---
      
      self.ball = Ball('white', 5, self.center, [6, 2], self.surface)
      
      # --- for paddles ---
      self.paddle_height = 60
      self.top = (self.size[1]//2) - (self.paddle_height//2)
      self.left_p1 = self.size[0]//2 - 200
      self.left_p2 = self.size[0]//2 + 200
      self.initial_score = 0
      
      # paddle instances
      self.paddle_1 = Paddle('white', self.left_p1, self.top, 20, self.paddle_height, self.initial_score, self.surface) 
      self.paddle_2 = Paddle('white', self.left_p2, self.top, 20, self.paddle_height, self.initial_score, self.surface) 
      
      # --- for scores --- 
      # list of scores of left and right player
      self.scores = [0,0]
      #font size and color for scores
      self.font_size =72
      self.fg_color = pygame.Color('white')
   

   def play(self):
      # play game until close button is clicked.
      # game will stop once either of the player score 11 points 
      # - self is the Game which would be continued over conditions

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:    # until either player scores 11 points
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled
      
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         
         if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
         
         if event.type == pygame.KEYUP:
            self.handle_keyup(event)
   
   def handle_keydown(self, event):
      # Handle the event of KEYDOWN when any keyboard key is pressed, and give commands
      # to move the paddle upwards or downwards
      # - self is the game to handle
      # - event is the event of KEYDOWN which will determine the movement
      
      # The conditional statements are making the paddles move up or down 
      # on basis of the button pressed
      if (event.key == pygame.K_q):
         self.paddle_1.set_velocity(-10) 
      elif event.key == pygame.K_a :
         self.paddle_1.set_velocity(10) 
      
      if event.key == pygame.K_p :
         self.paddle_2.set_velocity(-10) 
      elif event.key == pygame.K_l :
         self.paddle_2.set_velocity(10) 
   
   def handle_keyup(self,event):
      # Handle the event of KEYUP when the key is released, and give commands
      # to stop the already moving paddle 
      # - self is the game to handle
      # - event is the event of KEYUP which will stop the movement
      
      # conditional statements to set the value of velocity to its default value i.e. 0,
      # when the key is released
      if event.key == pygame.K_q or event.key == pygame.K_a:
         self.paddle_1.set_velocity(0) 
      
      if event.key == pygame.K_p or event.key == pygame.K_l:
         self.paddle_2.set_velocity(0) 
   
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.ball.draw()
      self.paddle_1.draw()
      self.paddle_2.draw()
      self.left_score_draw()
      self.right_score_draw()
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects for next frame.
      # - self is the Game to update
      
      self.ball.move(self.paddle_1, self.paddle_2, self.scores)
      self.paddle_1.move()
      self.paddle_2.move()
   
   def left_score_draw(self):
      # Draw the scores of Player 1 (left side) on the left side
      # of the screen 
      # - self is the Game 
      
      # text that has to be displayed
      score_string = str(self.scores[0])
      
      # creating a font object
      font = pygame.font.SysFont('Comic Sans',self.font_size) 
      
      # Creating a textbox by rendering the font
      text_box = font.render(score_string, True, self.fg_color, self.bg_color)
      
      # Computing the location of top_left corner of the text_box on surface
      location = (0,0) 
      
      # Blitting the text on the surface
      self.surface.blit(text_box,location)      

   def right_score_draw(self):
      # Draw the scores of Player 2 (right side) on the right side
      # of the screen 
      # - self is the Game 
      
      # text that has to be displayed
      score_string = str(self.scores[1])
      
      # creating a font object
      font = pygame.font.SysFont('Comic Sans',self.font_size) 
      
      # Creating a textbox by rendering the font
      text_box = font.render(score_string, True, self.fg_color, self.bg_color)
      w = text_box.get_width()    # getting the width of the text box screen
      
      # Computing the location of top_left corner of the text_box on surface
      location = (self.size[0] - w, 0) 
      
      # Blitting the text on the surface
      self.surface.blit(text_box,location)       
   
   def decide_continue(self):
      # Decide whether the game has met the ending conditions, i.e.,
      # Either of the scores have reached 11 points
      # - self is the game to be continued
      
      # loop and conditional statement for situation 
      # if score either player's score reaches 11, game ends
      for i in range(0,2):
         if self.scores[i] == 11:
            self.continue_game = False
   
class Ball:
   # An object in this class represents a Dot that moves 
   
   def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface):
      # Initialize a Dot.
      # - self is the Dot to initialize
      # - color is the pygame.Color of the dot
      # - center is a list containing the x and y int
      #   coords of the center of the dot
      # - radius is the int pixel radius of the dot
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object

      self.color = pygame.Color(dot_color)
      self.radius = dot_radius
      self.center = dot_center
      self.velocity = dot_velocity
      self.surface = surface
      
      self.score = 0
      
   def move(self,p1,p2, scores): # paddle_attribs
      # Change the location of the Dot by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # And it will also increment the score once the ball hit the wall.
      # - self is the Dot         
      # - p1 is the instance of player 1 paddle
      # - p2 is the instance of player 2 paddle
      # - scores is the list of scores of both players
      
      for i in range(0,2):
         self.center[i] = (self.center[i] + self.velocity[i])
         
      size = self.surface.get_size()
      
      # condition of collision with screen
      # Did not use loop to make it easier for incrementing the score
      if self.radius + self.center[0] >= size[0]:
         self.velocity[0] = -self.velocity[0]
         scores[0] += 1
      elif self.radius >= self.center[0]:
         self.velocity[0] = -self.velocity[0]
         scores[1] += 1
      elif self.radius + self.center[1] >= size[1]:
         self.velocity[1] = -self.velocity[1]
      elif self.radius >= self.center[1]:
         self.velocity[1] = -self.velocity[1]      
      
      
      # condition of collision with paddles
      # conditional statements making sure that ball bounces off
      # only when its approaching the paddle from opposite side of the screen
      # with respect to them
      if self.velocity[0] < 0:
         if p1.collide_points(self.center):
            self.velocity[0] = -self.velocity[0]
      
      elif self.velocity[0] > 0:
         if p2.collide_points(self.center):
            self.velocity[0] = -self.velocity[0]
   
   
   def draw(self):
      # Draw the dot on the surface
      # - self is the Dot
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)


class Paddle:
   # An object in the class represents a paddle for the game 'Pong'
   # that will be moved according to user's command.
   
   def __init__(self,paddle_color,left, top, width, height, score, screen):
      # Initialize the Paddle's attributes
      # self is the Paddle to initialize
      # color is the color of paddle
      # left is x co-ordinate value of the top left corner of Paddle
      # top is y co-ordinate value of the top left corner of Paddle
      # width is the width of the Paddle
      # height is the height of the paddle
      # screen is the surface on which paddle has to be drawn on
      
      self.color = pygame.Color(paddle_color)
      self.left = left
      self.top = top
      self.width = width
      self.height = height
      self.screen = screen
      self.score = score
      
      self.velocity = 0
      self.size = screen.get_size()
   
   def set_velocity(self,velocity):
      # will set the value of the velocity of the paddle
      # - self is the paddle of whose velocity has to be set
      
      self.velocity = velocity
   
   def move(self):
      # update the movement of the paddle as per the velocity
      # of the paddle
      # - self is the Paddle to be moved
      
      self.top = self.top + self.velocity    
      
      # Will prevent the paddles from going beyond the screen 
      # by making it stick its positions at the extremities 
      if self.top <= 0:
         self.top = 0
      elif self.top + self.height >= self.size[1]:
         self.top = self.size[1] - self.height 
   
   def draw(self):
      # draw the Paddle on the surface of the game
      # - self is the Paddle to be drawn
      
      pygame.draw.rect(self.screen, self.color, pygame.Rect(self.left,self.top,self.width,self.height))
      
   def collide_points(self,center):
      # Will check the condition if ball hits the paddle or not 
      # - self is the Paddle on which the ball hitting condition is being assessed
      # - center is the location of center (x,y co-ordinates) of the center
      
      return pygame.Rect(self.left,self.top,self.width,self.height).collidepoint(center)
   
main()