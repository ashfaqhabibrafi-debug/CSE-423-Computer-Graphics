from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_12
from OpenGL.GLUT import GLUT_BITMAP_9_BY_15

last_camera_coords = None
camera_pos = (0, 500, 500)
camera_angle = 0
camera_height = 500
first_person_mode = False

fovY = 120  
GRID_LENGTH = 600 

player_pos = [0, 0, 0]
gun_angle = 0
player_life = 5
game_score = 0
bullets_missed = 0
game_over = False
cheat_mode = False
cheat_vision = False
gun_follow_mode = False
player_fall_angle = 0
time_elapsed = 0

bullets = []
enemies = []
enemy_scale_direction = []

PLAYER_SPEED = 30
BULLET_SPEED = 20
ENEMY_SPEED = 1
MAX_BULLETS_MISSED = 10
NUM_ENEMIES = 5

class Bullet:
    def __init__(self, x, y, z, angle):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.active = True
    
    def update(self):
        if self.active:
            self.x += BULLET_SPEED * math.cos(math.radians(self.angle))
            self.y += BULLET_SPEED * math.sin(math.radians(self.angle))
            if abs(self.x) > GRID_LENGTH or abs(self.y) > GRID_LENGTH:
                self.active = False
                return False
        return True

class Enemy:
    def __init__(self):
        self.respawn()
        self.scale = 1.0
        self.scale_direction = 1
    
    def respawn(self):
        side = random.randint(0, 3)
        if side == 0:
            self.x = random.uniform(-GRID_LENGTH, GRID_LENGTH)
            self.y = GRID_LENGTH
        elif side == 1:
            self.x = GRID_LENGTH
            self.y = random.uniform(-GRID_LENGTH, GRID_LENGTH)
        elif side == 2:
            self.x = random.uniform(-GRID_LENGTH, GRID_LENGTH)
            self.y = -GRID_LENGTH
        else:
            self.x = -GRID_LENGTH
            self.y = random.uniform(-GRID_LENGTH, GRID_LENGTH)
        self.z = 0
    
    def update(self):
        global time_elapsed
        if not game_over:
            dx = player_pos[0] - self.x
            dy = player_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > 0:
                self.x += (dx / distance) * ENEMY_SPEED
                self.y += (dy / distance) * ENEMY_SPEED
            self.scale = 1 + 0.2 * math.sin(time_elapsed)
    
    def collision_player(self):
        dx = self.x - player_pos[0]
        dy = self.y - player_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < 50
    
    def collision_bullet(self, bullet):
        dx = self.x - bullet.x
        dy = self.y - bullet.y
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < 30

def enemy_line(player_pos, player_angle, enemy_pos, tolerance=1):
    gun_dx = math.cos(math.radians(player_angle))
    gun_dy = math.sin(math.radians(player_angle))
    enemy_dx = enemy_pos[0] - player_pos[0]
    enemy_dy = enemy_pos[1] - player_pos[1]
    distance = math.sqrt(enemy_dx**2 + enemy_dy**2)
    if distance == 0:
        return False
    enemy_dx /= distance
    enemy_dy /= distance
    dot_product = gun_dx * enemy_dx + gun_dy * enemy_dy
    angle = math.degrees(math.acos(max(-1, min(1, dot_product))))
    return abs(angle) <= tolerance

def init_game():
    global enemies, bullets, player_pos, gun_angle, player_life, game_score, bullets_missed, game_over, cheat_mode, cheat_vision, gun_follow_mode, player_fall_angle, time_elapsed
    player_pos = [0, 0, 0]
    gun_angle = 0
    player_life = 5
    game_score = 0
    bullets_missed = 0
    game_over = False
    cheat_mode = False
    cheat_vision = False
    gun_follow_mode = False
    player_fall_angle = 0
    time_elapsed = 0
    enemies = []
    for _ in range(NUM_ENEMIES):
        enemies.append(Enemy())
    bullets = []
    print("Game initialized.")

def draw_text(x, y, text, font=None):
    if font is None:
        try:
            font = GLUT_BITMAP_HELVETICA_18
        except:
            try:
                font = GLUT_BITMAP_HELVETICA_12
            except:
                font = GLUT_BITMAP_9_BY_15
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def head():
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 165)
    glutSolidSphere(15, 10, 10)
    glTranslatef(0, 0, -165)

def body():
    glColor3f(0, 0.4, 0)
    glTranslatef(0, 0, 100)
    glScalef(1, 1, 1)
    glutSolidCube(50)
    glScalef(2, 1.43, 0.4)
    glTranslatef(0, 0, -100)

def legs():
    glColor3f(0, 0, 1)
    glTranslatef(0, 10, 50)
    glRotatef(180, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
    glRotatef(-180, 0, 1, 0)
    glTranslatef(0, -10, -50)
    glTranslatef(0, -10, 50)
    glRotatef(180, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
    glRotatef(-180, 0, 1, 0)
    glTranslatef(0, 10, -50)

def arms():
    glColor3f(1, 0.8, 0.6)
    glTranslatef(0, 30, 125)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 25, 10, 10)
    glRotatef(90, 0, 1, 0)
    glTranslatef(0, -30, -125)
    glTranslatef(0, -30, 125)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 25, 10, 10)
    glRotatef(90, 0, 1, 0)
    glTranslatef(0, 30, -125)

def weapon():
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0, 0, 125)
    glRotatef(-90, 0, 1, 0)
    glScalef(1, 1, 2)
    gluCylinder(gluNewQuadric(), 10, 3, 20, 10, 10)
    glScalef(1, 1, 0.5)
    glRotatef(90, 0, 1, 0)
    glTranslatef(0, 0, -125)

def draw_player():
    global player_pos, player_fall_angle, game_over, gun_angle
    glPushMatrix()
    x, y, z = player_pos
    glTranslatef(x, y, z)
    glRotatef(180, 0, 0, 1)
    glRotatef(gun_angle, 0, 0, 1)
    if game_over:
        glRotatef(player_fall_angle, 0, 1, 0)
    glScalef(1, 1, 1)
    body()
    legs()
    head()
    arms()
    weapon()
    glPopMatrix()

def draw_enemy(enemy):
    glPushMatrix()
    glTranslatef(enemy.x, enemy.y, enemy.z)
    glScalef(enemy.scale, enemy.scale, enemy.scale)
    glColor3f(1, 0, 0)
    glutSolidSphere(25, 25, 25)
    glTranslatef(0, 0, 25)
    glColor3f(0, 0, 0)
    glutSolidSphere(15, 25, 25)
    glPopMatrix()

def draw_first_person():
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(750, 150, 0)
    glScalef(3.0, 3.0, 3.0)
    glPopMatrix()
    glLoadIdentity()
    glTranslatef(500, 400, 0)
    glColor3f(1, 1, 1)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(-15, 0)
    glVertex2f(15, 0)
    glVertex2f(0, -15)
    glVertex2f(0, 15)
    glEnd()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()

def draw_bullet(bullet):
    glPushMatrix()
    glTranslatef(bullet.x, bullet.y, bullet.z + 10)
    glColor3f(0, 0, 0)
    glutSolidCube(5)
    glPopMatrix()

def draw_grid_and_boundaries():
    glBegin(GL_QUADS)
    grid_size = 80
    num_squares = int(GRID_LENGTH * 2 / grid_size)
    for i in range(num_squares):
        for j in range(num_squares):
            x1 = -GRID_LENGTH + i * grid_size
            y1 = -GRID_LENGTH + j * grid_size
            x2 = x1 + grid_size
            y2 = y1 + grid_size
            if (i + j) % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)
            else:
                glColor3f(0.7, 0.5, 0.95)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
    glEnd()
    glColor3f(1, 1, 0)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 100)
    glEnd()
    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)
    glEnd()
    glColor3f(1, 0, 1)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 100)
    glEnd()

def fire_bullet():
    global bullets_missed
    if not game_over:
        gun_x = player_pos[0] + 40 * math.cos(math.radians(gun_angle))
        gun_y = player_pos[1] + 40 * math.sin(math.radians(gun_angle))
        bullet = Bullet(gun_x, gun_y, 10, gun_angle)
        bullets.append(bullet)
        print(f"Bullet fired.")

def auto_targeting():
    global gun_angle
    gun_angle += 2
    if gun_angle >= 360:
        gun_angle = 0
    for target in enemies:
        target_coordinates = [target.x, target.y, target.z]
        if enemy_line(player_pos, gun_angle, target_coordinates):
            fire_bullet()
            break

def update_game():
    global player_life, game_score, bullets_missed, game_over, gun_angle, time_elapsed, player_fall_angle
    time_elapsed += 0.05
    if game_over:
        if player_fall_angle < 90:
            player_fall_angle += 2
        return
    if cheat_mode:
        auto_targeting()
    for bullet in bullets[:]:
        if not bullet.update():
            bullets.remove(bullet)
            bullets_missed += 1
            print(f"Bullet missed: {bullets_missed}/{MAX_BULLETS_MISSED}")
    for enemy in enemies:
        enemy.update()
    for bullet in bullets[:]:
        for enemy in enemies:
            if enemy.collision_bullet(bullet):
                bullets.remove(bullet)
                enemy.respawn()
                game_score += 1
                print(f"Enemy hit! Score: {game_score}")
                break
    for enemy in enemies:
        if enemy.collision_player():
            player_life -= 1
            enemy.respawn()
            print(f"Player hit! Life remaining: {player_life}")
            if player_life <= 0:
                game_over = True
                print("GAME OVER: player has no lives left.")
    if not game_over and bullets_missed >= MAX_BULLETS_MISSED:
        game_over = True
        print("GAME OVER: too many bullets missed.")

def keyboardListener(key, x, y):
    global player_pos, gun_angle, cheat_mode, cheat_vision, game_over, gun_follow_mode
    if key == b'w' and not game_over:
        player_pos[0] += PLAYER_SPEED * math.cos(math.radians(gun_angle))
        player_pos[1] += PLAYER_SPEED * math.sin(math.radians(gun_angle))
        player_pos[0] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_pos[0]))
        player_pos[1] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_pos[1]))
    elif key == b's' and not game_over:
        player_pos[0] -= PLAYER_SPEED * math.cos(math.radians(gun_angle))
        player_pos[1] -= PLAYER_SPEED * math.sin(math.radians(gun_angle))
        player_pos[0] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_pos[0]))
        player_pos[1] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_pos[1]))
    elif key == b'a' and not game_over and not cheat_mode:
        gun_angle += 20
        if gun_angle >= 360:
            gun_angle = 0
    elif key == b'd' and not game_over and not cheat_mode:
        gun_angle -= 20
        if gun_angle < 0:
            gun_angle = 355
    elif key == b'c':
        cheat_mode = not cheat_mode
        if cheat_mode:
            print("Cheat mode activated!")
        else:
            print("Cheat mode deactivated!")
    elif key == b'v':
        if cheat_mode and first_person_mode:
            gun_follow_mode = not gun_follow_mode
            if gun_follow_mode:
                print("Gun-following mode activated!")
            else:
                print("Gun-following mode deactivated!")
    elif key == b'r' and game_over:
        init_game()

def specialKeyListener(key, x, y):
    global camera_pos, camera_angle, camera_height, first_person_mode
    if not first_person_mode:
        x_pos, y_pos, z_pos = camera_pos
        if key == GLUT_KEY_UP:
            camera_height += 10
            z_pos = camera_height
        elif key == GLUT_KEY_DOWN:
            camera_height = max(100, camera_height - 20)
            z_pos = camera_height
        elif key == GLUT_KEY_LEFT:
            camera_angle -= 10
            if camera_angle < 0:
                camera_angle = 355
        elif key == GLUT_KEY_RIGHT:
            camera_angle += 10
            if camera_angle >= 360:
                camera_angle = 0
        radius = 700
        x_pos = radius * math.cos(math.radians(camera_angle))
        y_pos = radius * math.sin(math.radians(camera_angle))
        camera_pos = (x_pos, y_pos, z_pos)

def mouseListener(button, state, x, y):
    global first_person_mode, fovY, camera_pos
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        fire_bullet()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode
        if first_person_mode:
            fovY = 90
            print("First-person mode activated")
        else:
            fovY = 120
            camera_pos = (0, 500, 500)
            print("Third-person mode activated")

def setupCamera():
    global first_person_mode, player_pos, gun_angle, gun_follow_mode, camera_pos, last_camera_coords, time_elapsed, cheat_mode
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if first_person_mode:
        neck_height = 50
        forward_offset = 10
        x, y, z = player_pos
        camera_x = x + forward_offset * math.cos(math.radians(gun_angle))
        camera_y = y + forward_offset * math.sin(math.radians(gun_angle))
        camera_z = z + neck_height
        if first_person_mode and gun_follow_mode and cheat_mode:
            if last_camera_coords and len(last_camera_coords) >= 6:
                rotation_angle = time_elapsed * 15
                look_distance = 200
                frozen_cam_x, frozen_cam_y, frozen_cam_z = last_camera_coords[0], last_camera_coords[1], last_camera_coords[2]
                look_at_x = frozen_cam_x + look_distance * math.cos(math.radians(rotation_angle))
                look_at_y = frozen_cam_y + look_distance * math.sin(math.radians(rotation_angle))
                look_at_z = frozen_cam_z + 20
                gluLookAt(frozen_cam_x, frozen_cam_y, frozen_cam_z, look_at_x, look_at_y, look_at_z, 0, 0, 1)
        elif first_person_mode and cheat_mode and not gun_follow_mode:
            if not last_camera_coords:
                look_distance = 100
                look_at_x = camera_x + look_distance * math.cos(math.radians(gun_angle))
                look_at_y = camera_y + look_distance * math.sin(math.radians(gun_angle))
                look_at_z = camera_z - 10
                last_camera_coords = (camera_x, camera_y, camera_z, look_at_x, look_at_y, look_at_z)
            gluLookAt(last_camera_coords[0], last_camera_coords[1], last_camera_coords[2], last_camera_coords[3], last_camera_coords[4], last_camera_coords[5], 0, 0, 1)
        else:
            last_camera_coords = None
            look_distance = 100
            look_at_x = camera_x + look_distance * math.cos(math.radians(gun_angle))
            look_at_y = camera_y + look_distance * math.sin(math.radians(gun_angle))
            look_at_z = camera_z - 10
            gluLookAt(camera_x, camera_y, camera_z, look_at_x, look_at_y, look_at_z, 0, 0, 1)
    else:
        last_camera_coords = None
        x, y, z = camera_pos
        gluLookAt(x, y, z,
                  0, 0, 0, 
                  0, 0, 1)

def idle():
    update_game()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    draw_grid_and_boundaries()
    if not (first_person_mode and not game_over):
        draw_player()
    for enemy in enemies:
        draw_enemy(enemy)
    for bullet in bullets:
        draw_bullet(bullet)
    if first_person_mode and not game_over:
        draw_first_person()
    draw_text(10, 720, f"Life: {player_life}")
    draw_text(10, 690, f"Score: {game_score}")
    draw_text(10, 660, f"Bullets Missed: {bullets_missed}")
    if cheat_mode:
        draw_text(10, 630, "CHEAT MODE ON")
    if gun_follow_mode and cheat_mode and first_person_mode:
        draw_text(10, 600, "GUN FOLLOW MODE ON")
    if first_person_mode:
        draw_text(10, 0, "FIRST PERSON MODE")
    if game_over:
        draw_text(400, 400, "GAME OVER!")
        draw_text(380, 370, "Press R to Restart")
    glutSwapBuffers()

def main():
    init_game()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Bullet Frenzy 3D")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

main()