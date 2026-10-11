from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

WIDTH = 800
HEIGHT = 600
catcher_x = WIDTH // 2
catcher_y = 50
catcher_width = 100
catcher_height = 25
diamond_x = random.randint(50, WIDTH - 50)
diamond_y = HEIGHT - 50
diamond_size = 10
diamond_speed = 100 
game_over = False
paused = False
score = 0
last_time = time.time()
diamond_color = [random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)]

button_size = 40
button_y = HEIGHT - 60
restart_button = {'x': 50, 'y': button_y, 'width': button_size, 'height': button_size}
pause_button = {'x': WIDTH // 2 - button_size // 2, 'y': button_y, 'width': button_size, 'height': button_size}
exit_button = {'x': WIDTH - 90, 'y': button_y, 'width': button_size, 'height': button_size}

def find_zone(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    
    if abs(dx) >= abs(dy):  
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:  
            return 7
    else:  
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:  
            return 6

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y
    else:
        return x, y

def convert_from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    else:
        return x, y

def midpoint_line_zone0(x1,y1,x2,y2):
    points = []
    dx = x2-x1
    dy = y2-y1
    
    d = 2 * dy-dx
    inc_e = 2 * dy
    inc_ne = 2 * (dy-dx)
    y = y1
    
    for x in range(x1,x2 + 1):
        points.append((x, y))
        if d > 0:
            d += inc_ne
            y += 1
        else:
            d += inc_e
    
    return points

def draw_line_all_zones(x1,y1,x2,y2):
    if x1 == x2 and y1 == y2:
        return [(x1, y1)]

    orig_x1, orig_y1, orig_x2, orig_y2 = x1, y1, x2, y2
    
    zone = find_zone(x1, y1, x2, y2)
    
    x1_z0, y1_z0 = convert_to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = convert_to_zone0(x2, y2, zone)
    
    if x1_z0 > x2_z0:
        x1_z0, x2_z0 = x2_z0, x1_z0
        y1_z0, y2_z0 = y2_z0, y1_z0
    
    points_z0 = midpoint_line_zone0(x1_z0, y1_z0, x2_z0, y2_z0)
    
    points = []
    for x, y in points_z0:
        orig_x, orig_y = convert_from_zone0(x, y, zone)
        points.append((orig_x, orig_y))
    
    return points

def draw_pixel(x,y):
    glVertex2f(x,y)

def draw_line(x1,y1,x2,y2):
    points = draw_line_all_zones(int(x1), int(y1), int(x2), int(y2))
    glBegin(GL_POINTS)
    for x, y in points:
        draw_pixel(x, y)
    glEnd()

def draw_diamond(x,y,size):
    top = (x,y+size)
    right = (x+size,y)
    bottom = (x,y-size)
    left = (x-size,y)
    
    draw_line(top[0],top[1],right[0],right[1])  
    draw_line(right[0],right[1],bottom[0],bottom[1]) 
    draw_line(bottom[0],bottom[1],left[0],left[1])  
    draw_line(left[0],left[1],top[0],top[1])       

def draw_catcher(x,y,width,height):
    bottom_left = (x-width//4,y)  
    bottom_right = (x+width//4,y)  
    top_left = (x-width//2,y+height) 
    top_right = (x+width//2,y+height)
    
    draw_line(top_left[0],top_left[1],top_right[0],top_right[1])        
    draw_line(top_left[0],top_left[1],bottom_left[0],bottom_left[1])     
    draw_line(top_right[0],top_right[1],bottom_right[0],bottom_right[1]) 
    draw_line(bottom_left[0],bottom_left[1],bottom_right[0],bottom_right[1]) 

def draw_restart_button(x,y,size):
    center_y = y+size//2
    
    draw_line(x+8, center_y, x+size-8, center_y)
    
    arrow_length = size//3
    draw_line(x+8,center_y, x+8 + arrow_length, center_y+arrow_length//2)  
    draw_line(x+8, center_y, x+8+arrow_length, center_y-arrow_length // 2)  

def draw_pause_button(x, y, size):
    if paused:
        left_x = x+8
        right_x = x+size-8
        mid_y = y + size//2
        top_y = y + size-8
        bottom_y = y+8
        
        draw_line(left_x, bottom_y, left_x, top_y)          
        draw_line(left_x, top_y, right_x, mid_y)            
        draw_line(right_x, mid_y, left_x, bottom_y)         
    else:
        left_rect_x1 = x+10
        left_rect_x2 = x+16
        right_rect_x1 = x+24
        right_rect_x2 = x+30
        top_y = y+size-8
        bottom_y = y+8
        
        draw_line(left_rect_x1, bottom_y, left_rect_x1, top_y)   
        draw_line(left_rect_x1, top_y, left_rect_x2, top_y)      
        draw_line(left_rect_x2, top_y, left_rect_x2, bottom_y)   
        draw_line(left_rect_x2, bottom_y, left_rect_x1, bottom_y)
        
        draw_line(right_rect_x1, bottom_y, right_rect_x1, top_y)  
        draw_line(right_rect_x1, top_y, right_rect_x2, top_y)     
        draw_line(right_rect_x2, top_y, right_rect_x2, bottom_y)   
        draw_line(right_rect_x2, bottom_y, right_rect_x1, bottom_y) 

def draw_exit_button(x, y, size):
    margin = 10
    draw_line(x + margin, y + margin, x + size - margin, y + size - margin) 
    draw_line(x + size - margin, y + margin, x + margin, y + size - margin)  
    draw_line(x + margin + 1, y + margin, x + size - margin + 1, y + size - margin)  
    draw_line(x + margin, y + margin + 1, x + size - margin, y + size - margin + 1)  
    draw_line(x + size - margin - 1, y + margin, x + margin - 1, y + size - margin)  
    draw_line(x + size - margin, y + margin + 1, x + margin, y + size - margin + 1)

def check_collision(catcher_x, catcher_y, diamond_x, diamond_y):
    catcher_left = catcher_x - catcher_width // 2  
    catcher_right = catcher_x + catcher_width // 2 
    catcher_top = catcher_y + catcher_height
    catcher_bottom = catcher_y

    diamond_left = diamond_x - diamond_size
    diamond_right = diamond_x + diamond_size
    diamond_top = diamond_y + diamond_size
    diamond_bottom = diamond_y - diamond_size
    
    return (catcher_left < diamond_right and
            catcher_right > diamond_left and
            catcher_bottom < diamond_top and
            catcher_top > diamond_bottom)

def reset_game():
    global catcher_x, diamond_x, diamond_y, diamond_speed, game_over, score, diamond_color, paused, last_time
    catcher_x = WIDTH // 2
    diamond_x = random.randint(50, WIDTH - 50)
    diamond_y = HEIGHT - 50
    diamond_speed = 100
    game_over = False
    paused = False
    score = 0
    diamond_color = [random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)]
    last_time = time.time()  
    print("Starting Over")
    glutPostRedisplay() 

def spawn_new_diamond():
    global diamond_x, diamond_y, diamond_speed, diamond_color
    diamond_x = random.randint(diamond_size + 10, WIDTH - diamond_size - 10)
    diamond_y = HEIGHT - 50
    diamond_speed += 10 
    diamond_color = [random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)]

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()  
    glPointSize(2.0)
    glColor3f(0.0, 0.8, 0.8)
    draw_restart_button(restart_button['x'], restart_button['y'], restart_button['width'])  
    glColor3f(1.0, 0.75, 0.0)
    draw_pause_button(pause_button['x'], pause_button['y'], pause_button['width'])
    glColor3f(1.0, 0.0, 0.0)
    draw_exit_button(exit_button['x'], exit_button['y'], exit_button['width'])

    if game_over:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0) 
    draw_catcher(catcher_x, catcher_y, catcher_width, catcher_height)
    
    
    if not game_over:
        glColor3f(diamond_color[0], diamond_color[1], diamond_color[2])
        draw_diamond(diamond_x, diamond_y, diamond_size)
    
    glutSwapBuffers()

def update():
    global diamond_y, last_time, game_over, score
    
    current_time = time.time()
    delta_time = current_time - last_time
    
    if delta_time < 0.016:  
        return
    
    last_time = current_time
    
    if not paused and not game_over:
        diamond_y -= diamond_speed * delta_time
        
        if check_collision(catcher_x, catcher_y, diamond_x, diamond_y):
            score += 1
            print(f"Score: {score}")
            spawn_new_diamond()
        
        elif diamond_y < -diamond_size:
            game_over = True
            print(f"Game Over! Final Score: {score}")
    
    glutPostRedisplay()

def keyboard_special(key, x, y):
    global catcher_x
    
    if key == 27:  
        print("ESC pressed - Force exit!")
        import os
        os._exit(0)
        return
    
    if not game_over and not paused:
        if key == GLUT_KEY_LEFT:
            catcher_x = max(catcher_width // 2, catcher_x - 25)
            glutPostRedisplay()  
        elif key == GLUT_KEY_RIGHT:
            catcher_x = min(WIDTH - catcher_width // 2, catcher_x + 25)
            glutPostRedisplay()  

def keyboard_normal(key, x, y):
    if ord(key) == 27: 
        print("ESC pressed - Force exit!")
        import os
        os._exit(0)  
    elif key == b'q' or key == b'Q':
        print("Q pressed - Quitting game!")
        import os
        os._exit(0)

def mouse_click(button, state, x, y):
    global paused
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print(f"Mouse click: ({x}, {y})")
        y_converted = HEIGHT - y
        print(f"Converted click coordinates: ({x}, {y_converted})")
        print(f"Exit button area: x({exit_button['x']} to {exit_button['x'] + exit_button['width']}), y({exit_button['y']} to {exit_button['y'] + exit_button['height']})")
        
        exit_x_min = exit_button['x'] - 5  # Add some margin
        exit_x_max = exit_button['x'] + exit_button['width'] + 5
        exit_y_min = exit_button['y'] - 5
        exit_y_max = exit_button['y'] + exit_button['height'] + 5
        
        print(f"Extended exit button area (with margin): x({exit_x_min} to {exit_x_max}), y({exit_y_min} to {exit_y_max})")
        
        if (exit_x_min <= x <= exit_x_max and exit_y_min <= y_converted <= exit_y_max):
            print("EXIT BUTTON DETECTED! Exiting immediately...")
            print(f"Goodbye! Final Score: {score}")
            import os
            import sys
            print("Attempting immediate exit...")
            os._exit(0) 
        elif (restart_button['x'] <= x <= restart_button['x'] + restart_button['width'] and
              restart_button['y'] <= y_converted <= restart_button['y'] + restart_button['height']):
            print("Restart button clicked!")
            reset_game()
        elif (pause_button['x'] <= x <= pause_button['x'] + pause_button['width'] and
              pause_button['y'] <= y_converted <= pause_button['y'] + pause_button['height']):
            print("Pause/Play button clicked!")
            paused = not paused
            if paused:
                print("Game Paused")
            else:
                print("Game Resumed")
        else:
            print("Click was not on any button")

def exit_game():
    print("Exiting game...")
    import sys
    sys.exit(0)

def init_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0) 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    """Main function - entry point"""
    print("=== Catch the Diamonds! ===")
    print("Controls:")
    print("- Left/Right Arrow Keys: Move catcher")
    print("- Left Click Buttons:")
    print("  * Teal Arrow (Left): Restart game")
    print("  * Amber Play/Pause (Center): Toggle pause")
    print("  * Red X (Right): Exit game")
    print("Objective: Catch falling diamonds to score points!")
    print("Game starts now...\n")
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")
    init_opengl()
    glutDisplayFunc(display)
    glutSpecialFunc(keyboard_special)
    glutKeyboardFunc(keyboard_normal) 
    glutMouseFunc(mouse_click)
    glutIdleFunc(update) 
    glutMainLoop()
main()