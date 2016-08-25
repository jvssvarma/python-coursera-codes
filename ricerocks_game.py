#Name: Jampana Santosh Varma Venkata Subramaniya
# program template for Spaceship
import simplegui
import math
import random

WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started=True
velrate=1

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(canvas,rock_group):
    for tmp in rock_group:
        tmp.draw(canvas)
        if tmp.update():
            rock_group.remove(tmp)

def group_collide(group,other_object):
    numcol=0
    for tmp in set(group):
        if tmp.collide(other_object):
            group.remove(tmp)
            numcol+=1
    return numcol

def group_group_collide(group1,group2):
    numcol=0
    for tmp in set(group1):
        tmpcol=group_collide(group2,tmp)
        if tmpcol:
            numcol+=tmpcol
            group1.remove(tmp)
    return numcol
        
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            self.image_center[0]=135
        else:
            self.image_center[0]=45
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,self.angle)

    def update(self):
        self.vel[0]*=0.98
        self.vel[1]*=0.98
        self.pos[0]+=self.vel[0]
        self.pos[0]%=WIDTH
        self.pos[1]+=self.vel[1]
        self.pos[1]%=HEIGHT
        self.angle+=self.angle_vel
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
        if self.thrust:
            foward=angle_to_vector(self.angle)
            self.vel[0]+=foward[0]/10
            self.vel[1]+=foward[1]/10
            
    def shoot(self):
        global a_missile
        foward=angle_to_vector(self.angle)
        tmppos=[self.pos[0]+45*foward[0],self.pos[1]+45*foward[1]]
        tmpvel=[self.vel[0]+foward[0]*5,self.vel[1]+foward[1]*5]
        a_missile = Sprite(tmppos, tmpvel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.append(a_missile)
        missile_sound.play()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            tmpcenter=[self.image_center[0]+self.age*self.image_size[0],self.image_center[1]]
            canvas.draw_image(self.image, tmpcenter, self.image_size, self.pos, self.image_size,self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,self.angle)
    
    def update(self):
        self.pos[0]+=self.vel[0]
        self.pos[0]%=WIDTH
        self.pos[1]+=self.vel[1]
        self.pos[1]%=HEIGHT
        self.angle+=self.angle_vel
        
        self.age+=1
        if self.age>self.lifespan:
            return True
        else:
            return False
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def collide(self,other_object):
        if dist(self.get_position(),other_object.get_position())<self.get_radius()+other_object.get_radius():
            foward=angle_to_vector(self.angle)
            tmppos=[self.pos[0]+self.get_radius(),self.pos[1]+self.get_radius()]
            a_explosion=Sprite(tmppos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.append(a_explosion)
            return True
        else:
            return False

           
def draw(canvas):
    global time,lives,score,rock_group,missile_group,started,explosion_group
    
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    my_ship.draw(canvas)
    process_sprite_group(canvas,rock_group)
    process_sprite_group(canvas,missile_group)
    process_sprite_group(canvas,explosion_group)
    
    canvas.draw_text('lives:'+str(lives), (50, 50), 24, "White")
    canvas.draw_text('score:'+str(score), (WIDTH-100, 50), 24, "White")
    
    if group_collide(rock_group,my_ship):
        lives-=1
        
    if lives==0:
        started=False
        rock_group=[]
        explosion_group=[]
        canvas.draw_image(splash_image,splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        
    if group_group_collide(rock_group,missile_group):
        score+=1

    my_ship.update()
               
def rock_spawner():
    global rock_group,started,velrate
    if not started:return
    
    if len(rock_group)<12:
        pos=[random.random()*WIDTH, random.random()*HEIGHT]
        while dist(my_ship.get_position(),pos)<200:
            pos=[random.random()*WIDTH, random.random()*HEIGHT]
        a_rock = Sprite(pos, [random.random()*velrate, random.random()*velrate], random.random()*2*math.pi, random.random()*0.1, asteroid_image, asteroid_info)
        velrate+=0.2
        rock_group.append(a_rock)
    
def keydown(key):
    if key==simplegui.KEY_MAP['left']:
        my_ship.angle_vel=-0.08
    elif key==simplegui.KEY_MAP['right']:
        my_ship.angle_vel=0.08
    elif key==simplegui.KEY_MAP['up']:
        my_ship.thrust=True
    elif key==simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key==simplegui.KEY_MAP['left']:
        my_ship.angle_vel=0
    elif key==simplegui.KEY_MAP['right']:
        my_ship.angle_vel=0
    elif key==simplegui.KEY_MAP['up']:
        my_ship.thrust=False
        
def mouse_handler(pos):
    global started,lives,score,velrate,my_ship
    if started==False and dist(pos,[WIDTH / 2, HEIGHT / 2])<200:
        started=True
        lives=3
        score=0
        velrate=1
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group=[]
missile_group=[]
explosion_group=[]

frame.set_draw_handler(draw)

frame.set_keydown_handler(keydown)  
frame.set_keyup_handler(keyup)  
frame.set_mouseclick_handler(mouse_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()