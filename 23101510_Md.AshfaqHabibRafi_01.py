# from OpenGL.GL import *
# from OpenGL.GLUT import *
# import random
# import math

# window_width, window_height = 800, 600

# num_drops_x = 40
# num_drops_y = 20        #making grid 40col*20row=800 drops
# drop_length = 0.06

# tilt_angle = 0.0       
# target_tilt_angle = 0.0
# max_tilt = math.radians(30)  

# background_brightness = 1.0  
# target_brightness = 1.0

# class RainLine:
#     def __init__(self, x, y):
#         self.x = x          
#         self.y = y
#         self.speed = random.uniform(0.005, 0.015)

#     def fall(self):
#         self.y -= self.speed
#         if self.y < -1.0:
#             self.y = 1.0    # reseting y and making it start from top[looping]


# rain_lines = []

# def init_rain():
#     global rain_lines
#     rain_lines = []
#     for i in range(num_drops_x):
#         for j in range(num_drops_y):
#             x = -1.0 + i * (2.0 / num_drops_x)      #square screen,evenly spaces drops in the screen
#             y = 1.0 - j * (2.0 / num_drops_y)
#             rain_lines.append(RainLine(x, y))       #drop position,random speed

# def draw_rain():
#     glColor3f(1 - background_brightness, 1 - background_brightness, 1.0)    #when day (0,0,1) night(1,1,1)white
#     glBegin(GL_LINES)
#     dx = drop_length * math.sin(tilt_angle)     #drop move sideway
#     dy = drop_length * math.cos(tilt_angle)     #vertical lenght
#     for drop in rain_lines:
#         glVertex2f(drop.x, drop.y)
#         glVertex2f(drop.x + dx, drop.y - dy)    #tilt line
#     glEnd()

# def draw_ground():
#     glBegin(GL_TRIANGLES)
#     glColor3f(0.2, 0.6, 0.2)    #green color
#     glVertex2f(-1.0, -1.0)
#     glVertex2f(1.0, -1.0)
#     glVertex2f(1.0, -0.5)
#     glVertex2f(-1.0, -1.0)      #2 trinagles creating 1 rectangle ground
#     glVertex2f(1.0, -0.5)
#     glVertex2f(-1.0, -0.5)
#     glEnd()

# def draw_house():
     
#     glColor3f(0.6, 0.3, 0.2)    #(brown color)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(-0.4, -0.5)
#     glVertex2f(0.4, -0.5)
#     glVertex2f(0.4, 0.0)    # Main house body
#     glVertex2f(0.4, 0.0)
#     glVertex2f(-0.4, 0.0)
#     glVertex2f(-0.4, -0.5)
#     glEnd()
    
     
#     glColor3f(0.8, 0.1, 0.1)    #(red color)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(-0.45, 0.0)  # Roof
#     glVertex2f(0.0, 0.4)
#     glVertex2f(0.45, 0.0)
#     glEnd()
      
#     glColor3f(0.2, 0.1, 0.0)    #(dark brown color)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(-0.1, -0.5)
#     glVertex2f(0.1, -0.5)
#     glVertex2f(0.1, -0.2)   # Door
#     glVertex2f(0.1, -0.2)
#     glVertex2f(-0.1, -0.2)
#     glVertex2f(-0.1, -0.5)
#     glEnd()
    
#     glColor3f(0.7, 0.9, 1.0)    #light blue color
#     glBegin(GL_TRIANGLES)
#     glVertex2f(-0.3, -0.15)
#     glVertex2f(-0.2, -0.15)
#     glVertex2f(-0.2, -0.05)     # Left window
#     glVertex2f(-0.2, -0.05)
#     glVertex2f(-0.3, -0.05)
#     glVertex2f(-0.3, -0.15)
#     glEnd()
    
#     glColor3f(0.7, 0.9, 1.0) #light blue color
#     glBegin(GL_TRIANGLES)
#     glVertex2f(0.2, -0.15)
#     glVertex2f(0.3, -0.15)
#     glVertex2f(0.3, -0.05)  # Right window 
#     glVertex2f(0.3, -0.05)
#     glVertex2f(0.2, -0.05)
#     glVertex2f(0.2, -0.15)
#     glEnd()
    
#     glColor3f(0.3, 0.3, 0.3)    # Window frames (dark gray color)
#     glLineWidth(2.0)
    
#     glBegin(GL_LINE_LOOP)   
#     glVertex2f(-0.3, -0.15)
#     glVertex2f(-0.2, -0.15)
#     glVertex2f(-0.2, -0.05) # Left window frame
#     glVertex2f(-0.3, -0.05)
#     glEnd()
    
#     glBegin(GL_LINES)
#     glVertex2f(-0.25, -0.15)
#     glVertex2f(-0.25, -0.05)    # Left window cross
#     glVertex2f(-0.3, -0.1)
#     glVertex2f(-0.2, -0.1)
#     glEnd()
    
#     glBegin(GL_LINE_LOOP)
#     glVertex2f(0.2, -0.15)
#     glVertex2f(0.3, -0.15)
#     glVertex2f(0.3, -0.05)  # Right window frame
#     glVertex2f(0.2, -0.05)
#     glEnd()
    
#     glBegin(GL_LINES)
#     glVertex2f(0.25, -0.15)
#     glVertex2f(0.25, -0.05) # Right window cross
#     glVertex2f(0.2, -0.1)
#     glVertex2f(0.3, -0.1)
#     glEnd()

     
#     glColor3f(0.8, 0.6, 0.0)    #(golden color)
#     glPointSize(6.0)
#     glBegin(GL_POINTS)  # Door knob
#     glVertex2f(0.07, -0.35)
#     glEnd()

# def display():
#     glClearColor(background_brightness, background_brightness, background_brightness, 1.0)
#     glClear(GL_COLOR_BUFFER_BIT)
#     draw_ground()
#     draw_house()
#     draw_rain()
#     glutSwapBuffers()

# def idle():
#     global tilt_angle, background_brightness
#     tilt_angle += (target_tilt_angle - tilt_angle) * 0.05
#     background_brightness += (target_brightness - background_brightness) * 0.01

#     for drop in rain_lines:
#         drop.fall()

#     glutPostRedisplay()

# def special_keys(key, x, y):
#     global target_tilt_angle
#     if key == GLUT_KEY_LEFT:
#         target_tilt_angle = max(target_tilt_angle - math.radians(5), -max_tilt)
#     elif key == GLUT_KEY_RIGHT:
#         target_tilt_angle = min(target_tilt_angle + math.radians(5), max_tilt)

# def keyboard(key, x, y):
#     global target_brightness
#     if key in (b'd', b'D'):
#         target_brightness = 1.0
#     elif key in (b'n', b'N'):
#         target_brightness = 0.0

# def main():
#     glutInit()
#     glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
#     glutInitWindowSize(window_width, window_height)
#     glutCreateWindow(b"Assignment Task-1")
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glPointSize(2)
#     init_rain()
#     glutDisplayFunc(display)
#     glutIdleFunc(idle)
#     glutSpecialFunc(special_keys)
#     glutKeyboardFunc(keyboard)
#     glutMainLoop()

# main()



from OpenGL.GL import *
from OpenGL.GLUT import *
import random

window_width, window_height = 800, 600

box_left, box_right = -1.0, 1.0
box_bottom, box_top = -1.0, 1.0     #Boundary

class MovingPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        directions = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
        self.dx, self.dy = random.choice(directions)
        self.color = (random.uniform(0.3, 1), random.uniform(0.3, 1), random.uniform(0.3, 1))
        self.speed = 0.001  # starting speed
        self.blinking = False
        self.blink_phase = 0.0
        self.visible = True

    def update(self, dt, global_speed, frozen):
        if frozen:
            return
        self.x += self.dx * self.speed * global_speed * dt
        self.y += self.dy * self.speed * global_speed * dt

        if self.x <= box_left:
            self.x = box_left
            self.dx *= -1
        elif self.x >= box_right:
            self.x = box_right
            self.dx *= -1
        if self.y <= box_bottom:        #if point hits left or right or top or bottom edge then reverse direction
            self.y = box_bottom
            self.dy *= -1
        elif self.y >= box_top:
            self.y = box_top
            self.dy *= -1

        if self.blinking:
            self.blink_phase += dt / 1000.0
            if self.blink_phase > 1.0:
                self.blink_phase -= 1.0
            self.visible = self.blink_phase < 0.5
        else:
            self.visible = True

points = []
global_speed = 1.0
frozen = False
last_time = 0

def display():
    glClearColor(0, 0, 0, 1)  # black background
    glClear(GL_COLOR_BUFFER_BIT)

    glPointSize(8)  #point size to 8 pixel
    glBegin(GL_POINTS)
    for p in points:
        if p.visible:
            glColor3f(*p.color)
            glVertex2f(p.x, p.y)
    glEnd()

    glutSwapBuffers()

def idle():
    global last_time
    current_time = glutGet(GLUT_ELAPSED_TIME)
    if last_time == 0:
        last_time = current_time
        return
    dt = current_time - last_time
    last_time = current_time

    for p in points:
        p.update(dt, global_speed, frozen)

    glutPostRedisplay()

def mouse(button, state, x, y):
    if state != GLUT_DOWN:
        return

    c_x = (x / window_width) * 2 - 1
    c_y = 1 - (y / window_height) * 2

    if button == GLUT_RIGHT_BUTTON:
        points.append(MovingPoint(c_x, c_y))
        print(f"Point created at co-ords: ({c_x:.3f}, {c_y:.3f})")

    elif button == GLUT_LEFT_BUTTON:
        if len(points) == 0:
            return
        any_blinking = any(p.blinking for p in points)
        new_blinking_state = not any_blinking
        for p in points:
            p.blinking = new_blinking_state
        print("Blinking ON" if new_blinking_state else "Blinking OFF")

def keyboard(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen
        print(f"Points {'frozen' if frozen else 'unfrozen'}")

def special_keys(key, x, y):
    global global_speed
    if frozen:
        return
    if key == GLUT_KEY_UP:
        old_speed = global_speed
        global_speed *= 1.2
        if global_speed > 10:
            global_speed = 10
        print(f"Speed increased from {old_speed:.3f} to {global_speed:.3f}")
    elif key == GLUT_KEY_DOWN:
        old_speed = global_speed
        global_speed /= 1.2
        if global_speed < 0.1:
            global_speed = 0.1
        print(f"Speed decreased from {old_speed:.3f} to {global_speed:.3f}")

def reshape(width, height):
    global window_width, window_height
    window_width = width
    window_height = height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Assignment Task-2")
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutReshapeFunc(reshape)
    glutMainLoop()

main()

