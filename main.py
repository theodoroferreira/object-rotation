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


def display():
    """Main display callback."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup_camera()

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
