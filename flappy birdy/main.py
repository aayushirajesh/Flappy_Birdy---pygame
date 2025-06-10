import pygame, random
from pygame.locals import *

pygame.init()   # initialize pygame modules  //MUST ALWAYS BE THERE
clock = pygame.time.Clock()   # used to control the game’s speed
fps = 60   # set game to run at 60 frames per second

# Creating Window
screen_width = 600
screen_height = screen_width
screen = pygame.display.set_mode((screen_width,screen_height))   # WIDTH(X) and HEIGHT(Y)   // creates actual window where game runs
pygame.display.set_caption("Flappy Birdy")   # title of window
icon = pygame.image.load('bird1.png') # load image into icon variable
pygame.display.set_icon(icon)   # display image in icon variable as icon for game

# load required images and resize if needed
bg = pygame.image.load('bg.png')
bg = pygame.transform.scale(bg, (600, 480))   # resize bg to desired size
ground = pygame.image.load('ground.png')
button_img = pygame.image.load('restart.png')

# Game specific variables
run = True   # Game loop runs while run is True
ground_scroll = 0   # To move ground image sideways
scroll_speed = 4   # Speed of ground and pipes
flying = False   # True when bird starts flying
game_over = False   # True when bird crashes
pipe_gap = 150   # gap between top and bottom pipes
pipe_frequency = 1500   # Time (milliseconds) between pipe appearances
last_pipe = pygame.time.get_ticks() - pipe_frequency   # Timer for when last pipe was created
score = 0  #global variable      # Player score
pass_pipe = False   # Helps count score when bird passes a pipe
font = pygame.font.SysFont('Arial', 60)   # Set font style and size
white = (255, 255, 255)   # RGB code for white

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)  # render text as an image
    screen.blit(img, (x, y))   # blit(img, (x, y)) = place text image on screen at (x, y)
def reset_game():
    pipe_group.empty()   # remove all pipes
    flappy.rect.x = 100   # reset bird's x position
    flappy.rect.y = int(screen_height/2)   # reset bird's y position
    score = 0  #local variable      # reset score
    return score   # return new score to update global variable

class Bird(pygame.sprite.Sprite):   # inherit pygame’s sprite class
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []   # list of bird images for animation
        self.index = 0    # Current image index
        self.counter = 0  # Timer for animation
        for num in range(1, 4):
            img = pygame.image.load(f'bird{num}.png')   # load images
            self.images.append(img)   # add images to list
        self.image = self.images[self.index]   # current image
        self.rect = self.image.get_rect()   # create rectangle around bird (used for position and collision)
        self.rect.center = [x, y]   # place bird at (x, y)
        self.vel = 0  #velocity of bird
        self.clicked = False  #nothing has been clicked    // to detect mouse clicks

    def update(self):

        #gravity
        if flying==True:
            self.vel += 0.5  # accelerate downward    // fall down slowly
            if self.vel > 8:
                self.vel = 8  # max falling speed
            if self.rect.bottom < 480:   # stop at ground
                self.rect.y += int(self.vel)   # move bird down (or up) based on how fast its going

        if game_over == False:

            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:    # mouse clicked
                self.clicked = True
                self.vel = -10   # jump up
            if pygame.mouse.get_pressed()[0] == 0:    # mouse released
                self.clicked = False

            #animate bird flapping
            self.counter += 1
            flap_cooldown = 5                    # frames between flap changes
            if self.counter > flap_cooldown:     # counter > cooldown time
                self.counter = 0
                self.index += 1                  # move to next image
                if self.index >= len(self.images):  #position of index >= position of last index of images_list
                    self.index = 0    # reset index position to 0
            self.image = self.images[self.index]   # display image of bird at index 0 and loop of animation continues

            #rotate bird based on speed
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            #if game over, rotate bird straight down (90 degrees)
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):   
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()

        # position 1 is for top and -1 is for bottom
        if position == 1:   # top pipe
            self.image = pygame.transform.flip(self.image, False, True)    # flip pipe_img upside down
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]   # add gap btw top and bottom pipe(at bottom part of top_pipe)
        if position == -1:   # bottom pipe
            self.rect.topleft = [x, y + int(pipe_gap/2)]   # add gap btw top and bottom pipe(at top part of bottom_pipe)
    
    def update(self):   # to maintain moving animation of pipes
        self.rect.x -= scroll_speed     # move pipe to left
        if self.rect.right < 0:
            self.kill()                 # remove pipe if it goes off screen

class Button():   # restart button
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)      # set position

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()   #get mouse position

        #check if mouse is over button and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action =True
        screen.blit(self.image, (self.rect.x, self.rect.y))   #put button
        
        return action

# create sprite groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

#get button_img's size dynamically to center it.
button_rect = button_img.get_rect()
button = Button((screen_width - button_rect.width) // 2, (screen_height - button_rect.height) // 2, button_img)

# create bird object and add to group
flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)

# game loop
while run:
    clock.tick(fps)                  # control frame rate(60 fps)

    screen.blit(bg, (0,0))           #put bg on screen
    bird_group.draw(screen)          #put bird on screen
    bird_group.update()           #update bird logic
    pipe_group.draw(screen)          #put pipes on screen
    screen.blit(ground, (ground_scroll, 480))  #put ground animation on screen

    #check score by checking if bird successfully passed the pipes
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
            pass_pipe = True                       # mark pipe as passed
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1                         # increase score
                pass_pipe = False
    draw_text(str(score), font, white, int(screen_width/2), 20)  # display score
    
    #collision detection -> checking if bird and pipes collide
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    #checking if bird has hit ground
    if flappy.rect.bottom >= 480:   # 480 is height of bg that I changed it to
        game_over = True
        flying = False
    if game_over == False and flying == True:
        #add new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        #scroll ground to left 
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()    # update and move pipes

    #check for game_over and restart
    if game_over == True:
        if button.draw() == True:     # if restart button clicked
            game_over = False
            score = reset_game()      # reset everything

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # to close the window
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()   # refresh screen with all updates    //MUST ALWAYS BE THERE

pygame.quit()
