# Implementation of classic arcade game Pong

import simplegui
import random


WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
position_ball = [WIDTH/2,HEIGHT/2]
velocity_ball = [-random.randrange(60, 180)/60,random.randrange(120, 240)/60]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2

def ball_init(right):
    global position_ball, velocity_ball
    position_ball = [WIDTH/2,HEIGHT/2]
    velocity_ball[1] = -random.randrange(60, 180)/60
    if right == True:
        velocity_ball[0] = random.randrange(120, 240)/60
    else:
        velocity_ball[0] = -random.randrange(120, 240)/60
    pass

def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  
    global score1, score2  
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    ball_init(0 == random.randrange(0,11) % 2)
    pass

def draw(c):
    global score1, score2, paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos, position_ball, velocity_ball
    if paddle1_pos < (HALF_PAD_HEIGHT) and paddle1_vel < 0:
        paddle1_vel = 0
    if paddle2_pos < (HALF_PAD_HEIGHT) and paddle2_vel < 0:
        paddle2_vel = 0
    if paddle1_pos > (HEIGHT - (HALF_PAD_HEIGHT)) and paddle1_vel > 0:
        paddle1_vel = 0
    if paddle2_pos > (HEIGHT - (HALF_PAD_HEIGHT)) and paddle2_vel > 0:
        paddle2_vel = 0    
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel        
    
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    c.draw_polygon([(0, paddle1_pos-HALF_PAD_HEIGHT), (0, paddle1_pos+HALF_PAD_HEIGHT), (PAD_WIDTH-2, paddle1_pos+HALF_PAD_HEIGHT),(PAD_WIDTH-2,paddle1_pos-HALF_PAD_HEIGHT)], PAD_WIDTH-1, "White","White")
    c.draw_polygon([(WIDTH, paddle2_pos-HALF_PAD_HEIGHT), (WIDTH, paddle2_pos+HALF_PAD_HEIGHT), (WIDTH-PAD_WIDTH+2, paddle2_pos+HALF_PAD_HEIGHT),(WIDTH-PAD_WIDTH+2,paddle2_pos-HALF_PAD_HEIGHT)], PAD_WIDTH-1, "White","White")
    
    position_ball[0] += velocity_ball[0]
    position_ball[1] += velocity_ball[1]
    if position_ball[1] >= (HEIGHT - BALL_RADIUS) or position_ball[1] <= (BALL_RADIUS):
        velocity_ball[1] = -velocity_ball[1]
    if position_ball[0] <= (PAD_WIDTH + BALL_RADIUS):
        if position_ball[1] < (paddle1_pos - HALF_PAD_HEIGHT) or position_ball[1] > (paddle1_pos + HALF_PAD_HEIGHT):
            ball_init(True)
            score2 += 1
        else:
            velocity_ball[0] = -velocity_ball[0] * 1.1
            
    if  position_ball[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):
        if position_ball[1] < (paddle2_pos - HALF_PAD_HEIGHT) or position_ball[1] > (paddle2_pos + HALF_PAD_HEIGHT):
            ball_init(False)
            score1 += 1
        else:
            velocity_ball[0] = -velocity_ball[0] * 1.1
    
    c.draw_circle(position_ball, BALL_RADIUS, 2, "Red", "White")
    c.draw_text(str(score1), (170, 50), 36, "Red")
    c.draw_text(str(score2), (400, 50), 36, "Red")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -4
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 4
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -4
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 4
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)


# start frame
init()
frame.start()
