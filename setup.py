### Setup Configuration
from setuptools import setup, find_packages
from typing import List


def get_requirements() -> List[str]:
    ''' This function reads the requirements.txt file and returns a list of dependencies.
    '''
    requirements = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement  and requirement != '-e .':
                    requirements.append(requirement)
            
    except FileNotFoundError:
        print("requirements.txt file not found.")
    return requirements

print(get_requirements())

setup(
    name='network_security_mlops_project',
    version='0.0.1',
    author='Aymen Maiziz',
    author_email='aymenmaiziz55@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)
