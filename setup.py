import os
from setuptools import setup, find_packages

def get_requirements_list():
    """
    This function will return a list of requirements
    """
    requirement_list = []
    path_to_file = os.path.abspath("requirements.txt")

    with open(path_to_file) as f:
        libraries = f.readlines()

    for lib in libraries:
        if lib != '-e .' and lib != '-e .\n':
            if lib.endswith('\n'):
                requirement_list.append(lib[:-1])
            else:
                requirement_list.append(lib)

    return requirement_list

setup(
    name= "sensor",
    version= "0.0.1",
    author= "Sumegh Sen",
    author_email= "sumegh20@gmail.com",
    packages= find_packages(),
    install_requires= get_requirements_list()
)

#command to run
# python setup.py install