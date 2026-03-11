import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# --- Variabel Global ---
camera_rot_x, camera_rot_y = 20, 0
camera_zoom = -30

robot_x, robot_z = 0, 0
robot_y = 0       
jump_v = 0        
is_jumping = False
is_sitting = False # Variabel baru untuk status duduk
gravity = 0.015   
robot_yaw = 0
walk_cycle = 0
is_moving = False

# Tekstur/Lubang Spons
SPONGE_HOLES = [
    (1,1,0.6), (-1,1,0.6), (1,-1,0.6), (-1,-1,0.6),
    (0,0,0.6), (0.5, 0.5, 0.6), (-0.5, -0.5, 0.6),
    (1.1,0,0.3), (-1.1,0,0.3), (0,1.1,0.3), (0,-1.1,0.3)
]

# Gelembung
bubbles = [[random.uniform(-10, 10), -7, random.uniform(-10, 10)] for _ in range(15)]

def draw_solid_cube():
    glBegin(GL_QUADS)
    normals = [(0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)]
    verts = [
        [(-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)], [(-1,-1,-1), (-1,1,-1), (1,1,-1), (1,-1,-1)],
        [(-1,1,-1), (-1,1,1), (1,1,1), (1,1,-1)], [(-1,-1,-1), (1,-1,-1), (1,-1,1), (-1,-1,1)],
        [(1,-1,-1), (1,1,-1), (1,1,1), (1,-1,1)], [(-1,-1,-1), (-1,-1,1), (-1,1,1), (-1,1,-1)]
    ]
    for i in range(6):
        glNormal3fv(normals[i]); [glVertex3fv(v) for v in verts[i]]
    glEnd()

def draw_gary(quad, t):
    gary_move = math.sin(t * 0.5) * 3 
    glPushMatrix()
    glTranslatef(8 + gary_move, -6.8, 5) 
    glRotatef(-90 if math.cos(t*0.5) > 0 else 90, 0, 1, 0)
    glColor3f(0.7, 0.9, 1.0); glPushMatrix(); glScalef(0.5, 0.3, 1.5); draw_solid_cube(); glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0.8 + math.sin(t*2)*0.1, -0.2)
    glColor3f(1.0, 0.7, 0.8); gluSphere(quad, 0.9, 20, 20)
    glColor3f(1.0, 0.2, 0.2)
    for s in [-1, 1]:
        glPushMatrix(); glTranslatef(0.8*s, 0, 0); gluSphere(quad, 0.2, 10, 10); glPopMatrix()
    glPopMatrix()
    for s in [-1, 1]:
        glPushMatrix()
        glTranslatef(0.2*s, 0.3, 1.0); glRotatef(math.sin(t*3)*10, 0, 0, 1)
        glColor3f(0.7, 0.9, 1.0); glPushMatrix(); glRotatef(-90, 1, 0, 0); gluCylinder(quad, 0.05, 0.05, 1.0, 10, 1); glPopMatrix()
        glTranslatef(0, 1.0, 0); glColor3f(1, 1, 1); gluSphere(quad, 0.2, 12, 12)
        glColor3f(0, 0, 0); glTranslatef(0, 0, 0.15); gluSphere(quad, 0.07, 10, 10)
        glPopMatrix()
    glPopMatrix()

def draw_tv(quad):
    glPushMatrix()
    glTranslatef(-8, -5.5, -8)
    glColor3f(0.5, 0.2, 0.5); glPushMatrix(); glScalef(1.5, 1.2, 1.0); draw_solid_cube(); glPopMatrix()
    glColor3f(0.7, 0.7, 1.0); glPushMatrix(); glTranslatef(0, 0, 1.01); glScalef(1.1, 0.8, 0.05); draw_solid_cube(); glPopMatrix()
    glColor3f(0.3, 0.3, 0.3); glPushMatrix(); glTranslatef(0, 1.2, 0); glRotatef(-45, 0, 0, 1); gluCylinder(quad, 0.05, 0.01, 1.5, 10, 1); glPopMatrix()
    glPopMatrix()

def draw_chair():
    glPushMatrix()
    glTranslatef(-6, -5.0, 5) # Posisi kursi
    glRotatef(45, 0, 1, 0)
    glColor3f(0.0, 0.5, 0.2)
    glPushMatrix(); glScalef(2.5, 0.5, 2.0); draw_solid_cube(); glPopMatrix()
    glPushMatrix(); glTranslatef(0, 1.5, -1.8); glScalef(2.5, 1.5, 0.3); draw_solid_cube(); glPopMatrix()
    for s in [-1, 1]:
        glPushMatrix(); glTranslatef(2.7*s, 0.8, 0); glScalef(0.3, 0.3, 1.8); draw_solid_cube(); glPopMatrix()
    glPopMatrix()

def draw_spongebob_limb(quad, x, y, z, angle, color, is_leg=False, sitting=False):
    glPushMatrix()
    glTranslatef(x, y, z); glColor3f(color[0]*0.8, color[1]*0.8, color[2]*0.8); gluSphere(quad, 0.15, 12, 12)
    
    # Animasi kaki khusus jika sedang duduk
    if is_leg and sitting:
        glRotatef(-90, 1, 0, 0) # Kaki selonjoran ke depan
    else:
        glRotatef(angle, 1, 0, 0)
        
    glColor3fv(color)
    glPushMatrix(); glRotatef(90, 1, 0, 0); gluCylinder(quad, 0.06, 0.04, 1.2, 12, 1); glPopMatrix()
    glTranslatef(0, -1.2, 0)
    if is_leg:
        glColor3f(0.1, 0.1, 0.1); glPushMatrix(); glScalef(0.35, 0.25, 0.45); draw_solid_cube(); glPopMatrix()
    else:
        glColor3fv(color); gluSphere(quad, 0.15, 12, 12)
    glPopMatrix()

def main():
    global camera_rot_x, camera_rot_y, camera_zoom, robot_x, robot_z, robot_y, jump_v, is_jumping, is_sitting, robot_yaw, walk_cycle, is_moving, bubbles
    pygame.init(); pygame.mixer.init()
    try:
        pygame.mixer.music.load('lagu_spongebob.mp3'); pygame.mixer.music.play(-1)
    except: pass

    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    glMatrixMode(GL_PROJECTION); gluPerspective(45, (800/600), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST); glEnable(GL_LIGHTING); glEnable(GL_LIGHT0); glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_POSITION, (5, 15, 10, 1))
    
    quad = gluNewQuadric(); clock = pygame.time.Clock(); mouse_down = False

    while True:
        is_moving = False
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); return
            
            # Tombol E untuk duduk/berdiri
            if event.type == KEYDOWN:
                if event.key == K_e:
                    # Cek jarak ke kursi (-6, 5)
                    dist = math.sqrt((robot_x - (-6))**2 + (robot_z - 5)**2)
                    if dist < 4: # Jika cukup dekat
                        is_sitting = not is_sitting
                        if is_sitting:
                            robot_x, robot_z = -6, 5 # Snap ke kursi
                            robot_yaw = -45 # Hadap depan kursi
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1: mouse_down = True
                if event.button in [4, 5]: camera_zoom += 1.0 if event.button == 4 else -1.0
            if event.type == MOUSEBUTTONUP: mouse_down = False
            if event.type == MOUSEMOTION and mouse_down:
                dx, dy = event.rel; camera_rot_y += dx; camera_rot_x += dy

        # Kontrol hanya aktif jika tidak sedang duduk
        if not is_sitting:
            keys = pygame.key.get_pressed()
            if keys[K_a]: robot_yaw += 4
            if keys[K_d]: robot_yaw -= 4
            if keys[K_w]:
                robot_x += math.sin(math.radians(robot_yaw)) * 0.15
                robot_z += math.cos(math.radians(robot_yaw)) * 0.15
                is_moving = True
            if keys[K_s]:
                robot_x -= math.sin(math.radians(robot_yaw)) * 0.15
                robot_z -= math.cos(math.radians(robot_yaw)) * 0.15
                is_moving = True
            if keys[K_SPACE] and not is_jumping: jump_v = 0.35; is_jumping = True

        if is_jumping:
            robot_y += jump_v; jump_v -= gravity
            if robot_y <= 0: robot_y = 0; jump_v = 0; is_jumping = False

        walk_cycle = walk_cycle + 0.2 if is_moving and not is_jumping else walk_cycle * 0.8
        t = pygame.time.get_ticks() / 1000

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); glLoadIdentity()
        glTranslatef(0, 0, camera_zoom); glRotatef(camera_rot_x, 1, 0, 0); glRotatef(camera_rot_y, 0, 1, 0)

        # 1. LANTAI
        glBegin(GL_QUADS)
        for x in range(-20, 20, 2):
            for z in range(-20, 20, 2):
                glColor3f(0.0, 0.6, 0.8) if (x+z)%4==0 else glColor3f(0.0, 0.7, 0.9)
                glNormal3f(0, 1, 0); glVertex3f(x, -7, z); glVertex3f(x+2, -7, z); glVertex3f(x+2, -7, z+2); glVertex3f(x, -7, z+2)
        glEnd()

        draw_gary(quad, t)
        draw_tv(quad)
        draw_chair()
        
        # Gelembung
        glColor4f(1, 1, 1, 0.5)
        for b in bubbles:
            b[1] += 0.05
            if b[1] > 5: b[1] = -7; b[0] = random.uniform(-10, 10)
            glPushMatrix(); glTranslatef(b[0], b[1], b[2]); gluSphere(quad, 0.1, 8, 8); glPopMatrix()

        # 4. SPONGEBOB
        glPushMatrix()
        # Jika duduk, posisi Y diturunkan sedikit agar menempel kursi
        sit_y = -0.5 if is_sitting else 0
        glTranslatef(robot_x, -1.8 + robot_y + sit_y, robot_z); glRotatef(robot_yaw, 0, 1, 0)
        
        swing = math.sin(walk_cycle) * 40
        # Badan
        glColor3f(1, 1, 0); glPushMatrix(); glScalef(1.2, 1.2, 1.0); draw_solid_cube(); glPopMatrix()
        for hx, hy, hz in SPONGE_HOLES:
            glPushMatrix(); glColor3f(0.8, 0.8, 0.0); glTranslatef(hx, hy, hz); gluSphere(quad, 0.15, 10, 10); glPopMatrix()
        
        # Wajah
        glPushMatrix(); glTranslatef(0, 0, 1.0); glColor3f(1, 1, 1)
        for s in [-1, 1]:
            glPushMatrix(); glTranslatef(0.35*s, 0.4, 0.05); gluSphere(quad, 0.3, 24, 24)
            glColor3f(0.2, 0.2, 0.8); glTranslatef(0, 0, 0.2); gluSphere(quad, 0.12, 16, 16)
            glColor3f(0, 0, 0); glTranslatef(0, 0, 0.05); gluSphere(quad, 0.05, 10, 10); glPopMatrix()
        glColor3f(1, 1, 0); glPushMatrix(); glTranslatef(0, 0.1, 0.1); glRotatef(10, 1, 0, 0); gluCylinder(quad, 0.08, 0.06, 0.5, 12, 1); glPopMatrix()
        glColor3f(0.8, 0.2, 0.2); glPushMatrix(); glTranslatef(0, -0.4, 0.05); glScalef(0.6, 0.1, 0.05); draw_solid_cube(); glPopMatrix()
        glColor3f(1, 1, 1); [glPushMatrix() or (glTranslatef(0.12*s, -0.5, 0.06), glScalef(0.1, 0.15, 0.05), draw_solid_cube(), glPopMatrix()) for s in [-1, 1]]
        glPopMatrix()

        # Pakaian & Kaki/Lengan
        glPushMatrix(); glTranslatef(0, -1.5, 0); glColor3f(1, 1, 1); glPushMatrix(); glScalef(1.2, 0.3, 1.0); draw_solid_cube(); glPopMatrix()
        glColor3f(0.9, 0.1, 0.1); glPushMatrix(); glTranslatef(0, 0.1, 1.0); glScalef(0.15, 0.25, 0.05); draw_solid_cube(); glPopMatrix()
        glTranslatef(0, -0.6, 0); glColor3f(0.6, 0.4, 0.2); glPushMatrix(); glScalef(1.2, 0.3, 1.0); draw_solid_cube(); glPopMatrix()
        
        # Kirim status 'is_sitting' ke fungsi limb
        draw_spongebob_limb(quad, 0.4, -0.3, 0, -swing, (1, 1, 0), True, is_sitting)
        draw_spongebob_limb(quad, -0.4, -0.3, 0, swing, (1, 1, 0), True, is_sitting)
        glPopMatrix()
        
        # Lengan
        arm_angle = 45 if is_sitting else swing
        draw_spongebob_limb(quad, 1.3, -1.3, 0, arm_angle, (1, 1, 0)) 
        draw_spongebob_limb(quad, -1.3, -1.3, 0, -arm_angle, (1, 1, 0)) 

        glPopMatrix()

        pygame.display.flip(); clock.tick(60)

if __name__ == "__main__":
    main()