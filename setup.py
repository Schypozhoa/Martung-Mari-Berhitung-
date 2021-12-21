import sys
import subprocess

try:
    import OpenGL
    print(f'OpenGL found')
except ImportError:
    print('OpenGL not found, installing')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyopengl'])

try:
    import pygame
    print(f'PyGame found')
except ImportError:
    print('PyGame not found, installing')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])

print('Loading library done, run main.py')
