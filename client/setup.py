import os

from setuptools import find_packages
from setuptools import setup

setupDirectory = os.path.dirname(os.path.realpath(__file__))

requirements = []
with open(os.path.join(setupDirectory, 'requirements.txt'), 'r') as requirementsFile:
    for requirement in requirementsFile.read().splitlines():
        if requirement:
            requirements.append(requirement)

setup(
    name='kiba-pablo-client',
    version='0.1.1',
    description='Pablo client',
    url='https://github.com/kibalabs/pablo',
    packages=find_packages(exclude=['tests*']),
    python_requires='~=3.7',
    install_requires=requirements,
    tests_require=[],
    package_data={
        'pablo': [
            'py.typed',
        ]
    },
    test_suite='tests',
    include_package_data=True,
)
