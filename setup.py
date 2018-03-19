from cx_Freeze import setup, Executable

base = None    

executables = [Executable("SpaceInvaders.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Pygame Space Invaders",
    options = options,
    version = "1.0",
    description = 'A Space invaders game made in python with pygame library',
    executables = executables
)