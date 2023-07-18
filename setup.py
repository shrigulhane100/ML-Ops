from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    """
    Retrieves a list of requirements from a file.

    Args:
        file_path (str): The path to the file containing the requirements.

    Returns:
        List[str]: A list of requirements extracted from the file.
    """
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements


setup(
    name='ML-Ops', 
    version="0.0.1",
    author="Shriyash Gulhane",
    author_email="shriswimmer@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt'))


