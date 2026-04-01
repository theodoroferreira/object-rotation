import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Camera parameters (spherical coordinates)
camera_distance = 8.0
camera_azimuth = 45.0   # horizontal angle in degrees
camera_elevation = 30.0  # vertical angle in degrees


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


def draw_axis_labels():
    """Draw X, Y, Z labels near the positive ends of each axis."""
    label_offset = 5.3

    # X label
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos3f(label_offset, 0.0, 0.0)
    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord('X'))

    # Y label
    glColor3f(0.0, 1.0, 0.0)
    glRasterPos3f(0.0, label_offset, 0.0)
    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord('Y'))

    # Z label
    glColor3f(0.0, 0.0, 1.0)
    glRasterPos3f(0.0, 0.0, label_offset)
    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord('Z'))


def display():
    """Main display callback."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup_camera()

    draw_axes()
    draw_axis_labels()

    glutSwapBuffers()


def keyboard(key, x, y):
    """Handle regular key presses."""
    if key == b'\x1b':  # ESC key
        sys.exit(0)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Simulador de Transformacoes 3D")

    init()

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)

    glutMainLoop()


if __name__ == "__main__":
    main()
