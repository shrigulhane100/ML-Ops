from setuptools import find_packages, setup
from typing import List
hypen_e_dot = '-e .'
def get_requirements(file_path:str)->List[str]:
    ''''
    This functions will return a list of requirements
    '''
    requiements=[]
    with open(file_path) as file_obj:
        requiements=file_obj.readlines()
        requiements = [req.replace('\n', '') for req in requiements]
        if hypen_e_dot in requiements:
            requiements.remove(hypen_e_dot)

    return requiements


setup(
    name='ML-Ops', 
    version="0.0.1",
    author="Shriyash Gulhane",
    author_email="shriswimmer@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt'))

