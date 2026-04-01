import sys
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Camera parameters (spherical coordinates)
camera_distance = 8.0
camera_azimuth = 45.0   # horizontal angle in degrees
camera_elevation = 30.0  # vertical angle in degrees

# Camera orbit speed
CAMERA_ORBIT_SPEED = 3.0  # degrees per key press

# Animation parameters
rotation_angle = 0.0
ROTATION_SPEED = 1.0  # degrees per frame


def init():
    """Initialize OpenGL settings."""
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def setup_camera():
    """Set up the perspective projection and camera position."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Convert spherical to cartesian coordinates
    azimuth_rad = math.radians(camera_azimuth)
    elevation_rad = math.radians(camera_elevation)

    eye_x = camera_distance * math.cos(elevation_rad) * math.sin(azimuth_rad)
    eye_y = camera_distance * math.sin(elevation_rad)
    eye_z = camera_distance * math.cos(elevation_rad) * math.cos(azimuth_rad)

    gluLookAt(eye_x, eye_y, eye_z,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)


def draw_axes():
    """Draw color-coded X, Y, Z axes through the origin."""
    axis_length = 5.0

    glBegin(GL_LINES)

    # X axis - Red
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-axis_length, 0.0, 0.0)
    glVertex3f(axis_length, 0.0, 0.0)

    # Y axis - Green
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -axis_length, 0.0)
    glVertex3f(0.0, axis_length, 0.0)

    # Z axis - Blue
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -axis_length)
    glVertex3f(0.0, 0.0, axis_length)

    glEnd()


def draw_wireframe_cube(size=0.4):
    """Draw a wireframe cube centered at the origin."""
    s = size / 2.0
    edges = [
        # Bottom face
        (-s, -s, -s), (s, -s, -s),
        (s, -s, -s), (s, -s, s),
        (s, -s, s), (-s, -s, s),
        (-s, -s, s), (-s, -s, -s),
        # Top face
        (-s, s, -s), (s, s, -s),
        (s, s, -s), (s, s, s),
        (s, s, s), (-s, s, s),
        (-s, s, s), (-s, s, -s),
        # Vertical edges
        (-s, -s, -s), (-s, s, -s),
        (s, -s, -s), (s, s, -s),
        (s, -s, s), (s, s, s),
        (-s, -s, s), (-s, s, s),
    ]
    glBegin(GL_LINES)
    for v in edges:
        glVertex3f(*v)
    glEnd()


def draw_cube(x, y, z, rot_axis_x, rot_axis_y, rot_axis_z, size=0.4):
    """Draw a wireframe cube at (x, y, z) rotating around the given axis."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation_angle, rot_axis_x, rot_axis_y, rot_axis_z)
    glColor3f(1.0, 1.0, 0.0)
    draw_wireframe_cube(size)
    glPopMatrix()


def draw_cubes():
    """Draw 6 cubes at axis extremities, each rotating around its respective axis."""
    pos = 4.0  # position along axis (within axis length of 5.0, with visible gap)

    # +X and -X: rotate around X axis
    draw_cube(pos, 0.0, 0.0, 1.0, 0.0, 0.0)
    draw_cube(-pos, 0.0, 0.0, 1.0, 0.0, 0.0)

    # +Y and -Y: rotate around Y axis
    draw_cube(0.0, pos, 0.0, 0.0, 1.0, 0.0)
    draw_cube(0.0, -pos, 0.0, 0.0, 1.0, 0.0)

    # +Z and -Z: rotate around Z axis
    draw_cube(0.0, 0.0, pos, 0.0, 0.0, 1.0)
    draw_cube(0.0, 0.0, -pos, 0.0, 0.0, 1.0)


def draw_axis_labels():
    """Draw X, Y, Z labels near the positive ends of each axis using pygame font rendering."""
    font = pygame.font.SysFont("helvetica", 18)
    labels = [
        ("X", (255, 0, 0), 5.3, 0.0, 0.0),
        ("Y", (0, 255, 0), 0.0, 5.3, 0.0),
        ("Z", (0, 0, 255), 0.0, 0.0, 5.3),
    ]

    for text, color, x, y, z in labels:
        # Project 3D position to 2D screen coordinates
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        screen = gluProject(x, y, z, modelview, projection, viewport)
        if screen is not None:
            sx, sy = int(screen[0]), int(WINDOW_HEIGHT - screen[1])
            surface = font.render(text, True, color)
            texture_data = pygame.image.tostring(surface, "RGBA", True)
            w, h = surface.get_size()

            # Save OpenGL state and draw as 2D overlay
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            glDisable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            glRasterPos2i(sx, WINDOW_HEIGHT - sy)
            glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

            glDisable(GL_BLEND)
            glEnable(GL_DEPTH_TEST)

            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()


def display():
    """Main display function."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup_camera()

    draw_axes()
    draw_axis_labels()
    draw_cubes()

    pygame.display.flip()


def main():
    global rotation_angle, camera_azimuth, camera_elevation

    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Simulador de Transformacoes 3D")

    init()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

        # Handle held keys for smooth camera orbit
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            camera_azimuth -= CAMERA_ORBIT_SPEED
        if keys[K_RIGHT]:
            camera_azimuth += CAMERA_ORBIT_SPEED
        if keys[K_UP]:
            camera_elevation += CAMERA_ORBIT_SPEED
        if keys[K_DOWN]:
            camera_elevation -= CAMERA_ORBIT_SPEED

        # Clamp elevation to avoid flipping at poles
        camera_elevation = max(-89.0, min(89.0, camera_elevation))
        # Keep azimuth in [0, 360) range
        camera_azimuth = camera_azimuth % 360.0

        # Update animation
        rotation_angle += ROTATION_SPEED
        if rotation_angle >= 360.0:
            rotation_angle -= 360.0

        display()
        clock.tick(60)


if __name__ == "__main__":
    main()
