import os

src = 'path/to/src'  # Replace with the actual path to the src directory
init_file = os.path.join(src, '__init__.py')

if not os.path.exists(init_file):
    open(init_file, 'w').close()

