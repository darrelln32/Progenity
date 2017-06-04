# dsn32 - INTERACTIVE PYTHON CLASS
# Implementation of classic arcade game Pong
#

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
MID_WIDTH = WIDTH / 2
MID_HEIGHT = HEIGHT / 2
LEFT = False
RIGHT = True

# paddle variables
PADDLE1_POS = HEIGHT / 2.5
PADDLE2_POS = HEIGHT / 2.5
PADDLE1_VEL = 0
PADDLE2_VEL = 0
PADDLE_VEL = 5

SCORE1 = 0
SCORE2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
BALL_POS = [MID_WIDTH,MID_HEIGHT]
BALL_VEL = [0,1]

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def SPAWN_BALL(direction):
    global BALL_POS, BALL_VEL # these are vectors stored as lists
    BALL_POS = [MID_WIDTH,MID_HEIGHT]	
    BALL_VEL[0] = -random.randrange(120,240) / 100 
    if direction == True:
        BALL_VEL[0] *= -1
    BALL_VEL[1] = -random.randrange(60, 180) / 100

# define event handlers
# set up pong table for new game
def NEW_GAME():
    global PADDLE1_POS, PADDLE2_POS, PADDLE1_VEL, PADDLE2_VEL  # these are numbers
    global SCORE1, SCORE2  # these are ints
    SCORE1 = 0
    SCORE2 = 0
    SPAWN_BALL(0)
    PADDLE1_POS = HEIGHT / 2.5
    PADDLE2_POS = HEIGHT / 2.5
    
# draw the pong table    
def DRAW(canvas):
    global SCORE1, SCORE2, PADDLE1_POS, PADDLE2_POS, BALL_POS, BALL_VEL
 
    # draw mid line and gutters
    canvas.draw_line([MID_WIDTH, 0],[MID_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball AND determine whether paddle and ball collide 
    BALL_POS[0] += BALL_VEL[0]
    BALL_POS[1] += BALL_VEL[1]
    if BALL_POS[0] <= (BALL_RADIUS + PAD_WIDTH) or BALL_POS[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):        
        BALL_VEL[0] *= -1
        if (BALL_POS[0] > MID_WIDTH):             
            if (BALL_POS[1] < PADDLE2_POS or BALL_POS[1] > PADDLE2_POS + PAD_HEIGHT):
                SCORE1 += 1 
                SPAWN_BALL(LEFT) 
            else: BALL_VEL[0] += .1 * BALL_VEL[0]
        if (BALL_POS[0] < MID_WIDTH):
            if (BALL_POS[1] < PADDLE1_POS or BALL_POS[1] > PADDLE1_POS + PAD_HEIGHT):
                SCORE2 += 1
                SPAWN_BALL(RIGHT)
            else: BALL_VEL[0] += .1 * BALL_VEL[0]
    if BALL_POS[1] <= BALL_RADIUS or BALL_POS[1] >= (HEIGHT - BALL_RADIUS):
        BALL_VEL[1] *= -1
    
    # draw ball
    canvas.draw_circle(BALL_POS, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    global PADDLE1_VEL, PADDLE2_VEL
    if (PADDLE1_POS <= HEIGHT - PAD_HEIGHT and PADDLE1_VEL > 0) or (PADDLE1_POS >= 0 and PADDLE1_VEL < 0):
        PADDLE1_POS += PADDLE1_VEL
    elif (PADDLE2_POS <= HEIGHT - PAD_HEIGHT and PADDLE2_VEL > 0) or (PADDLE2_POS >= 0 and PADDLE2_VEL < 0):
        PADDLE2_POS += PADDLE2_VEL  
    
    # draw paddles
    canvas.draw_polygon([[0, PADDLE1_POS], [PAD_WIDTH, PADDLE1_POS],[PAD_WIDTH, (PADDLE1_POS) + PAD_HEIGHT],[0, (PADDLE1_POS) + PAD_HEIGHT]],1, "green", "white") 
    canvas.draw_polygon([[WIDTH, PADDLE2_POS], [WIDTH - PAD_WIDTH, PADDLE2_POS], [WIDTH - PAD_WIDTH, PADDLE2_POS + PAD_HEIGHT], [WIDTH, PADDLE2_POS + PAD_HEIGHT]],1, "green", "white")
        
    # draw scores
    canvas.draw_text(str(SCORE1), [225, 100], 60, "Red", "sans-serif")    
    canvas.draw_text(str(SCORE2), [350, 100], 60, "Red", "sans-serif")
        
def KEY_DOWN(key):
    global PADDLE1_VEL, PADDLE2_VEL, PADDLE_VEL    
    if key == simplegui.KEY_MAP["w"]:
        PADDLE1_VEL = -PADDLE_VEL     
    elif key == simplegui.KEY_MAP["s"]:
        PADDLE1_VEL = PADDLE_VEL  
    if key == simplegui.KEY_MAP["down"]:
        PADDLE2_VEL = PADDLE_VEL    
    elif key == simplegui.KEY_MAP["up"]:
        PADDLE2_VEL = -PADDLE_VEL 

def KEY_UP(key):
    global PADDLE1_VEL, PADDLE2_VEL
    if key == simplegui.KEY_MAP["w"]:
        PADDLE1_VEL = 0
    elif key == simplegui.KEY_MAP["s"]:
        PADDLE1_VEL = 0
    if key == simplegui.KEY_MAP["down"]:
        PADDLE2_VEL = 0
    elif key == simplegui.KEY_MAP["up"]:
        PADDLE2_VEL = 0

# create frame
f = simplegui.create_frame("PONG", WIDTH, HEIGHT)
f.set_canvas_background("blue")
f.set_draw_handler(DRAW)
f.set_keydown_handler(KEY_DOWN)
f.set_keyup_handler(KEY_UP)
f.add_button("RESTART", NEW_GAME, 150)


# start frame
NEW_GAME()
f.start()
